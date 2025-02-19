from sqlalchemy import Boolean, Integer, Column, ForeignKey, String, Numeric, DateTime
from database import Base
from datetime import datetime
import uuid

class expenses(Base):
    __tablename__ = 'expenses'

    expense_id = Column(String, primary_key = True, default=lambda: str(uuid.uuid4()))
    expense_name = Column(String, nullable = False)
    expense_amount = Column(Numeric(10,2), nullable = False)
    expense_currency = Column(String, nullable = False)
    expense_category_id = Column(Integer, nullable = False)
    expense_date = Column(DateTime, default = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

class category(Base):
    __tablename__ = 'category'

    category_id = Column(Integer, primary_key = True, index = True)
    category_name = Column(String)
    custom_category = Column(Boolean)


class User(Base):
    __tablename__ = 'users'

    username = Column(String, primary_key = True)
    hashed_password = Column(String)
    fullname = Column(String)
    disabled = Column(Boolean)