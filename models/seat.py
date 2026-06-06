from extensions import db
from sqlalchemy import Integer, String, Boolean, DateTime, Column, ForeignKey
from datetime import datetime


class Seats(db.Model):
    id = Column(Integer(), primary_key=True)
    seat_number = Column(Integer(), unique=True)
    flight_id = Column(Integer(), ForeignKey("flights.id"), nullable=False)
    seat_class = Column(String(20), nullable=False)  # economy / business / vip
    is_booked = Column(Boolean(), default=False)
    user_id = Column(Integer(), db.ForeignKey("users.id"), nullable=True)
    booked_at = Column(DateTime(), default=datetime.utcnow)

    flight = db.relationship('Flights', backref='flights', foreign_keys=[flight_id])
