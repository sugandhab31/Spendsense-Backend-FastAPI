from sqlalchemy import Boolean, Integer, Column, ForeignKey, String, Index, DateTime
from database import Base

class expenses(Base):
    __tablename__ = 'expenses'

    expense_id = Column(Integer, primary_key = True, index = True)
    expense_name = Column(String)
    expense_amount = Column(Integer)
    expemse_currency = Column(String)
    expense_category_id = Column(Integer)
    expense_date = Column(DateTime, server_default=("NOW()"))

class category(Base):
    __tablename__ = 'category'

    category_id = Column(Integer, ForeignKey, primary_key = True, index = True)
    category_name = Column(String)
    sub_category = Column(String)
