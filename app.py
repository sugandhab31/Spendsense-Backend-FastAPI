from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from typing import Annotated
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()

class ExpensesBase(BaseModel):
    expense_id = int,
    expense_name = str,
    expense_amount = int,
    expense_currency = str,
    expense_category_id = int,
    expense_date = datetime, 

class CategoryBase(BaseModel):
    category_id = int,
    category_name = str,
    custom_category = bool

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated(Session, db = Depends(get_db))

@app.post('/addexpense/')
def addexpense(expenses = ExpensesBase, db = db_dependency):
    db_expense = models.expenses(
        expense_id = expenses.expense_id,
        expense_name = expenses.expense_name,
        expense_amount = expenses.expense_amount,
        expense_currency = expenses.expense_currency,
        expense_category_id = expenses.expense_category_id,
        expense_date = expenses.expense_date
        )
    db.add(db_expense)
    db.commit()

