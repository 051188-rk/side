import re
from typing import Optional, List
from pydantic import validator
from email_validator import validate_email, EmailNotValidError


def validate_email_address(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


def validate_url(url: str) -> bool:
    pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return pattern.match(url) is not None


def validate_phone_number(phone: str) -> bool:
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone) is not None


def validate_username(username: str) -> bool:
    pattern = r'^[a-zA-Z0-9_]{3,30}$'
    return re.match(pattern, username) is not None


def validate_password_strength(password: str) -> dict:
    result = {
        "valid": True,
        "score": 0,
        "issues": []
    }
    
    if len(password) < 8:
        result["valid"] = False
        result["issues"].append("Password must be at least 8 characters")
    
    if not re.search(r'[A-Z]', password):
        result["valid"] = False
        result["issues"].append("Password must contain uppercase letters")
    
    if not re.search(r'[a-z]', password):
        result["valid"] = False
        result["issues"].append("Password must contain lowercase letters")
    
    if not re.search(r'\d', password):
        result["valid"] = False
        result["issues"].append("Password must contain digits")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        result["valid"] = False
        result["issues"].append("Password must contain special characters")
    
    result["score"] = len(password) + (1 if re.search(r'[A-Z]', password) else 0) + \
                     (1 if re.search(r'[a-z]', password) else 0) + \
                     (1 if re.search(r'\d', password) else 0) + \
                     (1 if re.search(r'[!@#$%^&*(),.?":{}|<>]', password) else 0)
    
    return result


def sanitize_html(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<.*?>', '', text)
    return text.strip()


def validate_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    import hmac
    import hashlib
    
    expected_signature = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected_signature)


def validate_discord_webhook(signature: str, body: bytes, public_key: str) -> bool:
    try:
        from nacl.signing import VerifyKey
        verify_key = VerifyKey(bytes.fromhex(public_key))
        verify_key.verify(body, bytes.fromhex(signature))
        return True
    except Exception:
        return False
