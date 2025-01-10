import re
from datetime import datetime
from typing import Optional

from anyio.abc import value
from pydantic import BaseModel, Field, field_validator

from utils.utils import ResponseModel


class User(BaseModel):
    name:str = Field('John',min_length=3)
    date_of_birth:str = Field('01/01/1990')
    country:str = Field('India',min_length=3)
    phone_number:str = Field('9876543210',min_length=10)
    # email:Optional[str]= None
    # password:Optional[str]=None
    # is_verified:Optional[bool] = False
    # created_at:Optional[datetime]= datetime.now()


    @field_validator('date_of_birth')
    @classmethod
    def check_date_of_birth(cls,value):
        try:
            # Try to parse the date using the 'DD/MM/YYYY' format
            parsed_date = datetime.strptime(value, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Date of birth must be in DD/MM/YYYY format")
        return parsed_date.strftime("%d/%m/%Y")

    @field_validator('phone_number')
    @classmethod
    def validate(cls,value):
        expression = r'[0-9]{10}'
        result = re.match(expression,value)
        if not result:
            raise ValueError('Phone number must be in digits only')
        return value


class UserRequestModel(User):
    account_number:str = ""

class UserResponse(User):
    account_number:str

class UserResponseModel(ResponseModel):
    data:UserResponse
    message:Optional[str]=""

class DepositRequest(BaseModel):
    account_number:str = Field('1234567890')
    user_id:int
    amount:int

    @field_validator('account_number')
    @classmethod
    def check_account_number(cls,value):
        expression = r'^[0-9]'
        if not re.match(expression,value):
            raise ValueError('Please enter account number in digits only')
        return value