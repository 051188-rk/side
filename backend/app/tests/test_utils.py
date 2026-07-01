import pytest
from app.utils.helpers import (
    generate_hash,
    sanitize_input,
    truncate_text,
    extract_urls,
    extract_emails,
    calculate_similarity_score,
    mask_sensitive_data,
    chunk_text,
    normalize_whitespace,
    is_valid_url,
)
from app.utils.validators import (
    validate_email_address,
    validate_url,
    validate_phone_number,
    validate_username,
    validate_password_strength,
    sanitize_html,
)
from app.utils.date_utils import (
    utc_now,
    to_utc,
    add_days,
    add_hours,
    format_duration,
    get_start_of_day,
    get_end_of_day,
)


def test_generate_hash():
    content = "test content"
    hash1 = generate_hash(content)
    hash2 = generate_hash(content)
    assert hash1 == hash2
    assert len(hash1) == 64


def test_sanitize_input():
    content = "<script>alert('xss')</script>Hello World"
    sanitized = sanitize_input(content)
    assert "<script>" not in sanitized
    assert "Hello World" in sanitized


def test_truncate_text():
    content = "a" * 1000
    truncated = truncate_text(content, 100)
    assert len(truncated) == 103
    assert truncated.endswith("...")


def test_extract_urls():
    content = "Check out https://example.com and http://test.org"
    urls = extract_urls(content)
    assert len(urls) == 2
    assert "https://example.com" in urls


def test_extract_emails():
    content = "Contact us at test@example.com or admin@test.org"
    emails = extract_emails(content)
    assert len(emails) == 2
    assert "test@example.com" in emails


def test_calculate_similarity_score():
    text1 = "The app is crashing on startup"
    text2 = "Application crashes when starting"
    score = calculate_similarity_score(text1, text2)
    assert 0 <= score <= 1


def test_mask_sensitive_data():
    content = "Email: test@example.com, API Key: abc123xyz456"
    masked = mask_sensitive_data(content)
    assert "test@example.com" not in masked
    assert "***" in masked


def test_chunk_text():
    content = "a" * 2500
    chunks = chunk_text(content, 1000, 100)
    assert len(chunks) == 3
    assert all(len(chunk) <= 1000 + 100 for chunk in chunks)


def test_normalize_whitespace():
    content = "Hello    World\n\nTest"
    normalized = normalize_whitespace(content)
    assert "Hello World Test" == normalized


def test_is_valid_url():
    assert is_valid_url("https://example.com") == True
    assert is_valid_url("http://test.org/path") == True
    assert is_valid_url("not-a-url") == False


def test_validate_email_address():
    assert validate_email_address("test@example.com") == True
    assert validate_email_address("invalid-email") == False


def test_validate_phone_number():
    assert validate_phone_number("+1234567890") == True
    assert validate_phone_number("123") == False


def test_validate_username():
    assert validate_username("user123") == True
    assert validate_username("user@123") == False


def test_validate_password_strength():
    result = validate_password_strength("weak")
    assert result["valid"] == False
    
    result = validate_password_strength("StrongPass123!")
    assert result["valid"] == True


def test_sanitize_html():
    content = "<script>alert('xss')</script><p>Hello</p>"
    sanitized = sanitize_html(content)
    assert "<script>" not in sanitized
    assert "Hello" in sanitized


def test_utc_now():
    now = utc_now()
    assert now is not None
    assert now.tzinfo is not None


def test_add_days():
    now = utc_now()
    future = add_days(now, 7)
    assert (future - now).days == 7


def test_add_hours():
    now = utc_now()
    future = add_hours(now, 24)
    assert (future - now).total_seconds() == 86400


def test_format_duration():
    assert format_duration(30) == "30.00s"
    assert format_duration(120) == "2.00m"
    assert format_duration(7200) == "2.00h"


def test_get_start_of_day():
    now = utc_now()
    start = get_start_of_day(now)
    assert start.hour == 0
    assert start.minute == 0
    assert start.second == 0


def test_get_end_of_day():
    now = utc_now()
    end = get_end_of_day(now)
    assert end.hour == 23
    assert end.minute == 59
    assert end.second == 59
