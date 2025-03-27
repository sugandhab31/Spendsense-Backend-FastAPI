from sqlalchemy.orm import Session
from typing import List, Optional
from models import User

def get_users(db: Session) -> List[User]:
    return db.query(User).all()

def get_user_by_id(db: Session, userid: str) -> Optional[User]:
    #Optional[User] is a type hint indicating that the value can be either an instance of User or None. It's essentially a shorthand for Union[User, None].
    return db.query(User).filter(User.userid == userid).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

