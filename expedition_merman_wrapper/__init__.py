"""expedition-merman_wrapper flask application."""
from decimal import getcontext

import sentry_sdk
from celery import Celery
from flasgger import Swagger
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sentry_sdk.integrations.flask import FlaskIntegration
from sqlalchemy.dialects import sqlite

from expedition_merman_wrapper.apps.addresses import init_app as init_addresses
from expedition_merman_wrapper.apps.cars import init_app as init_cars
from expedition_merman_wrapper.apps.cities import init_app as init_cities
from expedition_merman_wrapper.apps.clients import init_app as init_clients
from expedition_merman_wrapper.apps.delivery_statements import (
    init_app as init_delivery_statements
)
from expedition_merman_wrapper.apps.employees import init_app as init_employees
from expedition_merman_wrapper.apps.packings import init_app as init_packings
from expedition_merman_wrapper.apps.ping import init_app as init_ping
from expedition_merman_wrapper.apps.products import init_app as init_products
from expedition_merman_wrapper.apps.sales_invoice import (
    init_app as init_sales_invoices
)
from expedition_merman_wrapper.apps.shifts import init_app as init_shifts
from expedition_merman_wrapper.apps.users import init_app as init_users
from expedition_merman_wrapper.apps.reciprocal_payments import (
    init_app as init_reciprocal_payments
)
from expedition_merman_wrapper.config import configure_app, BaseConfig

__version__ = '0.0.1'

db = SQLAlchemy()

celery = Celery(__name__, broker=BaseConfig.CELERY_BROKER_URL)


def create_app(import_name: str = __name__,
               config_name: str = 'default') -> Flask:
    """Create new flask app."""
    app = Flask(import_name)

    # configuration
    configure_app(app, config_name=config_name)

    init_addresses(app)
    init_cars(app)
    init_cities(app)
    init_clients(app)
    init_delivery_statements(app)
    init_employees(app)
    init_ping(app)
    init_products(app)
    init_sales_invoices(app)
    init_shifts(app)
    init_packings(app)
    init_users(app)
    init_reciprocal_payments(app)

    from expedition_merman_wrapper.apps.events.handler_task import (  # noqa F401
        events_handler_task
    )

    db.init_app(app)

    if BaseConfig.SWAGGER_ENABLED:
        Swagger(app)

    if app.config.get('SENTRY_DSN'):
        sentry_sdk.init(
            dsn=app.config.get('SENTRY_DSN'),
            integrations=[FlaskIntegration()]
        )

    celery.conf.update(app.config)

    getcontext().prec = 2

    return app


BigIntegerType = db.BigInteger()
BigIntegerType = BigIntegerType.with_variant(sqlite.INTEGER(), 'sqlite')
