from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from datetime import datetime
from typing import Annotated
import models
from database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
import auth
import uvicorn

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

class UserBase(BaseModel):
    username: str
    password: str
    fullname: str
    diabled: bool

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
        return e

@app.post('/createuser/')
def createuser(user_from_UI: UserBase, db: db_dependency):
    try:
        hashed_password = auth.get_password_hash(user_from_UI.password)
        result = auth.adduser(user_from_UI, hashed_password, db)
        return result
    except Exception as e:
        return e
    


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)