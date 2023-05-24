import time
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

import membership_and_Menu

app = FastAPI()
 

class LoginRequest(BaseModel):
    username: str
    password: str


class AccountCreateRequest(BaseModel):
    username: str
    password: str
    email: str


class PasswordRecoveryRequest(BaseModel):
    username: str
    email: str


@app.post("/login")
def login(request: LoginRequest):
    member = membership_and_Menu.Membership()
    result = member.Login_Account(request.username, request.password)
    return {"status": result}


@app.post("/create_account")
def create_account(request: AccountCreateRequest):
    member = membership_and_Menu.Membership()
    member.Create_Account(request.username, request.password, request.email)
    return {"status": "success"}


@app.post("/password_recovery")
def password_recovery(request: PasswordRecoveryRequest):
    member = membership_and_Menu.Membership()
    member.Recovery_Code(request.username, request.email)
    return {"status": "success"}


if __name__ == "__main__":
    print("""
    ***************************************************** 
                                                        *
          WELCOME TO THE LIBRARY APPLICATION LOGIN      *
                                                        *
    1.) Login your account                              *    
                                                        *
    2.) Create a new account                            *
                                                        *
    3.) Forget my password                              *
                                                        *
                                                        *
        press 'q' for exit                              *    
                                                        *
                                                        *
    *****************************************************
    """)

    while True:
        action = input("Select your action you want to do: ")
        if action == "q":
            print("The Application is closing...")
            time.sleep(4)
            print("the Application is closed....")
            break

        elif action == "1":
            username = input("please enter your username:")
            password = input("please enter your password:")
            login_request = LoginRequest(username=username, password=password)
            login_result = login(login_request)
            print(login_result)

        elif action == "2":
            print("Welcome new member! Please enter your information")
            time.sleep(3)
            username = input("Enter your username:")
            password = input("Enter your password:")
            email = input("Enter your email:")
            account_create_request = AccountCreateRequest(username=username, password=password, email=email)
            create_account(account_create_request)
            print("Your information saved successfully. Welcome again")

        elif action == "3":
            username = input("Please enter your username:")
            email = input("Please enter your email:")
            password_recovery_request = PasswordRecoveryRequest(username=username, email=email)
            password_recovery(password_recovery_request)
            print("A password recovery code has been sent to your email. Please check your email")

        else:
            print("You select an invalid action! Please enter a correct action")
