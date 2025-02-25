from fastapi import APIRouter, Depends

from app.booking.dao import BookingDAO
from app.booking.schemas import SBooking
from app.exceptions import RoomCannotBeException
from app.users.dependencies import get_current_user
from app.users.model import Users
from datetime import date

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"]
)

@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)

@router.post("")
async def add_booking(room_id: int, date_from: date, date_to: date,
    user: Users = Depends(get_current_user)):
    booking =  await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeException
