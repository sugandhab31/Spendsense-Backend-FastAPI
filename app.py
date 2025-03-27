from fastapi import FastAPI, HTTPException, Depends, status, Request
from pydantic import BaseModel
from datetime import timedelta, datetime
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
    
'''
{
  "username": "string",
  "password": "string",
  "repeat_password": "string",
  "fullname": "string",
  "disbled": true
}
'''
    
@app.post("/login") #response_model=basemodels.Token
async def create_session(db: db_dependency ,form_data: auth.OAuth2PasswordRequestForm = Depends()):
    user_details = auth.get_user(form_data.username, form_data.password, db)
    if user_details['body'] is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers = {
                "WWW-Authenticate":"Bearer"
            }
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRY_MINUTES)
    try:
        isactive = auth.check_active_session(user_details=user_details)
        if isactive:
            auth.update_token_expiry(userid=user_details['body'].user_id, expiry_timestamp=datetime.now()+access_token_expires, db=db)
            return {
                'status': status.HTTP_200_OK,
                'error': None,
                'body': "Session is Active."
            }
        else:
            access_token = auth.create_access_token(
                data = {
                    'subject': form_data.username
                },
                expires_delta = access_token_expires
            )
            auth.update_user_token(userid=form_data.username, token=access_token, expiry_timestamp=datetime.now()+access_token_expires, db=db)
            return {
                'status': status.HTTP_200_OK,
                'body':{
                    'access_token': access_token,
                    'token_type': "jwt bearer"
                },
                'error': None
            }
    except Exception as e:
        return {
                'status': status.HTTP_401_UNAUTHORIZED,
                'error': e,
                'body': None
            }
    
@app.get("/getexpenses/")
def getexpenses():
    pass
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)