import pytest
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings
from jose import jwt

def test_password_hashing():
    password = "testpassword"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)

def test_jwt_token_creation():
    subject = "testuser"
    token = create_access_token(subject)
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    assert decoded["sub"] == subject
