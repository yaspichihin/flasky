import pytest
import time

from app import create_app, db
from app.models import User


def test_password_setter():
    user = User(password="cat")
    assert user.password_hash is not None


def test_no_password_getter():
    user = User(password="cat")
    with pytest.raises(AttributeError):
        user.password


def test_password_verification():
    user = User(password="cat")
    assert user.verify_password("cat")
    assert not user.verify_password("dog")


def test_password_salts_are_random():
    user1 = User(password="cat")
    user2 = User(password="dog")
    assert user1.password_hash != user2.password_hash


def test_valid_confirmation_token(prepare_app_context):
    user = User(password='cat')
    db.session.add(user)
    db.session.commit()
    token = user.generate_confirmation_token()
    assert user.confirm(token)


def test_invalid_confirmation_token(prepare_app_context):
    user1 = User(password='cat')
    user2 = User(password='cat')
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    token = user1.generate_confirmation_token()
    assert not user2.confirm(token)


def test_valid_reset_token(prepare_app_context):
    user = User(password='cat')
    db.session.add(user)
    db.session.commit()
    token = user.generate_reset_token()
    assert User.reset_password(token, 'dog')
    assert user.verify_password('dog')


def test_invalid_reset_token(prepare_app_context):
    user = User(password='cat')
    db.session.add(user)
    db.session.commit()
    token = user.generate_reset_token()
    assert not User.reset_password(token + 'a', 'horse')
    assert user.verify_password('cat')


def test_valid_email_change_token(prepare_app_context):
    user = User(email='john@example.com', password='cat')
    db.session.add(user)
    db.session.commit()
    token = user.generate_email_change_token('susan@example.org')
    assert user.change_email(token)
    assert user.email == 'susan@example.org'


def test_invalid_email_change_token(prepare_app_context):
    user1 = User(email='john@example.com', password='cat')
    user2 = User(email='susan@example.org', password='dog')
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    token = user1.generate_email_change_token('david@example.net')
    assert not user2.change_email(token)
    assert user2.email == 'susan@example.org'


def test_duplicate_email_change_token(prepare_app_context):
    user1 = User(email='john@example.com', password='cat')
    user2 = User(email='susan@example.org', password='dog')
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    token = user2.generate_email_change_token('john@example.com')
    assert not user2.change_email(token)
    assert user2.email == 'susan@example.org'
