from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from typing import Annotated
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind = engine)

class ExpensesBase(BaseModel):
    expense_name: str
    expense_amount: int
    expense_currency: str
    expense_category_id: int

class CategoryBase(BaseModel):
    category_id: int
    category_name: str
    custom_category: bool

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post('/addexpense/')
def addexpense(expenses: ExpensesBase, db: db_dependency):
    try:
        db_expense = models.expenses(
            expense_name = expenses.expense_name,
            expense_amount = expenses.expense_amount,
            expense_currency = expenses.expense_currency,
            expense_category_id = expenses.expense_category_id,
            )
        db.add(db_expense)
        db.commit()
    except Exception as e:
        print(e)
    
