from fastapi import FastAPI, Form
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
import random
import sqlite3

from starlette.templating import Jinja2Templates


class LoginRequest(BaseModel):
    username: str
    password: str

class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: str

class ForgotPasswordRequest(BaseModel):
    username: str
    recovery_code: str

class Login:
    def __init__(self):
        self.create_connection()
        self.logged_in = False

    def create_connection(self):
        self.connection = sqlite3.connect("Members.db")
        self.cursor = self.connection.cursor()
        query = "CREATE TABLE IF NOT EXISTS Members (Username TEXT,Password TEXT,Email TEXT,Recovery_Code INT)"
        self.cursor.execute(query)
        self.connection.commit()

    def finish_connection(self):
        self.connection.close()

    def login(self, username: str, password: str) -> bool:
        connection = sqlite3.connect("Members.db")
        cursor = connection.cursor()
        query = "SELECT * FROM Members WHERE username = ? AND password = ?"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        connection.close()

        if result:
            self.logged_in = True
        else:
            self.logged_in = False

        return self.logged_in

    def is_logged_in(self) -> bool:
        return self.logged_in

    def create_account(self, username: str, password: str, email: str):
        connection = sqlite3.connect("Members.db")
        cursor = connection.cursor()
        query = "INSERT INTO Members VALUES (?,?,?,?)"
        recovery_code = random.randint(1000, 9999)
        cursor.execute(query, (username, password, email, recovery_code))
        connection.commit()
        connection.close()

    def forgot_password(self, username: str, recovery_code: str):
        recovery_code = str(random.randint(1000, 9999))

        connection = sqlite3.connect("Members.db")
        cursor = connection.cursor()
        query = "SELECT username, password, email, recovery_code FROM Members WHERE username = ? AND recovery_code = ?"
        cursor.execute(query, (username, recovery_code))
        result = cursor.fetchone()

        if result:
            # Reset the password or perform the necessary actions
            # based on the successful recovery code verification
            pass

        connection.close()


login = Login()
app = FastAPI()
templates = Jinja2Templates(directory="templates")


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

                .create-account-button {
                    display: block;
                    width: 100%;
                    padding: 10px;
                    background-color: #4287f5;
                    border: none;
                    color: #fff;
                    font-weight: bold;
                    cursor: pointer;
                    margin-top: 10px;
                    text-align: center;
                    text-decoration: none;
                    border-radius: 3px;
                }

                .create-account-button:hover {
                    background-color: #1e66d1;
                }
                .forgot-password-button {
                    display: block;
                    width: 100%;
                    padding: 10px;
                    background-color: #4287f5;
                    border: none;
                    color: #fff;
                    font-weight: bold;
                    cursor: pointer;
                    margin-top: 10px;
                    text-align: center;
                    text-decoration: none;
                    border-radius: 3px;
                }

                .forgot-password-button:hover {
                    background-color: #1e66d1;
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
            <a href="/create-account" class="create-account-button">Create Account</a>
            <a href="/forgot-password" class="forgot-password-button">Forgot Password</a>

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

@app.get("/dashboard", response_class=HTMLResponse)
def show_dashboard():
    return """
        <html>
        <head>
            <title>Library Dashboard</title>
        </head>
        <body>
            <h1>Welcome to the Library Dashboard!</h1>
            <!-- Dashboard content goes here -->
        </body>
        </html>
    """

@app.post("/login")
def login_user(request: LoginRequest):
    if login.login(request.username, request.password):
        return {"message": "Login successful!"}
    else:
        raise HTTPException(status_code=401, detail="Login failed!")

@app.get("/create-account", response_class=HTMLResponse)
def show_create_account_form():
    return """
        <html>
        <head>
            <title>Create Account</title>
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
                input[type="password"],
                input[type="email"] {
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

                .back-to-login-button {
                    display: block;
                    width: 100%;
                    padding: 10px;
                    background-color: #4287f5;
                    border: none;
                    color: #fff;
                    font-weight: bold;
                    cursor: pointer;
                    margin-top: 10px;
                    text-align: center;
                    text-decoration: none;
                    border-radius: 3px;
                }

                .back-to-login-button:hover {
                    background-color: #1e66d1;
                }
            </style>
        </head>
        <body>
            <h1>Create Account</h1>
            <form action="/create-account" method="post" onsubmit="event.preventDefault(); createAccount()">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required>
                <input type="submit" value="Create Account">
                <div id="error-message" class="error-message"></div>
            </form>
            <a href="/login" class="back-to-login-button">Back to Login</a>
            <script>
                function createAccount() {
                    const form = document.querySelector('form');
                    const formData = new FormData(form);
                    const data = Object.fromEntries(formData.entries());
                    fetch('/create-account', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(data),
                    })
                    .then(response => response.json())
                    .then(result => {
                        if (result.message === 'Account created!') {
                            window.location.href = '/account-creation';
                        } else {
                            const errorMessage = document.getElementById('error-message');
                            errorMessage.textContent = 'Account creation failed!';
                        }
                    })
                    .catch(error => console.error(error));
                }
            </script>
        </body>
        </html>
    """

@app.post("/create-account")
def create_account(request: CreateUserRequest):
    login.create_account(request.username, request.password, request.email)
    return {"message": "Account created!"}



@app.get("/forgot-password", response_class=HTMLResponse)
def show_forgot_password_form(request: ForgotPasswordRequest):
    return templates.TemplateResponse("forgot_password.html", {"request": request})
@app.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest):
    login.forgot_password(request.username, request.password, request.email)
    return {"message": "Forgot password action taken"}




















if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)






###borrow book retorn book


# class PasswordRecoveryRequest(BaseModel):
#     username: str
#     email: str
#
# @app.post("/password_recovery")
# def password_recovery(request: PasswordRecoveryRequest):
#     member = membership_and_Menu.Membership()
#     member.Recovery_Code(request.username, request.email)
#     return {"status": "success"}