# game_client.py
import socket
import threading
import json
import time
try:
    from .game_crypto import GameCrypto
except ImportError:
    from game_crypto import GameCrypto

class GameClient:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.socket = None
        self.crypto = GameCrypto()
        self.connected = False
        self.player_id = None
        self.game_state = {}
        self.callbacks = {}
        self.pending_commands = {}  # Хранение команд для повторной отправки
        self.max_retries = 3  # Максимальное количество попыток
        self.retry_delay = 1  # Задержка между попытками в секундах
        self.receive_buffer = b""  # Буфер для получения данных
        self.expected_length = 0  # Ожидаемая длина данных
        
    def connect(self):
        """Подключение к игровому серверу"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(30)  # Таймаут 30 секунд
            self.socket.connect((self.host, self.port))
            self.crypto.generate_keys()
            
            # Получаем публичный ключ сервера
            key_len_bytes = self._recv_exact(4)
            if not key_len_bytes:
                return False
            key_len = int.from_bytes(key_len_bytes, 'big')
            server_pub_key = self._recv_exact(key_len)
            if not server_pub_key:
                return False
            self.crypto.load_public_key(server_pub_key)
            
            # Отправляем публичный ключ клиента
            client_pub_key = self.crypto.serialize_public_key()
            self.socket.send(len(client_pub_key).to_bytes(4, 'big'))
            self.socket.send(client_pub_key)
            
            # Отправляем сессионный ключ
            session_key = self.crypto.generate_session_key()
            encrypted_session_key = self.crypto.encrypt_rsa(session_key)
            self.socket.send(len(encrypted_session_key).to_bytes(4, 'big'))
            self.socket.send(encrypted_session_key)
            
            # Получаем подтверждение
            response_len_bytes = self._recv_exact(4)
            if not response_len_bytes:
                return False
            response_len = int.from_bytes(response_len_bytes, 'big')
            encrypted_response = self._recv_exact(response_len)
            if not encrypted_response:
                return False
                
            response = self.crypto.decrypt_game_data(encrypted_response)
            
            if response.get('status') == 'ok':
                self.connected = True
                receive_thread = threading.Thread(target=self.receive_messages)
                receive_thread.daemon = True
                receive_thread.start()
                
                return True
            else:
                print("Ошибка подключения: нет статуса 'ok'")
                return False
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return False
    
    def _recv_exact(self, length):
        """Чтение точного количества байт"""
        data = b""
        while len(data) < length:
            try:
                chunk = self.socket.recv(length - len(data))
                if not chunk:
                    return None
                data += chunk
            except socket.timeout:
                print("Таймаут при чтении данных")
                return None
            except Exception as e:
                print(f"Ошибка чтения данных: {e}")
                return None
        return data
    
    def receive_messages(self):
        """Получение сообщений от сервера"""
        while self.connected:
            try:
                # Получаем длину сообщения
                data_len_bytes = self._recv_exact(4)
                if not data_len_bytes:
                    print("Соединение разорвано (нет данных длины)")
                    self.connected = False
                    break
                    
                data_len = int.from_bytes(data_len_bytes, 'big')
                if data_len == 0:
                    continue
                
                # Получаем зашифрованные данные
                encrypted_data = self._recv_exact(data_len)
                if not encrypted_data:
                    print("Соединение разорвано (нет данных)")
                    self.connected = False
                    break
                
                try:
                    game_data = self.crypto.decrypt_game_data(encrypted_data)
                    self.handle_server_message(game_data)
                except ValueError as e:
                    print(f"Ошибка целостности данных: {e}")
                    # Отправляем запрос на повторную отправку
                    self.request_resend()
                    
            except socket.timeout:
                continue  # Игнорируем таймауты, продолжаем слушать
            except (ConnectionResetError, BrokenPipeError):
                print("Соединение разорвано сервером")
                self.connected = False
                break
            except Exception as e:
                print(f"Ошибка получения данных: {e}")
                self.connected = False
                break
    
    def handle_server_message(self, game_data):
        """Обработка сообщений от сервера"""
        msg_type = game_data.get('type')
        
        if msg_type == 'response':
            # Ответ на нашу команду
            if 'callback' in game_data:
                callback_id = game_data['callback']
                if callback_id in self.callbacks:
                    self.callbacks[callback_id](game_data)
                    del self.callbacks[callback_id]
        
        elif msg_type == 'player_move':
            # Другой игрок переместился
            player_id = game_data.get('player_id')
            position = game_data.get('position')
            
            if player_id in self.game_state.get('other_players', {}):
                self.game_state['other_players'][player_id]['position'] = position
        elif msg_type == 'player_disconnect':
            player_id = game_data.get('player_id')
            if 'other_players' in self.game_state and player_id in self.game_state['other_players']:
                del self.game_state['other_players'][player_id]
        elif msg_type == 'game_update':
            pass
        elif msg_type == 'resend_request':
            # Сервер запрашивает повторную отправку
            self.resend_pending_command(game_data.get('command_id'))
            
        if hasattr(self, 'on_message'):
            self.on_message(game_data)
    
    def send_command(self, command_type, data=None, callback=None):
        """Отправка команды на сервер с механизмом повторной отправки"""
        if not self.connected:
            raise ConnectionError("Не подключено к серверу")
        if data is None:
            data = {}
        
        command_data = {'type': command_type, **data}
        callback_id = str(time.time())
        
        if callback:
            command_data['callback'] = callback_id
            self.callbacks[callback_id] = callback
        
        # Сохраняем команду для возможной повторной отправки
        self.pending_commands[callback_id] = {
            'data': command_data,
            'retries': 0,
            'sent_time': time.time()
        }
        
        return self._send_command_internal(callback_id)
    
    def _send_command_internal(self, callback_id):
        """Внутренняя отправка команды с обработкой ошибок"""
        if callback_id not in self.pending_commands:
            return False
            
        command_info = self.pending_commands[callback_id]
        
        if command_info['retries'] >= self.max_retries:
            print(f"Достигнуто максимальное количество попыток для команды {callback_id}")
            del self.pending_commands[callback_id]
            return False
        
        try:
            encrypted = self.crypto.encrypt_game_data(command_info['data'])
            self.socket.send(len(encrypted).to_bytes(4, 'big'))
            self.socket.send(encrypted)
            
            command_info['retries'] += 1
            command_info['sent_time'] = time.time()
            
            return True
        except Exception as e:
            print(f"Ошибка отправки: {e}")
            
            # Пытаемся отправить снова через некоторое время
            if command_info['retries'] < self.max_retries:
                time.sleep(self.retry_delay)
                return self._send_command_internal(callback_id)
            else:
                self.connected = False
                return False
    
    def request_resend(self):
        """Запрос повторной отправки последнего сообщения"""
        resend_request = {
            'type': 'resend_request',
            'timestamp': time.time()
        }
        
        try:
            encrypted = self.crypto.encrypt_game_data(resend_request)
            self.socket.send(len(encrypted).to_bytes(4, 'big'))
            self.socket.send(encrypted)
            return True
        except Exception as e:
            print(f"Ошибка отправки запроса на повтор: {e}")
            return False
    
    def resend_pending_command(self, command_id=None):
        """Повторная отправка ожидающей команды"""
        if not self.pending_commands:
            return
            
        if command_id:
            # Повторяем конкретную команду
            if command_id in self.pending_commands:
                self._send_command_internal(command_id)
        else:
            # Повторяем самую старую команду
            oldest_id = min(self.pending_commands.keys(), 
                          key=lambda k: self.pending_commands[k]['sent_time'])
            self._send_command_internal(oldest_id)
    
    def login(self, username, password, callback=None):
        """Авторизация игрока"""
        password_hash = self.hash_password(password)
        
        return self.send_command('login', {
            'username': username,
            'password_hash': password_hash
        }, callback)
    
    def move(self, x, y, z=0, callback=None):
        """Перемещение игрока"""
        return self.send_command('move', {
            'position': {'x': x, 'y': y, 'z': z}
        }, callback)
    
    def perform_action(self, action, target=None, callback=None):
        """Выполнение игрового действия"""
        data = {'action': action}
        if target:
            data['target'] = target
        
        return self.send_command('action', data, callback)
    
    def get_game_state(self, callback=None):
        """Запрос текущего состояния игры"""
        return self.send_command('get_state', callback=callback)
    
    def hash_password(self, password):
        """Хэширование пароля (упрощенное)"""
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()
    
    def disconnect(self):
        """Отключение от сервера"""
        self.connected = False
        if self.socket:
            self.socket.close()
    
    def set_message_handler(self, handler):
        """Установка обработчика входящих сообщений"""
        self.on_message = handler

# Пример использования клиента
def main():
    client = GameClient('127.0.0.1', 5555)
    
    def handle_message(data):
        print(f"📨 Получено: {data}")
    
    client.set_message_handler(handle_message)
    
    if client.connect():
        # Логин
        def login_callback(response):
            if response.get('status') == 'success':
                client.player_id = response.get('player_id')
                client.game_state = response.get('game_state', {})
                print(f"🎮 Игрок авторизован: {client.player_id}")
                
                # Перемещаемся после логина
                client.move(10, 5, callback=lambda r: print(f"Перемещение: {r}"))
            else:
                print(f"❌ Ошибка логина: {response.get('message')}")
        
        client.login("player1", "password123", login_callback)
        
        # Держим соединение открытым
        try:
            while client.connected:
                time.sleep(1)
                # Можно отправлять периодические запросы состояния
                # client.get_game_state()
        except KeyboardInterrupt:
            print("\n👋 Выход...")
        finally:
            client.disconnect()

if __name__ == "__main__":
    main()