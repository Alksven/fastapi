from fastapi import FastAPI, Query
from typing import Optional
from datetime import date
from pydantic import BaseModel
from app.booking.router import router as router_bookings

app = FastAPI()

app.include_router(router_bookings)

class SHotel(BaseModel):
    address: str
    name: str
    stars: int



@app.get("/hotels")
async def get_hotel(
        location: str,
        date_from: date,
        date_to: date,
        stars: Optional[int] = Query(None, ge=1, le=5),
        has_spa: Optional[bool] = None
) -> list[SHotel]:
    hotels = [
        {"address": "Гагарина 5", "name": "Василек", "stars": 5}
    ]
    return hotels

class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


@app.post("/booking")
async def add_booking(booking: SBooking):
    pass
