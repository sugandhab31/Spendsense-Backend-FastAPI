import utils.auth as auth
import models.basemodels as basemodels
from App import db_dependency
from fastapi import Request, APIRouter, HTTPException, status, Request
from datetime import timedelta, datetime

router = APIRouter()

@router.post('/createuser/')
def createuser(user_from_UI: basemodels.UserBase, db: db_dependency):
    try:
        hashed_password = auth.get_password_hash(user_from_UI.password)
        result = auth.adduser(user_from_UI, hashed_password, db)
        return result
    except Exception as e:
        return e
    

@router.post("/login") #response_model=basemodels.Token
async def create_session(db: db_dependency ,request: Request):
    query_params = dict(request.query_params)
    user_details = auth.get_user(query_params('username'), query_params('password'), db)
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
                    'subject': query_params('username')
                },
                expires_delta = access_token_expires
            )
            auth.update_user_token(userid=query_params('username'), token=access_token, expiry_timestamp=datetime.now()+access_token_expires, db=db)
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
