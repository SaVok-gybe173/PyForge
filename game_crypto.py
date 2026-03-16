# game_crypto.py
import json
import base64
import os
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import time

class GameCrypto:
    def __init__(self):
        self.session_key = None
        self.cipher = None
        self.server_public_key = None
        self.private_key = None
        self.public_key = None
        self.handshake_complete = False
        
    def generate_keys(self):
        """Генерация RSA ключей для игрового клиента/сервера"""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
        
    def serialize_public_key(self):
        """Сериализация публичного ключа для отправки"""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
    def load_public_key(self, pem_data):
        """Загрузка публичного ключа из данных"""
        self.server_public_key = serialization.load_pem_public_key(
            pem_data,
            backend=default_backend()
        )
    
    def encrypt_rsa(self, data):
        """Шифрование данных публичным ключом сервера"""
        if not self.server_public_key:
            raise ValueError("Нет публичного ключа сервера")
            
        return self.server_public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    
    def decrypt_rsa(self, encrypted_data):
        """Дешифрование данных приватным ключом"""
        return self.private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    
    def generate_session_key(self):
        """Генерация сессионного ключа для AES"""
        self.session_key = Fernet.generate_key()
        self.cipher = Fernet(self.session_key)
        return self.session_key
    
    def encrypt_game_data(self, data_dict):
        """Шифрование игровых данных"""
        if not self.cipher:
            raise ValueError("Сессионный ключ не установлен")
        
        # Добавляем временную метку для защиты от replay-атак
        data_dict['timestamp'] = time.time()
        data_dict['nonce'] = os.urandom(8).hex()  # Добавляем случайность
        
        json_data = json.dumps(data_dict, ensure_ascii=False).encode('utf-8')
        encrypted = self.cipher.encrypt(json_data)
        
        # Добавляем HMAC для проверки целостности
        hmac = self._generate_hmac(encrypted)
        
        # Формат: длина HMAC (2 байта) + HMAC + данные
        hmac_length = len(hmac)
        return hmac_length.to_bytes(2, 'big') + hmac + encrypted
    
    def decrypt_game_data(self, encrypted_data):
        """Дешифрование игровых данных"""
        if not self.cipher:
            raise ValueError("Сессионный ключ не установлен")
        
        try:
            # Получаем длину HMAC
            if len(encrypted_data) < 2:
                raise ValueError("Недостаточно данных для чтения длины HMAC")
            
            hmac_length = int.from_bytes(encrypted_data[:2], 'big')
            
            # Проверяем, что данных достаточно
            if len(encrypted_data) < 2 + hmac_length:
                raise ValueError("Недостаточно данных для чтения HMAC и зашифрованных данных")
            
            # Извлекаем HMAC и данные
            hmac_part = encrypted_data[2:2+hmac_length]
            data_part = encrypted_data[2+hmac_length:]
            
            # Проверяем HMAC
            expected_hmac = self._generate_hmac(data_part)
            if hmac_part != expected_hmac:
                raise ValueError("Ошибка проверки целостности данных")
            
            # Дешифруем
            decrypted = self.cipher.decrypt(data_part)
            data_dict = json.loads(decrypted.decode('utf-8'))
            
            # Проверяем временную метку (защита от старых пакетов)
            current_time = time.time()
            if current_time - data_dict['timestamp'] > 30:  # 30 секунд максимум
                raise ValueError("Устаревшие данные")
            
            return data_dict
        except Exception as e:
            # Добавляем информацию об ошибке
            raise ValueError(f"Ошибка дешифровки: {str(e)}")
    
    def _generate_hmac(self, data):
        """Генерация HMAC для проверки целостности"""
        if not self.session_key:
            raise ValueError("Сессионный ключ не установлен")
        
        h = hashlib.sha256(self.session_key + data)
        return h.digest()[:16]  # Берем первые 16 байт
    
    def set_session_key(self, key):
        """Установка сессионного ключа"""
        self.session_key = key
        self.cipher = Fernet(key)
        self.handshake_complete = True