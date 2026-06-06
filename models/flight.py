from extensions import db
from sqlalchemy import Integer, String, Time, DateTime, Date, Column, ForeignKey
from datetime import datetime

class Flights(db.Model):
    id = Column (Integer(), primary_key= True)
    airplane_name = Column (String(), ForeignKey("airplanes.name"))
    airplane_id = Column (Integer(), ForeignKey("airplanes.id"))
    origin = Column(String(110)) #مبدا
    destination = Column(String(110)) #مقصد
    departure_time = Column (Time(), nullable=False) #ساعت پرواز
    arrival_time = Column (Time(), nullable=False) #ساعت رسیدن
    departure_date = Column (Date()) #تاریخ پرواز
    arrival_date = Column (Date()) #روزتاریخ رسیدن
    economy_price = Column (Integer())
    business_price = Column (Integer())
    vip_price = Column (Integer())
    economy_passengers = Column (Integer(), default=0)
    business_passengers = Column (Integer(), default=0)
    vip_passengers = Column (Integer(), default=0)
    created_at = Column(DateTime(), default=datetime.utcnow)
    
    airplane = db.relationship('Airplanes', backref='flights', foreign_keys=[airplane_id])
