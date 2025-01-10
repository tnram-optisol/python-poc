from pydantic import BaseModel
from typing import  Any


class ResponseModel(BaseModel):
    status_code:int
    data:Any

class ResponseModelMessage(ResponseModel):
    message:str

def response_model(status_code:int,response):
    return ResponseModel(status_code=status_code,data=response)

def response_with_message(status_code:int,response:Any,message:str):
    return ResponseModelMessage(status_code=status_code,data=response,message=message)