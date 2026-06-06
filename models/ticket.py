from extensions import db
from sqlalchemy import Integer, String, DateTime, Column, ForeignKey, Enum
from datetime import datetime

class Tickets(db.Model):
    id = Column (Integer(), primary_key= True)

    flight_id = Column (Integer(), ForeignKey("flights.id"))

    airplane_name = Column (String(110), ForeignKey('airplanes.name'))

    seat_id = Column (Integer())
    seat_type = Column (Enum("vip", "economy", "business", name="seat_type_enum"))

    user_id = Column (Integer(), ForeignKey("users.id"))
    full_name = Column (String(110), ForeignKey("users.full_name"))
    national_code = Column (String(110), ForeignKey("users.national_code"))
    phone = Column (Integer(), ForeignKey("users.phone"))

    price = Column (Integer())

    created_at = Column(DateTime(), default=datetime.utcnow)
