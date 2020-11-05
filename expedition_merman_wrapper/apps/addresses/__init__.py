"""Модуль с инициализатором приложения адресов."""


def init_app(flask_app):
    """Метод инициализирует приложение адресов.

    :param flask_app: flask приложение
    """
    from .views import AddressView

    address_view = AddressView.as_view('addresses_api')

    flask_app.add_url_rule(
        '/addresses/<int:entity_id>',
        view_func=address_view,
        methods=('GET', 'PUT')
    )

    flask_app.add_url_rule(
        '/addresses',
        view_func=address_view,
        methods=('POST',)
    )
