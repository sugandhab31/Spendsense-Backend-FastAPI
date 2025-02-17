from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Annotated
from passlib.context import CryptContext
from database import get_db, engine, SessionLocal
from sqlalchemy.orm import Session
from models import User

SECRET_KEY = "secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MINUTES = 30

#--pydantinc models--

class Token(BaseModel): #Define the structure of the token response.
    access_token: str
    token_type: str

class TokenData(BaseModel): #Represents the data extracted from a decoded JWT.
    username: Optional[str] = None

class User_Model(BaseModel): #Define the public user model (information that you can share with clients).
    username: str
    fullname: Optional[str] = None
    diabled: Optional[bool] = None

class UserInDB(User): #Extend the public user model with the hashed password field, which is stored internally in the database.
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")    #Create a CryptContext that uses the bcrypt algorithm to hash and verify passwords.
db_dependency = Annotated(Session, Depends(get_db))


def get_user(username: str, user_password: str, db):
    try:
        user_details = db.query(User).filter(User.username == username).first()
        if not user_details:
            return {
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'User not found.'
            }
        else:
            db_hashed_password = user_details('hashed_password')
            password_validated = verify_password(password = user_password, hashed_password = db_hashed_password)
            if password_validated('status') == 200:
                return {
                    'status': status.HTTP_200_OK,
                    'message': 'User verified.'                 
                }

    except Exception as e:
        return {
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': 'Internal error occured.'
        }

def verify_password(password: str, hashed_password: str, db):
    try:
        result = pwd_context.verify(password, hashed_password)
        if not result:
            return {
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Invalid Password.'
            }
        else:
            return {
                'status': status.HTTP_200_OK,
                'message': 'Valid Password.'
            }
    except Exception as e:
        return {
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': 'Internal error occured.'
        }

def adduser(user: User_Model, hashed_password_from_user: str, db):
    try:
        db_user = User(
        username = user.username,
        fullname = user.fullname,
        hashed_password = hashed_password_from_user,
        disabled = False
        )
        db.add(db_user)
        db.commit()
        return {
            'status': status.HTTP_201_CREATED,
            'message': 'New User Created'
        }
    except Exception as e:
        return {
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': 'Internal error occured.'
        }
    
def get_password_hash(password: str):
    return pwd_context.hash(password)