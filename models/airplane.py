from extensions import db
from sqlalchemy import Integer, String, DateTime, Boolean, Column, ForeignKey
from datetime import datetime

class Airplanes(db.Model):
    id = Column (Integer, primary_key= True)
    name = Column(String(110), unique=True)
    capacity_economy = Column(Integer())
    capacity_business = Column(Integer())
    capacity_vip = Column(Integer())
    created_at = Column(DateTime(), default=datetime.utcnow)

