import random

from models.user_model import UserRequestModel

from db import Database


class BankAccount:
    __database_obj:Database
    def __init__(self):
        try:
            self.__database_obj = Database()
        except Exception as e:
            print(e)


    async def create_user_account(self,user:UserRequestModel):
        self.__database_obj = Database()
        result = self.__database_obj.add_user_transaction(user.__dict__)
        return  result[0]

    # def get_user(self):
    #     return  self.user


    def add_deposit_to_account(self,account_number,amount,id):
        try:
            result = self.__database_obj.add_deposit(account_number, amount)
            print(result)
            if result:
                response = {
                    "data": f'You have deposited {amount} in your account {account_number}'
                }
                return  response
        except Exception as e:
            raise e
