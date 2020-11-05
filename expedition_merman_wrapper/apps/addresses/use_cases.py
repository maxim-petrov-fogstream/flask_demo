"""Модуль с use cases для работы с адресами."""
from expedition_merman_wrapper.apps.cities.repository import CitiesRepository
from expedition_merman_wrapper.apps.streets.repository import StreetsRepository
from expedition_merman_wrapper.base.base_crud_use_case_pack import (
    BaseCrudUseCasesPack
)
from expedition_merman_wrapper.base.base_use_cases import (
    BaseCreateUseCase, BaseUpdateByIdUseCase
)
from expedition_merman_wrapper.common.repositories import get_by_name_or_create
from .repository import AddressesRepository


class CreateAddressUseCase(BaseCreateUseCase):
    """Use case на создание адреса."""

    def __init__(self, session):
        """Конструктор use case для создания адреса клиента."""
        super().__init__(AddressesRepository, session)
        self.streets_repository: StreetsRepository = StreetsRepository(session)
        self.cities_repository: CitiesRepository = CitiesRepository(session)

    def execute(self, args: dict):
        """Создает адрес клиента.

        При необходимости, создаются:
            - город клиента
            - улица клиента

        :param args: атрибуты адреса клиента

        :return: адрес клиента
        """
        street_name = args.get('street', None)
        city_name = args.get('city', None)

        address = self.repository.create(attributes=args)

        city = get_by_name_or_create(
            name=city_name,
            repository=self.cities_repository
        )

        street = get_by_name_or_create(
            name=street_name,
            repository=self.streets_repository
        )

        street.city = city
        address.street = street

        address_name_elements = (
            street.name,
            f' {args.get("building")}' if args.get('building') else None,
            f', кв/оф {args["apartment"]}' if args.get('apartment') else None,
        )

        address.name = ''.join(
            item for item in address_name_elements if item
        )

        address.phone_number = args.get('phone_number', None)

        return address


class UpdateAddressUseCase(BaseUpdateByIdUseCase):
    """Use case на обновление адреса."""

    def __init__(self, session):
        """Конструктор use case для обновления адреса клиента."""
        super().__init__(AddressesRepository, session)
        self.streets_repository: StreetsRepository = StreetsRepository(session)
        self.cities_repository: CitiesRepository = CitiesRepository(session)

    def execute(self, entity_id: int, args: dict):
        """Обновляет адрес клиента.

        При необходимости, создаются:
            - город клиента
            - улица клиента

        :param entity_id: идентификатор адреса
        :param args: атрибуты адреса клиента

        :return: адрес клиента
        """
        address = self.repository.update_by_id(
            entity_id=entity_id,
            attributes=args
        )

        street = self._get_street(
            street_name=args.get('street', None),
            city_name=args.get('city', None)
        )

        if street:
            address.street = street

        return address

    def _get_street(self, street_name: str, city_name: str):
        """Метод достает из БД улицу по имени или создает новую.

        :param street_name: название улицы
        :param city_name: название города

        :return: улицу
        """
        if not street_name:
            return

        street = get_by_name_or_create(
            name=street_name,
            repository=self.streets_repository
        )

        if city_name:
            city = get_by_name_or_create(
                name=city_name,
                repository=self.cities_repository
            )

            street.city = city

        return street


class AddressUseCasesPack(BaseCrudUseCasesPack):
    """Пак с набором CRUD use cases для работы с адресами."""

    def __init__(self):
        """Конструктор use case для создания адреса клиента."""
        super().__init__(AddressesRepository)

    def post_use_case(self, session) -> BaseCreateUseCase:
        """Метод возвращает use case на POST метод."""
        return CreateAddressUseCase(session)

    def put_use_case(self, session) -> BaseUpdateByIdUseCase:
        """Метод возвращает use case на PUT метод."""
        return UpdateAddressUseCase(session)
