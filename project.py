import time
from fastapi.exceptions import HTTPException
from typing import List
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class Login:
    def __init__(self):
        self.logged_in = False

    def login(self, username: str, password: str) -> bool:
        if username == "admin" and password == "password":
            self.logged_in = True
        else:
            self.logged_in = False
        return self.logged_in

    def is_logged_in(self) -> bool:
        return self.logged_in

login = Login()
app = FastAPI()

@app.get("/")
def home():
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse)
def show_login_form():
    return """
        <html>
        <head>
            <title>Library Login Page</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f2f2f2;
                    padding: 20px;
                }

                h1 {
                    text-align: center;
                    color: #333;
                }

                form {
                    max-width: 300px;
                    margin: 0 auto;
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 5px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }

                label {
                    display: block;
                    margin-bottom: 10px;
                    font-weight: bold;
                }

                input[type="text"],
                input[type="password"] {
                    width: 100%;
                    padding: 10px;
                    border: 1px solid #ccc;
                    border-radius: 3px;
                    margin-bottom: 20px;
                }

                input[type="submit"] {
                    width: 100%;
                    padding: 10px;
                    background-color: #4caf50;
                    border: none;
                    color: #fff;
                    font-weight: bold;
                    cursor: pointer;
                }

                input[type="submit"]:hover {
                    background-color: #45a049;
                }

                .error-message {
                    color: red;
                    margin-top: 10px;
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <h1>Library Login</h1>
            <form action="/login" method="post" onsubmit="event.preventDefault(); login()">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
                <input type="submit" value="Log In">
                <div id="error-message" class="error-message"></div>
            </form>
            <script>
                function login() {
                    const form = document.querySelector('form');
                    const formData = new FormData(form);
                    const data = Object.fromEntries(formData.entries());
                    fetch('/login', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(data),
                    })
                    .then(response => response.json())
                    .then(result => {
                        if (result.message === 'Login successful!') {
                            window.location.href = '/dashboard';
                        } else {
                            const errorMessage = document.getElementById('error-message');
                            errorMessage.textContent = 'Login failed!';
                        }
                    })
                    .catch(error => console.error(error));
                }
            </script>
        </body>
        </html>
    """

@app.post("/login")
def login_user(request: LoginRequest, csrf=False):
    if login.login(request.username, request.password):
        return {"message": "Login successful!"}
    else:
        raise HTTPException(status_code=401, detail="Login failed!")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)





#
# class AccountCreateRequest(BaseModel):
#     username: str
#     password: str
#     email: str
#
#
# class PasswordRecoveryRequest(BaseModel):
#     username: str
#     email: str
#
# @app.post("/create_account")
# def create_account(request: AccountCreateRequest):
#     member = membership_and_Menu.Membership()
#     member.Create_Account(request.username, request.password, request.email)
#     return {"status": "success"}
#
#
# @app.post("/password_recovery")
# def password_recovery(request: PasswordRecoveryRequest):
#     member = membership_and_Menu.Membership()
#     member.Recovery_Code(request.username, request.email)
#     return {"status": "success"}