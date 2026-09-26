import bcrypt

BCRYPT_ROUNDS = 12

# Precomputed dummy hash for timing-attack equalization
DUMMY_HASH = "$2a$12$e80yqZ6G9lT2b6hTzGkM1.aP0uVlUqNkJ2a3zK3/Hq9r8F1D0m0s2"

def validate_password(password: str, confirm_password: str = None) -> dict:
    if not password or not isinstance(password, str):
        return {"valid": False, "reason": "Password is required"}
    if len(password) < 8:
        return {"valid": False, "reason": "Password must be at least 8 characters long"}
    if len(password) > 128:
        return {"valid": False, "reason": "Password cannot exceed 128 characters"}
    if confirm_password is not None and password != confirm_password:
        return {"valid": False, "reason": "Passwords do not match"}
    return {"valid": True}

def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_str: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_str.encode("utf-8"))
    except Exception:
        return False

def verify_dummy_password(plain_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), DUMMY_HASH.encode("utf-8"))
    except Exception:
        return False
