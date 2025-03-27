from pydantic import BaseModel, ValidationError, BeforeValidator, AfterValidator, model_validator
from typing import Optional, Annotated
import models.models as models
import re
from typing_extensions import Self

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
    repeat_password: str
    fullname: str
    disbled: bool

    # @model_validator(mode='after')
    # def validate_password_format(self) -> Self:
    #     match = re.match('/^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/', self.password)
    #     if match is None:
    #         raise ValueError("Password must contain a lowercase, uppercase, symbol(?=.*?[#?!@$%^&*-) and number (0-9).")
    #     return self
    
    @model_validator(mode='after')
    def check_password_match(self) -> Self:
        if self.password != self.repeat_password:
            raise ValidationError("Passwords do not match")
        return self
    
    @model_validator(mode='before')
    def check_username_password(self) -> Self:
        if self['password'].lower == self['username'].lower:
            raise ValueError('Username and Password cannot be same')
        return self

class Token(BaseModel): #Define the structure of the token response.
    access_token: str
    token_type: str

class TokenData(BaseModel): #Represents the data extracted from a decoded JWT.
    username: Optional[str] = None

class UserInDB(models.User): #Extend the public user model with the hashed password field, which is stored internally in the database.
    hashed_password: str