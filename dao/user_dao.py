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

def update_user_by_username(db: Session, username: str, update_data: dict) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user_by_username(db: Session, username: str) -> bool:
    user = get_user_by_username(db, username)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True

def create_user(db:Session, db_user: dict) -> Optional[User]:
    user = User(**db_user)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user