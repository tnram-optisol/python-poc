from fastapi import APIRouter, status, HTTPException

from bank import BankAccount
from models.user_model import User, UserResponseModel, DepositRequest
from utils.utils import response_model, response_with_message

user_route = APIRouter(prefix='/user',tags=['User'])

@user_route.post('/create',response_model=UserResponseModel,status_code=status.HTTP_201_CREATED)
async def create_user(user:User):
    bank_account = BankAccount()
    data = await bank_account.create_user_account(user)
    return response_with_message(status.HTTP_201_CREATED,data,'Please make a deposit to start your account')

@user_route.post('/add-deposit',status_code=status.HTTP_201_CREATED)
async  def add_deposit(data:DepositRequest):
   try:
       bank_account = BankAccount()
       response = bank_account.add_deposit_to_account(data.account_number, data.amount, data.user_id)
       print(response)
       return response_model(status_code=status.HTTP_201_CREATED, response=response)
   except Exception as e:
       print(e)