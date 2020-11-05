"""Модуль с моделями адреса."""

from sqlalchemy import Sequence, ForeignKey
from sqlalchemy.orm import relationship

from expedition_merman_wrapper import db, BigIntegerType
from expedition_merman_wrapper.apps.streets.models import Street


class Address(db.Model):
    """Модель адреса клиента.

    Fields:
        ``id : int`` - идентификатор

        ``house : str?`` - номер дома

        ``building : str?`` - корпус дома

        ``apartment : str?`` - номер квартиры

        ``entrance : str?`` - номер подъезда

        ``floor : str?`` - номер этажа

        ``lat : str?`` - широта

        ``lon : str?`` - долгота

        ``stop_date : datetime?`` - дата остановки доставки на адрес

        ``start_date : datetime?`` - дата возобновления доставки на адрес

        ``phone_number: str?`` - телефон клиента

        ``comment : str?`` - комментарий к адресу

        ``additional_info : str?`` - дополнительная информация

        ``client_id : int?`` - идентификатор клиента, связанный с адресом

        ``street_id : int?`` - идентификатор улицы, связанный с адресом

        ``street`` : :class:`Street`? - улица, на которой расположен адрес
    """

    __tablename__ = 'kontragenty_adr'

    id = db.Column(
        BigIntegerType,
        Sequence(name='GEN_KONTRAGENTY_ADR_ID', optional=True),
        primary_key=True
    )
    name = db.Column('naimenovanie', db.String(100))
    house = db.Column('dom', db.String(50))
    building = db.Column('korpus', db.String(10))
    apartment = db.Column('kv', db.String(50))
    entrance = db.Column('pod', db.String(50))
    floor = db.Column('et', db.Integer)
    lat = db.Column('shirota', db.String(50))
    lon = db.Column('dolgota', db.String(50))
    stop_date = db.Column('stopd', db.DateTime)
    start_date = db.Column('startd', db.DateTime)
    phone_number = db.Column('telefon', db.String(255))

    comment = db.Column(db.String(255))
    additional_info = db.Column('dop_sv', db.String(255))

    # В таблице поле osntabl_id не является FK
    client_id = db.Column('osntabl_id', ForeignKey('kontragenty.id'))
    street_id = db.Column('ulica', ForeignKey('ulicy.id'))

    street: Street = relationship('Street', lazy='joined')
