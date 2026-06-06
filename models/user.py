from extensions import db
from sqlalchemy import Integer, String, DateTime, Column, Boolean
from flask_login import UserMixin
from datetime import datetime

class Users(db.Model, UserMixin):
    id = Column (Integer(), primary_key= True)
    full_name = Column (String(110))
    national_code = Column (Integer, unique=True)
    phone = Column (Integer(), unique=True)
    wallet = Column (Integer(), default=0)
    admin = Column (Boolean, default=False)
    created_at = Column(DateTime(), default=datetime.utcnow)
