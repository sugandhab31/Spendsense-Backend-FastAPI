from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from datetime import timedelta
from typing import Annotated
import models
from database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
import auth
import uvicorn
import basemodels

app = FastAPI()
models.Base.metadata.create_all(bind = engine)

# This base class contains a metadata attribute (Base.metadata), which collects information about all the tables and models defined.
# You use Base.metadata.create_all(engine) to create all tables in the database according to the defined models.

db_dependency = Annotated[Session, Depends(get_db)]

@app.post('/addexpense/')
def addexpense(expenses: basemodels.ExpensesBase, db: db_dependency):
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
def createuser(user_from_UI: basemodels.UserBase, db: db_dependency):
    try:
        hashed_password = auth.get_password_hash(user_from_UI.password)
        result = auth.adduser(user_from_UI, hashed_password, db)
        return result
    except Exception as e:
        return e
    
@app.post("/token", response_model=basemodels.Token)
async def login_for_access_token(db: db_dependency ,form_data: auth.OAuth2PasswordRequestForm = Depends()):
    user_details = auth.get_user(form_data.username, form_data.password, db)
    if user_details.body is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers = {
                "WWW-Authenticate":"Bearer"
            }
        )
    try:
        access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRY_MINUTES)
        access_token = auth.create_access_token(
            data = {
                'subject': user_details.username
            },
            expires_delta = access_token_expires
        )

        return {
            'status': status.HTTP_200_OK,
            'body':{
                "access_token": access_token,
                "token_type": "bearer"
            },
            'error': None
        }
    except Exception as e:
        return {
                'status': status.HTTP_401_UNAUTHORIZED,
                'error': 'Unable to generate token',
                'body': None
            }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)