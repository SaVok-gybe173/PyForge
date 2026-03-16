# game_server.py
import socket
import threading
import random
try:
    from .game_crypto import GameCrypto
except ImportError:
    from game_crypto import GameCrypto
import time

class GameServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = {}  # client_socket: {'crypto': GameCrypto, 'player_id': ..., 'last_response': ...}
        self.game_state = {}
        
        # Генерация ключей сервера
        self.crypto = GameCrypto()
        self.crypto.generate_keys()
        
    def start(self):
        """Запуск сервера"""
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f"🎮 Игровой сервер запущен на {self.host}:{self.port}")
        print(f"🔑 Публичный ключ сервера готов")
        
        # Поток для обработки подключений
        accept_thread = threading.Thread(target=self.accept_connections, daemon=True)
        accept_thread.start()
        
        # Основной игровой цикл
        self.game_loop()
    
    def accept_connections(self):
        """Принятие подключений клиентов"""
        while True:
            client, address = self.server.accept()
            print(f"🔗 Подключен новый клиент: {address}")
            
            # Создаем объект криптографии для клиента
            client_crypto = GameCrypto()
            client_crypto.generate_keys()
            client_crypto.load_public_key(self.crypto.serialize_public_key())
            
            # Сохраняем клиента
            self.clients[client] = {
                'crypto': client_crypto,
                'address': address,
                'player_id': None,
                'authenticated': False,
                'last_response': None  # Храним последний ответ для повторной отправки
            }
            
            # Отправляем публичный ключ сервера
            server_pub_key = self.crypto.serialize_public_key()
            client.send(len(server_pub_key).to_bytes(4, 'big') + server_pub_key)
            
            # Запускаем поток для обработки клиента
            thread = threading.Thread(
                target=self.handle_client,
                args=(client,), daemon=True
            )
            thread.start()
    
    def handle_client(self, client):
        """Обработка клиентского соединения"""
        client_data = self.clients[client]
        crypto = client_data['crypto']
        
        try:
            # 1. Получаем публичный ключ клиента
            key_len = int.from_bytes(client.recv(4), 'big')
            client_pub_key = client.recv(key_len)
            crypto.load_public_key(client_pub_key)
            
            # 2. Выполняем квитирование (handshake)
            self.perform_handshake(client, crypto)
            
            # 3. Основной цикл обработки игровых команд
            while True:
                # Получаем длину сообщения
                data_len = int.from_bytes(client.recv(4), 'big')
                if data_len == 0:
                    break
                
                # Получаем зашифрованные данные
                encrypted_data = client.recv(data_len)
                
                # Дешифруем
                try:
                    game_data = crypto.decrypt_game_data(encrypted_data)
                    
                    # Обрабатываем игровую команду
                    response = self.process_game_command(client, game_data)
                    
                    # Сохраняем последний ответ для возможной повторной отправки
                    if response and 'callback' in game_data:
                        client_data['last_response'] = {
                            'data': response,
                            'callback_id': game_data['callback']
                        }
                    
                    # Шифруем и отправляем ответ
                    if response:
                        encrypted_response = crypto.encrypt_game_data(response)
                        client.send(len(encrypted_response).to_bytes(4, 'big'))
                        client.send(encrypted_response)
                        
                except ValueError as e:
                    print(f"❌ Ошибка целостности данных от клиента: {e}")
                    # Отправляем ошибку с предложением повторить
                    error_data = {'type': 'error', 'message': 'Data integrity error', 'need_resend': True}
                    encrypted_error = crypto.encrypt_game_data(error_data)
                    client.send(len(encrypted_error).to_bytes(4, 'big'))
                    client.send(encrypted_error)
                    
                except Exception as e:
                    print(f"❌ Ошибка обработки данных: {e}")
                    # Отправляем ошибку
                    error_data = {'type': 'error', 'message': 'Invalid data'}
                    encrypted_error = crypto.encrypt_game_data(error_data)
                    client.send(len(encrypted_error).to_bytes(4, 'big'))
                    client.send(encrypted_error)
                    
        except (ConnectionResetError, BrokenPipeError):
            print(f"📤 Клиент отключился: {client_data['address']}")
        finally:
            self.remove_client(client)
    
    def perform_handshake(self, client, crypto):
        """Выполнение криптографического квитирования"""
        # 1. Получаем зашифрованный сессионный ключ от клиента
        key_len = int.from_bytes(client.recv(4), 'big')
        encrypted_session_key = client.recv(key_len)
        
        # 2. Расшифровываем сессионный ключ своим приватным ключом
        session_key = self.crypto.decrypt_rsa(encrypted_session_key)
        
        # 3. Устанавливаем сессионный ключ
        crypto.set_session_key(session_key)
        
        # 4. Отправляем подтверждение
        handshake_ok = {'type': 'handshake', 'status': 'ok'}
        encrypted_response = crypto.encrypt_game_data(handshake_ok)
        client.send(len(encrypted_response).to_bytes(4, 'big'))
        client.send(encrypted_response)
        
        print(f"🤝 Квитирование завершено для клиента")
    
    def process_game_command(self, client, game_data):
        """Обработка игровой команды"""
        cmd_type = game_data.get('type')
        player_id = self.clients[client].get('player_id')
        
        # Обработка запроса на повторную отправку
        if cmd_type == 'resend_request':
            # Повторно отправляем последний ответ
            if self.clients[client]['last_response']:
                return self.clients[client]['last_response']['data']
            else:
                return {'type': 'error', 'message': 'No previous response to resend'}
        
        response = {'type': 'response', 'timestamp': time.time()}
        
        if cmd_type == 'login':
            # Аутентификация игрока
            username = game_data.get('username')
            password_hash = game_data.get('password_hash')
            
            if username and password_hash:
                player_id = self.generate_player_id()
                self.clients[client]['player_id'] = player_id
                self.clients[client]['authenticated'] = True
                self.game_state[player_id] = {
                    'username': username,
                    'position': {'x': 0, 'y': 0, 'z': 0},
                    'health': 100,
                    'inventory': []
                }
                
                response.update({
                    'status': 'success',
                    'player_id': player_id,
                    'game_state': self.game_state[player_id]
                })
            else:
                response.update({'status': 'error', 'message': 'Invalid credentials'})
                
        elif cmd_type == 'move':
            # Движение игрока
            if player_id and self.clients[client]['authenticated']:
                new_position = game_data.get('position')
                if new_position:
                    self.game_state[player_id]['position'] = new_position
                    
                    # Рассылаем обновление другим игрокам
                    self.broadcast_player_move(player_id, new_position)
                    
                    response.update({
                        'status': 'success',
                        'position': new_position
                    })
        
        elif cmd_type == 'action':
            # Игровое действие (атака, использование предмета и т.д.)
            action = game_data.get('action')
            target = game_data.get('target')
            
            response.update({
                'status': 'success',
                'action_result': 'completed'
            })
        
        elif cmd_type == 'get_state':
            # Запрос состояния игры
            if player_id:
                response.update({
                    'status': 'success',
                    'game_state': self.game_state.get(player_id, {}),
                    'other_players': self.get_other_players(player_id)
                })
        
        # Добавляем callback ID если он был в запросе
        if 'callback' in game_data:
            response['callback'] = game_data['callback']
        
        return response
    
    def broadcast_player_move(self, player_id, position):
        """Рассылка движения игрока другим клиентам"""
        update_data = {
            'type': 'player_move',
            'player_id': player_id,
            'position': position,
            'timestamp': time.time()
        }
        
        for client, data in self.clients.items():
            if data['authenticated'] and data['player_id'] != player_id:
                try:
                    encrypted_update = data['crypto'].encrypt_game_data(update_data)
                    client.send(len(encrypted_update).to_bytes(4, 'big'))
                    client.send(encrypted_update)
                except:
                    pass  # Игнорируем ошибки отправки
    
    def get_other_players(self, exclude_player_id):
        """Получение данных других игроков"""
        return {
            pid: {k: v for k, v in data.items() if k != 'inventory'}
            for pid, data in self.game_state.items()
            if pid != exclude_player_id
        }
    
    def generate_player_id(self):
        """Генерация уникального ID игрока"""
        return f"player_{random.randint(len(self.game_state), 999999)}"
    
    def remove_client(self, client):
        """Удаление клиента"""
        if client in self.clients:
            player_id = self.clients[client].get('player_id')
            if player_id and player_id in self.game_state:
                del self.game_state[player_id]
                # Оповещаем других игроков об уходе
                self.broadcast_player_disconnect(player_id)
            del self.clients[client]
        client.close()
    
    def broadcast_player_disconnect(self, player_id):
        """Рассылка об отключении игрока"""
        disconnect_data = {
            'type': 'player_disconnect',
            'player_id': player_id
        }
        
        for client, data in self.clients.items():
            if data['authenticated']:
                try:
                    encrypted = data['crypto'].encrypt_game_data(disconnect_data)
                    client.send(len(encrypted).to_bytes(4, 'big'))
                    client.send(encrypted)
                except:
                    pass
    
    def game_loop(self):
        """Основной игровой цикл (тики сервера)"""
        tick_rate = 20  # 20 тиков в секунду
        tick_interval = 1.0 / tick_rate
        
        while True:
            time.sleep(tick_interval)
            
            # Обновление игровой логики
            # Например, проверка столкновений, регенерация здоровья и т.д.
            
            # Рассылка периодических обновлений
            self.broadcast_game_updates()
    
    def broadcast_game_updates(self):
        """Рассылка периодических игровых обновлений"""
        update_data = {
            'type': 'game_update',
            'timestamp': time.time(),
            'server_time': time.time()
        }
        
        for client, data in self.clients.items():
            if data['authenticated']:
                try:
                    encrypted = data['crypto'].encrypt_game_data(update_data)
                    client.send(len(encrypted).to_bytes(4, 'big'))
                    client.send(encrypted)
                except:
                    pass

if __name__ == "__main__":
    server = GameServer()
    server.start()