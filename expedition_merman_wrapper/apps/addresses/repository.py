"""Модуль с репозиторием адресов."""
from datetime import datetime

from expedition_merman_wrapper.common.repositories import CommonRepository
from .models import Address


class AddressesRepository(CommonRepository):
    """Класс-репозиторий адресов."""

    model = Address

    def create(self, attributes: dict):
        """Метод на создание адреса.

        :param attributes: атрибуты создаваемого адреса
        """
        address_attributes = self._create_address_attributes(
            attributes=attributes
        )

        address_attributes.update({'start_date': datetime.now()})
        return super().create(address_attributes)

    def update_by_id(self, entity_id: int, attributes: dict):
        """Метод обновляет адрес по идентификатору.

        :param entity_id: идентификатор адреса
        :param attributes: атрибуты адреса

        :return: обновлённый адрес
        """
        address_attributes = self._create_address_attributes(
            attributes=attributes
        )

        address_attributes.update({'stop_date': attributes.get('stop_date')})
        return super().update_by_id(entity_id, address_attributes)

    @staticmethod
    def _create_address_attributes(attributes: dict) -> dict:
        return dict(
            house=attributes.get('house'),
            building=attributes.get('building'),
            apartment=attributes.get('apartment'),
            entrance=attributes.get('entrance'),
            floor=attributes.get('floor'),
            lat=attributes.get('lat'),
            lon=attributes.get('lon'),
            comment=attributes.get('comment'),
            additional_info=attributes.get('additional_info'),
            client_id=attributes.get('client_id')
        )
