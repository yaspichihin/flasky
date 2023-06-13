import os
from pathlib import Path


BASE_DIR = Path(__file__).parent


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secured_key"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_ADMIN = "...@yandex.ru"
    FLASKY_POSTS_PER_PAGE = 20

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(BASE_DIR / "data" / "flasky_db_dev.sqlite3")

    MAIL_SUBJECT_PREFIX = "[FLASKY]-"
    MAIL_SENDER = "FLASKY Admin <...@yandex.ru>"
    MAIL_RECEIVER = "...@yandex.ru"
    MAIL_SERVER = "smtp.yandex.ru"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "..."
    MAIL_PASSWORD = "..."


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(BASE_DIR / "data" / "flasky_db_test.sqlite3")


class ProductionConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(BASE_DIR / "data" / "flasky_db_prod.sqlite3")


config = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "prod": ProductionConfig
}
