import base64
import os
from cryptography.fernet import Fernet
from flask import current_app

_fernet_instance = None

def get_fernet():
    global _fernet_instance
    if _fernet_instance is not None:
        return _fernet_instance

    key = current_app.config.get("FIELD_ENCRYPTION_KEY") if current_app else os.environ.get("FIELD_ENCRYPTION_KEY")
    if not key:
        # Fallback to deterministic key or generate if none provided
        key = Fernet.generate_key()
    elif isinstance(key, str):
        key = key.encode()
        
    _fernet_instance = Fernet(key)
    return _fernet_instance

def encrypt_text(plain_text: str) -> bytes:
    """Encrypt raw document text using Fernet/AES before storing at rest."""
    if not plain_text:
        return b""
    f = get_fernet()
    return f.encrypt(plain_text.encode("utf-8"))

def decrypt_text(encrypted_bytes: bytes) -> str:
    """Decrypt encrypted document text for audit-only purposes."""
    if not encrypted_bytes:
        return ""
    f = get_fernet()
    return f.decrypt(encrypted_bytes).decode("utf-8")
