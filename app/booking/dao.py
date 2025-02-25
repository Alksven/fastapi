
from app.dao.base import BaseDAO
from app.booking.models import Bookings
from datetime import date
from sqlalchemy import select, and_, or_, insert, func

from app.database import engine, async_session_maker
from app.hotels.rooms.models import Rooms


# class BookingDAO(BaseDAO):
#     model = Bookings
#
#     @classmethod
#     async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
#         async with async_session_maker() as session:
#             booked_rooms = select(Bookings).where(
#                 and_(
#                     Bookings.room_id == room_id,
#                     or_(
#                         and_(
#                             Bookings.date_from >= date_from,
#                             Bookings.date_from <= date_to
#                         ),
#                         and_(
#                             Bookings.date_from <= date_from,
#                             Bookings.date_to > date_from
#                         )
#
#                     )
#                 )
#             ).cte("booked_rooms")
#
#             get_rooms_left = select(
#                 Rooms.quantity - func.count(booked_rooms.c.room_id).label("rooms_left")
#                 ).select_from(Rooms).join(
#                 booked_rooms, booked_rooms.c.room_id == Rooms.id
#             ).where(Rooms.id == room_id).group_by(
#                 Rooms.quantity, booked_rooms.c.room_id
#             )
#
#             print(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))
#
#             rooms_left = await session.execute(get_rooms_left)
#             rooms_left  = rooms_left.scalar()
#             print(rooms_left, "rooms_left")
#
#             if rooms_left > 0:
#                 get_price = select(Rooms.price).filter_by(id=room_id)
#                 price = await session.execute(get_price)
#                 price  =  price.scalar()
#                 print(price, "price")
#
#                 add_booking = insert(Bookings).values(
#                     room_id=room_id,
#                     user_id=user_id,
#                     date_from=date_from,
#                     date_to=date_to,
#                     price=price
#                 ).returning(Bookings)
#
#                 new_booking = await session.execute(add_booking)
#                 await session.commit()
#                 return new_booking.scalar()
#             else:
#                 return None

class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            # Проверка пересечения дат бронирования
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == room_id,
                    or_(
                        and_(
                            Bookings.date_from < date_to,
                            Bookings.date_to > date_from
                        )
                    )
                )
            ).cte("booked_rooms")

            # Подсчет оставшихся комнат и получение цены
            get_rooms_left = select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left"),
                Rooms.price
            ).select_from(Rooms).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            ).where(Rooms.id == room_id).group_by(
                Rooms.quantity, Rooms.price, booked_rooms.c.room_id
            )

            result = await session.execute(get_rooms_left)
            row = result.first()

            if not row:
                raise ValueError("Room not found")

            rooms_left, price = row

            if rooms_left <= 0:
                raise ValueError("No available rooms for the selected dates")

            add_booking = insert(Bookings).values(
                room_id=room_id,
                user_id=user_id,
                date_from=date_from,
                date_to=date_to,
                price=price
            ).returning(Bookings)

            new_booking = await session.execute(add_booking)
            await session.commit()
            return new_booking.scalar()