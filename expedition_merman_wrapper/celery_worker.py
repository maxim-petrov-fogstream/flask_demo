"""expedition-merman-wrapper celery application."""
import os

from expedition_merman_wrapper import celery, create_app  # noqa: F401

app = create_app()
app.app_context().push()

SENTRY_DSN = os.getenv('SENTRY_DSN')
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.celery import CeleryIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=(CeleryIntegration(),)
    )
