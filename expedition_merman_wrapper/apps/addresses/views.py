"""Модуль содержит view на эндпоинт /addresses ."""
from expedition_merman_wrapper.base.base_crud_view import BaseCrudView
from expedition_merman_wrapper.common.http_methods import HttpMethods
from .serializers import AddressSchema, AddressRequestSchema
from .use_cases import AddressUseCasesPack


class AddressView(BaseCrudView):
    """View реализует GET и PUT методы на эндпоинт /addresses ."""

    tags = ('addresses',)
    definitions = {
        'AddressSchema': AddressSchema,
        'AddressRequestSchema': AddressRequestSchema
    }

    http_methods = (HttpMethods.GET, HttpMethods.PUT, HttpMethods.POST)
    use_cases_pack = AddressUseCasesPack()
    put_args_schema = AddressRequestSchema
    post_args_schema = AddressRequestSchema
    marshal_schema = AddressSchema

    def get(self, entity_id):
        """Возвращает адрес по идентификатору.

        ---
        parameters:
          - name: entity_id
            in: path
            type: integer
            description:
              Идентификатор адреса
        responses:
          200:
            description: Возвращает адрес.
            schema:
              $ref: '#/definitions/AddressSchema'

        """
        return super().get(entity_id)

    def put(self, entity_id):
        """Обновляет указанный адрес.

        ---
        parameters:
          - name: entity_id
            description:
                Идентификатор адреса
            in: path
            type: integer
          - in: body
            name: body
            description:
              Атрибуты адреса
            required: true
            schema:
              $ref: '#/definitions/AddressRequestSchema'
        responses:
          201:
            description: Обновленный адрес
            schema:
              $ref: '#/definitions/AddressSchema'

        """
        return super().put(entity_id)

    def post(self):
        """Создает новый адрес клиента.

        ---
        parameters:
          - name: body
            in: body
            required: true
            description:
              Атрибуты адреса
            schema:
              $ref: '#/definitions/AddressRequestSchema'
        responses:
          201:
            description: Новый адрес
            schema:
              $ref: '#/definitions/AddressSchema'

        """
        return super().post()
