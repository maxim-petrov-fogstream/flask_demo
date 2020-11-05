"""expedition_merman_wrapper flask config."""

import os


class BaseConfig:
    """Base flask configuration."""

    CONFIG_FILE = os.path.abspath(__file__)
    CONFIG_DIR = os.path.dirname(CONFIG_FILE)
    BASE_DIR = os.path.abspath(os.path.join(CONFIG_DIR, '..'))

    DB_HOST = os.getenv('FIREBIRD_HOST', 'firebird')
    DB_PORT = int(os.getenv('FIREBIRD_PORT', 3050))
    DATABASE_URI = os.getenv(
        'FIREBIRD_DATABASE_URI', '/firebird/data/expedition_merman'
    )
    FIREBIRD_USER = os.getenv('FIREBIRD_USER', 'SYSDBA')
    FIREBIRD_PASSWORD = os.getenv('FIREBIRD_PASSWORD', 'isc_admin')

    MERMAN_USER_ID = int(os.getenv('MERMAN_USER_ID', 1000000000001))
    DEFAULT_FIRM_ID = int(os.getenv('DEFAULT_FIRM_ID', 1000000000002))
    DEFAULT_PAYMENT_TYPE = int(
        os.getenv('DEFAULT_PAYMENT_TYPE', 1000000000002)
    )
    DEFAULT_STOCK_ID = int(os.getenv('DEFAULT_STOCK_ID', 1000000000001))
    DEFAULT_CASHBOX_ID = int(os.getenv('DEFAULT_CASHBOX_ID', 1000000000001))

    SQLALCHEMY_DATABASE_URI = (
        f'firebird+fdb://{FIREBIRD_USER}:{FIREBIRD_PASSWORD}@'
        f'{DB_HOST}:{DB_PORT}/{DATABASE_URI}?charset=WIN1251'
    )
    SQLALCHEMY_MIGRATE_REPO = os.path.join(CONFIG_DIR, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv(
        'SQLALCHEMY_TRACK_MODIFICATIONS'
    )

    MAX_PAGE_SIZE = int(os.getenv('MAX_PAGE_SIZE', '1000'))
    SWAGGER_ENABLED = os.getenv('SWAGGER_ENABLED', 'False') == 'True'
    SENTRY_DSN = os.getenv('SENTRY_DSN', None)

    CELERY_BROKER_HOST = os.getenv('CELERY_BROKER_HOST', 'redis')
    CELERY_BROKER_PORT = os.getenv('CELERY_BROKER_PORT', '6379')
    CELERY_BROKER_DB_ID = os.getenv('CELERY_BROKER_DB_ID', '11')

    CELERY_BROKER_URL = CELERY_RESULT_BACKEND = (
        f'redis://{CELERY_BROKER_HOST}:{CELERY_BROKER_PORT}'
        f'/{CELERY_BROKER_DB_ID}'
    )

    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
    RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', '5672')
    RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
    RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'guest')

    RABBITMQ_URL = (
        f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@'
        f'{RABBITMQ_HOST}:{RABBITMQ_PORT}/%2F'
    )

    RABBITMQ_RUN_WORKERS = os.getenv('RABBITMQ_RUN_WORKERS', 'FALSE') == 'TRUE'

    DEBUG = False
    TESTING = False
    HOST = 'localhost'
    PORT = 8000


class DevelopmentConfig(BaseConfig):
    """Flask configuration for devserver."""

    DEBUG = True
    TESTING = False

    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'FALSE') == 'TRUE'


class ProductionConfig(BaseConfig):
    """Flask configuration for production."""

    DEBUG = False
    TESTING = False


class TestingConfig(BaseConfig):
    """Flask configuration for tests."""

    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = False
    TESTING = True
    PORT = 9091


CONFIG = {
    'default': 'expedition_merman_wrapper.config.DevelopmentConfig',
    'dev': 'expedition_merman_wrapper.config.DevelopmentConfig',
    'prod': 'expedition_merman_wrapper.config.ProductionConfig',
    'test': 'expedition_merman_wrapper.config.TestingConfig',
}


def configure_app(app, config_name='default'):
    """Configure flask app."""
    config_name = os.getenv('CONFIG_NAME', None) or config_name
    app.config.from_object(CONFIG[config_name])
