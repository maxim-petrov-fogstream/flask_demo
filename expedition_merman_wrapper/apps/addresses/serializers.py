"""Модуль со схемами сериализатора эндпоинта /addresses ."""

from flasgger import Schema, fields
from marshmallow import EXCLUDE

from expedition_merman_wrapper.apps.streets.serializers import StreetSchema


class BaseAddressSchema(Schema):
    """Базовая схема сериализатора адреса."""

    name = fields.Str(allow_none=True)
    house = fields.Str(allow_none=True)
    building = fields.Str(allow_none=True)
    apartment = fields.Str(allow_none=True)
    entrance = fields.Str(allow_none=True)
    floor = fields.Int(allow_none=True)
    comment = fields.Str(allow_none=True)
    additional_info = fields.Str(allow_none=True)
    start_date = fields.DateTime(allow_none=True)
    stop_date = fields.DateTime(allow_none=True)
    phone_number = fields.Str(allow_none=True)


class AddressSchema(BaseAddressSchema):
    """Схема сериализатора адреса."""

    id = fields.Int()
    street = fields.Pluck(StreetSchema, 'name')
    city = fields.Pluck(
        StreetSchema,
        'city',
        attribute='street',
        dump_only=True
    )
    shift_id = fields.Int()
    client_id = fields.Int()


class AddressRequestSchema(BaseAddressSchema):
    """Схема десериализатора адреса."""

    client_id = fields.Int()
    street = fields.Str(load_only=True, allow_none=True)
    city = fields.Str()

    class Meta:  # noqa:D106
        unknown = EXCLUDE
