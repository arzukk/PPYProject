import sqlite3
import random
from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str
    password: str

class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: str

class CreateDashboardRequest(BaseModel):
    pass

class QueryBookRequest(BaseModel):
    book_name: str = Field(..., min_length=1)

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


class BookDatabase:
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.connection = sqlite3.connect("Books.db")
        self.cursor = self.connection.cursor()
        query = "CREATE TABLE IF NOT EXISTS Books (Name TEXT,Writer TEXT,Publisher TEXT,Type TEXT,Number_of_Pages INT,Edition INT)"
        self.cursor.execute(query)
        self.connection.commit()

    def finish_connection(self):
        self.connection.close()

    def get_all_books(self):
        connection = sqlite3.connect("Books.db")
        cursor = connection.cursor()
        query = "SELECT * FROM Books"
        cursor.execute(query)
        result = cursor.fetchall()
        connection.close()
        return result

    def query_book(self, book_name: str):
        connection = sqlite3.connect("Books.db")
        cursor = connection.cursor()
        query = "SELECT * FROM Books WHERE Name = ?"
        cursor.execute(query, (book_name,))
        result = cursor.fetchall()
        connection.close()
        return result


login = Login()
book_db = BookDatabase()
app = FastAPI()
templates = Jinja2Templates(directory="C:\\Users\\ENES CATAL\\Downloads\\PPYProject-arzununki\\PPYProject-arzununki\\templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
def show_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request, "logged_in": login.is_logged_in()})

@app.post("/login")
def login_user(request: LoginRequest):
    if login.login(request.username, request.password):
        return {"message": "Login successful!"}
    else:
        raise HTTPException(status_code=401, detail="Login failed!")

@app.post("/dashboard")
def show_dashboard(request: CreateDashboardRequest):
    return RedirectResponse(url="/dashboard")

@app.get("/create-account")
def show_create_account_form(request: Request):
    return templates.TemplateResponse("createAccount.html", {"request": request})

@app.post("/create-account")
def create_account(request: CreateUserRequest):
    login.create_account(request.username, request.password, request.email)
    return {"message": "Account created!"}

@app.get("/show-books", response_class=HTMLResponse)
def show_books(request: Request):
    books = book_db.get_all_books()
    return templates.TemplateResponse("showBooks.html", {"request": request, "books": books})

@app.get("/query-book", response_class=HTMLResponse)
def show_query_book_form(request: Request):
    return templates.TemplateResponse("queryBook.html", {"request": request})

@app.post("/query-book", response_class=HTMLResponse)
def query_book(request: QueryBookRequest):
    book_name = request.book_name
    books = book_db.query_book(book_name)
    if books:
        return templates.TemplateResponse("queryBookResult.html", {"request": request, "books": books})
    else:
        return templates.TemplateResponse("queryBookResult.html", {"request": request, "message": "No books found with the given name."})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
