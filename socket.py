import socket
from socket import socket as _socket
from typing import Optional

from .encrypted import ( 
    generate_dh_private_key,
    compute_dh_public_key,
    compute_shared_secret,
    encrypt_with_shared,
    decrypt_with_shared,
)


class SecureSocket(_socket):
    """
    Сокет с поддержкой Diffie–Hellman и шифрования (XOR + PBKDF2).
    Наследует стандартный socket.socket, добавляет методы для защищённого обмена.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._shared_secret: Optional[int] = None
        self._priv_key: Optional[int] = None
        self._pub_key: Optional[int] = None


    def gen_dh_keypair(self) -> int:
        """Генерирует пару ключей DH, возвращает публичный ключ."""
        self._priv_key = generate_dh_private_key()
        self._pub_key = compute_dh_public_key(self._priv_key)
        return self._pub_key

    def set_shared_secret(self, other_public_key: int) -> int:
        """Вычисляет общий секрет на основе чужого публичного ключа."""
        if self._priv_key is None:
            raise RuntimeError("Сначала вызовите gen_dh_keypair()")
        self._shared_secret = compute_shared_secret(self._priv_key, other_public_key)
        return self._shared_secret

    def exchange_keys(self, server_side: bool = False):
        """
        Обменивается публичными ключами с удалённой стороной.
        server_side=True – сервер (ждёт ключ первым), False – клиент (отправляет первым).
        После вызова общий секрет доступен через ._shared_secret.
        """
        pub = self.gen_dh_keypair()
        if server_side:
            other_pub = int(self.recv(1024).decode().strip())
            self.sendall(str(pub).encode())
        else:
            self.sendall(str(pub).encode())
            other_pub = int(self.recv(1024).decode().strip())
        self.set_shared_secret(other_pub)

    def send_encrypted(self, data: str):
        """Шифрует строку через encrypt_with_shared и отправляет."""
        if self._shared_secret is None:
            raise RuntimeError("Сначала выполните обмен ключами (exchange_keys)")
        encrypted = encrypt_with_shared(data, self._shared_secret)
        self.sendall(encrypted.encode())

    def recv_encrypted(self, bufsize: int = 4096) -> str:
        """Получает данные, расшифровывает через decrypt_with_shared."""
        if self._shared_secret is None:
            raise RuntimeError("Сначала выполните обмен ключами (exchange_keys)")
        raw = self.recv(bufsize).decode()
        return decrypt_with_shared(raw, self._shared_secret)


if __name__ == "__main__":
    import threading
    import time

    def server():
        with SecureSocket() as s:
            s.bind(('127.0.0.1', 65432))
            s.listen(1)
            print("Сервер ждёт подключения...")
            conn, addr = s.accept()
            with conn:
                print(f"Клиент подключён: {addr}")
                # Сервер: ждём ключ клиента (server_side=True)
                conn.exchange_keys(server_side=True)
                # Получаем сообщение
                msg = conn.recv_encrypted()
                print(f"Сервер получил: {msg}")
                # Отправляем ответ
                conn.send_encrypted("Привет, клиент! Сообщение получено.")

    def client():
        time.sleep(0.5)
        with SecureSocket() as s:
            s.connect(('127.0.0.1', 65432))
            # Клиент: отправляем ключ первым (server_side=False)
            s.exchange_keys(server_side=False)
            s.send_encrypted("Привет, сервер! Это секретное сообщение.")
            reply = s.recv_encrypted()
            print(f"Клиент получил: {reply}")

    # Запускаем сервер в потоке, клиент в основном
    threading.Thread(target=server, daemon=True).start()
    client()