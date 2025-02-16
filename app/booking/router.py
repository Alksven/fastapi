from fastapi import APIRouter

from app.booking.dao import BookingDAO

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"]
)

@router.get("")
async def get_bookings():
    return await BookingDAO.find_all()

@router.post('1')
async def asdf():
    return "hello world"


