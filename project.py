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
            <title>Login Page</title>
        </head>
        <body>
            <h1>Login</h1>
            <form action="/login" method="post" onsubmit="event.preventDefault(); login()">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required><br>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required><br>
                <input type="submit" value="Log In">
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
                            alert('Login failed!');
                        }
                    })
                    .catch(error => console.error(error));
                }
            </script>
        </body>
        </html>
    """

@app.post("/login")
def login_user(request: LoginRequest):
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