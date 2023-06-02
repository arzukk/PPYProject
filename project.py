import sqlite3
import random
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, HTTPException, Form
from pydantic import BaseModel, Field
from fastapi import Request
import traceback


class LoginRequest(BaseModel):
    username: str
    password: str

class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: str

class QueryBookRequest(BaseModel):
    book_name: str = Field(..., min_length=1)

class DeleteBookRequest(BaseModel):
    book_name: str = Field(..., min_length=1)

class AddBookRequest(BaseModel):
    name: str = Field(..., description="Name of the book", max_length=100)
    writer: str = Field(..., description="Writer of the book", max_length=100)
    publisher: str = Field(..., description="Publisher of the book", max_length=100)
    type: str = Field(..., description="Type/genre of the book", max_length=100)
    number_of_page: int = Field(..., description="Number of pages in the book")
    edition: int = Field(..., description="Edition of the book")

class CreateDashboardRequest(BaseModel):
    pass

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
        query = "SELECT * FROM Members WHERE username = ? AND password = ?"
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()

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

    def delete_account(self, request: LoginRequest):
        query = "DELETE FROM Members WHERE Username = ? AND Password = ?"
        self.cursor.execute(query, (request.username, request.password))
        self.connection.commit()

    def check_account_exists(self, username: str) -> bool:
        query = "SELECT * FROM Members WHERE Username = ?"
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        return result is not None

class Library:
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.connection = sqlite3.connect("Books.db")
        self.cursor = self.connection.cursor()
        query = "CREATE TABLE IF NOT EXISTS Books (Name TEXT, Writer TEXT, Publisher TEXT, Type TEXT, Number INT, Edition INT, Borrowed INT DEFAULT 0, Deadline TEXT DEFAULT NULL)"
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

    def delete_book(self, book_name: str):
        connection = sqlite3.connect("Books.db")
        cursor = connection.cursor()
        query = "DELETE FROM Books WHERE Name = ?"
        cursor.execute(query, (book_name,))
        connection.commit()
        connection.close()

    def add_book(self, name: str, writer: str, publisher: str, type: str, number: int, edition: int):
        connection = sqlite3.connect("Books.db")
        cursor = connection.cursor()
        query = "INSERT INTO Books (Name, Writer, Publisher, Type, Number, Edition) VALUES (?,?,?,?,?,?)"
        cursor.execute(query, (name, writer, publisher, type, number, edition))
        connection.commit()
        connection.close()

app = FastAPI()
templates = Jinja2Templates(directory="/Users/arzukilic/PycharmProjects/PPYProject/templates")

login = Login()
library = Library()

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
def show_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.post("/login", response_class=RedirectResponse)
async def login_user(request: LoginRequest):
    if login.login(request.username, request.password):
        library.logged_in = True  # Update the library instance's logged_in attribute
        return RedirectResponse(url="/dashboard", status_code=303)
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

@app.get("/delete-account")
def show_delete_account_form(request: Request):
    return templates.TemplateResponse("deleteAccount.html", {"request": request})

@app.post("/delete-account")
async def delete_account(request: LoginRequest):
    login.delete_account(request)
    return {"message": "Account deleted successfully!"}
    raise HTTPException(status_code=404, detail="Account not found!")


@app.get("/show-books", response_class=HTMLResponse)
def show_books(request: Request):
    books = library.get_all_books()
    return templates.TemplateResponse("showBooks.html", {"request": request, "books": books})

@app.get("/query-book", response_class=HTMLResponse)
def show_query_book_form(request: Request):
    return templates.TemplateResponse("queryBook.html", {"request": request})

@app.post("/query-book", response_class=HTMLResponse)
def query_book(request: QueryBookRequest):
    book_name = request.book_name
    books = library.query_book(book_name)
    if books:
        return templates.TemplateResponse("queryBookResult.html", {"request": request, "books": books})
    else:
        return templates.TemplateResponse("queryBookResult.html", {"request": request, "message": "No books found with the given name."})


@app.get("/add-book", response_class=HTMLResponse)
def show_add_book_form(request: Request):
    if not library.logged_in:
        raise HTTPException(status_code=400, detail="You are not logged in.")
    return templates.TemplateResponse("add_book.html", {"request": request})


@app.post("/add-book")
async def add_book(request: Request):
    try:
        form_data = await request.form()
        library.add_book(
            form_data["name"],
            form_data["writer"],
            form_data["publisher"],
            form_data["type"],
            int(form_data["number_of_page"]),
            int(form_data["edition"])
        )
        return RedirectResponse("/dashboard", status_code=303)
    except Exception as e:
        traceback.print_exc()  # Print the traceback for debugging
        raise HTTPException(status_code=500, detail="Failed to add book")


@app.get("/delete-book", response_class=HTMLResponse)
def show_delete_book_form(request: Request):
    return templates.TemplateResponse("delete_book.html", {"request": request})


@app.post("/delete-book", response_class=HTMLResponse)
async def delete_book(request: Request):
    try:
        form_data = await request.form()
        book_name = form_data["book_name"]
        books = library.query_book(book_name)

        if books:
            library.delete_book(book_name)
            return templates.TemplateResponse("delete_book.html",
                                              {"request": request, "message": "Book deleted successfully."})
        else:
            return templates.TemplateResponse("delete_book.html",
                                              {"request": request, "message": "No such book exists."})
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to delete book")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
