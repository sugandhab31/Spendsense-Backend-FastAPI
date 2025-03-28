from fastapi import status
from passlib.context import CryptContext
import models.basemodels as basemodels
from models.models import User
from typing import Optional
from datetime import timedelta, datetime
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from dao import user_dao 

SECRET_KEY = "secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MINUTES = 10

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")    #Create a CryptContext that uses the bcrypt algorithm to hash and verify passwords.

def get_user(username: str, user_password: str, db):
    try:
        user_details = user_dao.get_user_by_username(db=db, username=username)
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
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
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
            'error': e,
            'body': None
        }

def check_active_session(userid, token_from_header, db):
    try:
        scheme, token = token_from_header.split()
        # payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # return payload
        user = db.query(User).filter(User.username == userid).first()
        expiry_timestamp = user.expiry_timestamp
        if expiry_timestamp is None:
            return False
        if user.session_token == token:
            if expiry_timestamp <= (datetime.now()+timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)):
                return True
            else:
                return False
        else:
            return {
                'status': status.HTTP_401_UNAUTHORIZED,
                 'error': 'Invalid Token',
                 'body': None
            }
    except Exception as e:
        return {
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'error': e,
            'body': None
        }

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
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'error': e,
            'body': None
        }
