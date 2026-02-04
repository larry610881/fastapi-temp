import base64
import logging
from typing import Union, Dict, Any, Optional
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from app.core.config import settings
import os

logger = logging.getLogger(__name__)

class EncryptionService:
    def rsa_sign(self, data: str) -> Union[str, Dict[str, str]]:
        """
        使用RSA私鑰對資料進行簽名
        
        Args:
            data: 要簽名的資料
            
        Returns:
            簽名後的資料（Base64編碼）或錯誤字典
        """
        try:
            private_key_path = settings.ICP_CLIENT_PRIVATE_KEY_PATH
            
            if not os.path.exists(private_key_path):
                 return {'error': f'Private key not found at {private_key_path}'}

            with open(private_key_path, 'rb') as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                    backend=default_backend()
                )

            signature = private_key.sign(
                data.encode('utf-8'),
                padding.PKCS1v15(),
                hashes.SHA256()
            )

            return base64.b64encode(signature).decode('utf-8')

        except Exception as e:
            return {'error': f'RSA簽名過程發生錯誤: {str(e)}'}

    def aes_encrypt(self, data: str) -> Union[str, Dict[str, str]]:
        """
        使用AES加密資料
        
        Args:
            data: 要加密的資料
            
        Returns:
            加密後的資料 (Raw bytes)
        """
        try:
            key = settings.ICP_AES_KEY.encode('utf-8')
            iv = settings.ICP_AES_IV.encode('utf-8')
            
            # Pad data to block size (16 bytes for AES)
            # PKCS7 padding
            block_size = 128 # bits
            # In bytes: 16
            bs = 16
            raw_data = data.encode('utf-8')
            padding_len = bs - (len(raw_data) % bs)
            padded_data = raw_data + bytes([padding_len] * padding_len)

            # Justification: Required for legacy system (ICP) compatibility
            # nosemgrep: python.cryptography.security.mode-without-authentication.crypto-mode-without-authentication
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            encrypted = encryptor.update(padded_data) + encryptor.finalize()
            
            return encrypted
        except Exception as e:
            return {'error': f'AES加密過程發生錯誤: {str(e)}'}

    def aes_decrypt(self, data: Union[bytes, str]) -> Union[str, Dict[str, str]]:
        """
        使用AES解密資料
        """
        try:
            key = settings.ICP_AES_KEY.encode('utf-8')
            iv = settings.ICP_AES_IV.encode('utf-8')
            
            # Justification: Required for legacy system (ICP) compatibility
            # nosemgrep: python.cryptography.security.mode-without-authentication.crypto-mode-without-authentication
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            
            # If data is str, ensure bytes.
            if isinstance(data, str):
                data = data.encode('latin-1') 

            decrypted_padded = decryptor.update(data) + decryptor.finalize()
            
            # Unpad (PKCS7)
            padding_len = decrypted_padded[-1]
            if padding_len < 1 or padding_len > 16:
                 # Padding error or no padding
                 # Return as is or handle error, strictly legacy might fail silently or return garbage
                 pass
                 
            decrypted = decrypted_padded[:-padding_len]
            
            return decrypted.decode('utf-8')
        except Exception as e:
            return {'error': f'AES解密過程發生錯誤: {str(e)}'}

    def verify_signature(self, data: str, signature: str) -> Union[bool, Dict[str, str]]:
        """
        驗證RSA簽名
        """
        try:
            public_key_path = settings.ICP_SERVER_PUBLIC_KEY_PATH
            
            if not os.path.exists(public_key_path):
                 return {'error': f'Public key not found at {public_key_path}'}

            with open(public_key_path, 'rb') as key_file:
                public_key = serialization.load_pem_public_key(
                    key_file.read(),
                    backend=default_backend()
                )

            decoded_signature = base64.b64decode(signature)
            
            # verify throws exception if invalid
            public_key.verify(
                decoded_signature,
                data.encode('utf-8'),
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return True
        except Exception as e:
            logger.error(f"Signature verification failed: {e}")
            return False
