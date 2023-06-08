import pytest

from app.models import User


def test_password_setter():
    u = User(password="cat")
    assert u.password_hash is not None


def test_no_password_getter():
    u = User(password="cat")
    with pytest.raises(AttributeError):
        u.password


def test_password_verification():
    u = User(password="cat")
    assert u.verify_password("cat")
    assert not u.verify_password("dog")


def test_password_salts_are_random():
    u1 = User(password="cat")
    u2 = User(password="dog")
    assert u1.password_hash != u2.password_hash
