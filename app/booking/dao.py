from app.dao.base import BaseDAO
from app.booking.models import Bookings

class BookingDAO(BaseDAO):
    model = Bookings