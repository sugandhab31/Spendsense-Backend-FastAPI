from fastapi import FastAPI, Depends, HTTPException, status
import json
from passlib.context import CryptContext
from utils.database import get_db, engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import update
import App
import models.basemodels as basemodels
from models.models import User
from typing import Optional
from datetime import timedelta, datetime
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


SECRET_KEY = "secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MINUTES = 10

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")    #Create a CryptContext that uses the bcrypt algorithm to hash and verify passwords.

def get_user(username: str, user_password: str, db):
    try:
        user_details = db.query(User).filter(User.username == username).first()
        if not user_details:
            return {
                'status': status.HTTP_404_NOT_FOUND,
                'error': 'User not found.',
                'body': None
            }
        else:
            db_hashed_password = user_details.hashed_password
            password_validated = verify_password(password = user_password, hashed_password = db_hashed_password, db = db)
            if password_validated['status'] == 200:
                return {
                    'status': status.HTTP_200_OK,
                    'error': None,
                    'body': user_details
            }

    except Exception as e:
        return {
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': 'Internal error occured. User could not be retrieved.',
            'body': None
        }

def verify_password(password: str, hashed_password: str, db):
    try:
        result = pwd_context.verify(password, hashed_password)
        if not result:
            return {
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Invalid Password.',
                'body': None                
            }
        else:
            return {
                'status': status.HTTP_200_OK,
                'message': 'Valid Password.',
                'body': None
            }
    except Exception as e:
        return {
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': 'Internal error occured. Password could not be verified.',
            'body': None
        }

def adduser(user: basemodels.UserBase, hashed_password_from_user: str, db):
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
            'message': 'New User Created',
            'body': None
        }
    except Exception as e:
        return {
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': 'Internal error occured. User could not be created.',
            'body': None
        }
    
def get_password_hash(password: str):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    try: 
        to_encode = data.copy()
        # expire = datetime.now() + (expires_delta or timedelta(minutes=15))
        # to_encode.update({
        #     "expiry": expire
        # })
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encode_jwt
    except Exception as e:
        return e
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def update_user_token(userid, token, expiry_timestamp,db):
    try:
        user = db.query(User).filter(User.username == userid).update({
            "session_token": token, "expiry_timestamp": expiry_timestamp
        })
        db.commit()
        if user:
            return {
                'status': status.HTTP_201_CREATED,
                'error': None,
                'body': 'Session Token Updated'
            }
    except Exception as e:
        return {
            'status': status.HTTP_502_BAD_GATEWAY,
            'error': e,
            'body': None
        }
    

def validate_user_exists(userid, db):
    try:
        user_details = db.query(User).filter(User.username == userid).first()
        if not user_details:
            return {
                'status': status.HTTP_404_NOT_FOUND,
                'error': 'User not found.',
                'body': None
            }
        else:
            return {
                    'status': status.HTTP_200_OK,
                    'error': None,
                    'body': user_details
            }

    except Exception as e:
        return {
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': 'Internal error occured. User could not be retrieved.',
            'body': None
        }

def check_active_session(user_details):
    try:
        if user_details['body'].expiry_timestamp <= (datetime.now()+timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)):
            return True
        else:
            return False
    except Exception as e:
        return e

def update_token_expiry(userid, expiry_timestamp,db):
    try:
        user = db.query(User).filter(User.username == userid).update({
            "expiry_timestamp": expiry_timestamp
        })
        db.commit()
        if user:
            return {
                'status': status.HTTP_200_OK,
                'error': None,
                'body': 'Session Expiry Updated'
            }
    except Exception as e:
        return {
            'status': status.HTTP_502_BAD_GATEWAY,
            'error': e,
            'body': None
        }
    
def verify_token(userid, token_from_header, db):
    try:
        user = db.query(User).filter(User.username == userid).first()
        # issessionactive = get_user(userid)
        if user.session_token == token_from_header and check_active_session(user):
            return {
                'status': status.HTTP_200_OK,
                'error': None,
                'body': 'Token is valid'
            }
        else:
            return {
                'status': status.HTTP_401_UNAUTHORIZED,
                'error': 'Invalid Token',
                'body': None
        }
    except Exception as e:
        return {
            'status': status.HTTP_502_BAD_GATEWAY,
            'error': e,
            'body': None
        }
