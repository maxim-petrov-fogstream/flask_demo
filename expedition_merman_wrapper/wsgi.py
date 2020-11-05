"""expedition_merman_wrapper wsgi config."""
from expedition_merman_wrapper import create_app


application = create_app(__name__)
