import sqlite3
import random
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, HTTPException, Form
from pydantic import BaseModel, Field
from fastapi import Request
import traceback
from datetime import datetime, timedelta, date
import logging



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

class UpdateBookEditionRequest(BaseModel):
    book_name: str = Field(..., min_length=1)
    new_edition: int

class AddBookRequest(BaseModel):
    name: str = Field(..., description="Name of the book", max_length=100)
    writer: str = Field(..., description="Writer of the book", max_length=100)
    publisher: str = Field(..., description="Publisher of the book", max_length=100)
    type: str = Field(..., description="Type/genre of the book", max_length=100)
    number_of_page: int = Field(..., description="Number of pages in the book")
    edition: int = Field(..., description="Edition of the book")

class CreateDashboardRequest(BaseModel):
    pass

class ResetPasswordRequest(BaseModel):
    username: str
    recovery_code: str
    new_password: str

class BorrowBookRequest(BaseModel):
    book_number: int
    desired_date: date

class AccountSettingsRequest(BaseModel):
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

    def reset_password(recovery_code, username, new_password):
        conn = sqlite3.connect('Members.db')
        cursor = conn.cursor()

        # Query the user by recovery code and username
        query = "SELECT * FROM users WHERE recovery_code=? AND username=?"
        cursor.execute(query, (recovery_code, username))
        user = cursor.fetchone()

        if user is not None:
            # Update the user's password
            update_query = "UPDATE users SET password=? WHERE recovery_code=? AND username=?"
            cursor.execute(update_query, (new_password, recovery_code, username))
            conn.commit()
            conn.close()
            return {"message": "Password reset successful"}
        else:
            conn.close()
            return {"message": "Invalid recovery code or username"}

        ##account settings

    def update_username(self, old_username: str, new_username: str):
        query = "UPDATE Members SET Username = ? WHERE Username = ?"
        self.cursor.execute(query, (new_username, old_username))
        self.connection.commit()
        self.username = new_username

    def update_password(self, username: str, new_password: str):
        query = "UPDATE Members SET Password = ? WHERE Username = ?"
        self.cursor.execute(query, (new_password, username))
        self.connection.commit()



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

    def update_book_edition(self, book_name: str, new_edition: int):
        connection = sqlite3.connect("Books.db")
        cursor = connection.cursor()
        query = "UPDATE Books SET Edition = ? WHERE Name = ?"
        cursor.execute(query, (new_edition, book_name))
        connection.commit()
        connection.close()

    def add_book(self, name: str, writer: str, publisher: str, type: str, number: int, edition: int):
        connection = sqlite3.connect("Books.db")
        cursor = connection.cursor()
        query = "INSERT INTO Books (Name, Writer, Publisher, Type, Number, Edition) VALUES (?,?,?,?,?,?)"
        cursor.execute(query, (name, writer, publisher, type, number, edition))
        connection.commit()
        connection.close()

        #################################

    def borrow_book(self, borrow_request):
        book_number = borrow_request.book_number
        desired_date = borrow_request.desired_date

        # Check if book exists
        query = "SELECT * FROM Books WHERE Number = ?"
        self.cursor.execute(query, (book_number,))
        book = self.cursor.fetchone()
        if book is None:
            return "Book not found"

        if book[6] == 1:
            deadline = self.get_borrowed_deadline(book_number)
            if deadline == "Book not found":
                return "Book is already borrowed"
            else:
                return "Book is already borrowed. Deadline: " + deadline

        borrowing_date = desired_date.isoformat()
        deadline = (desired_date + timedelta(days=15)).isoformat()

        query = "UPDATE Books SET Borrowed = 1, Deadline = ? WHERE Number = ?"
        self.cursor.execute(query, (deadline, book_number))
        self.connection.commit()

        return "Book borrowed successfully"

    def get_book_status(self, book_number):
        query = "SELECT * FROM Books WHERE Number = ?"
        self.cursor.execute(query, (book_number,))
        book = self.cursor.fetchone()
        if book is None:
            return "Book not found"

        if book[6] == 0:
            return "Book is available"

        return "Book is borrowed"

    def set_borrowed_status(self, book_number, borrowed):
        query = "UPDATE Books SET Borrowed = ? WHERE Number = ?"
        self.cursor.execute(query, (borrowed, book_number))
        self.connection.commit()

    def set_borrowed_deadline(self, book_number, deadline):
        query = "UPDATE Books SET Deadline = ? WHERE Number = ?"
        self.cursor.execute(query, (deadline, book_number))
        self.connection.commit()

    def get_borrowed_deadline(self, book_number):
        query = "SELECT Deadline FROM Books WHERE Number = ?"
        self.cursor.execute(query, (book_number,))
        deadline = self.cursor.fetchone()
        if deadline is None:
            return "Book not found"

        return deadline[0]


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

##account settings
@app.get("/account-settings", response_class=HTMLResponse)
def show_account_settings(request: Request):
    return templates.TemplateResponse("accountSettings.html", {"request": request})

@app.post("/delete-account")
async def delete_account(request: AccountSettingsRequest):
    login.delete_account(request)
    return {"message": "Account deleted successfully!"}
    raise HTTPException(status_code=404, detail="Account not found!")


@app.post("/reset-password")
async def reset_password_endpoint(request: Request):
    form_data = await request.json()

    recovery_code = form_data.get("recovery_code")
    username = form_data.get("username")
    new_password = form_data.get("new_password")

    print(f"Recovery Code: {recovery_code}")
    print(f"Username: {username}")
    print(f"New Password: {new_password}")

    if recovery_code is None or username is None or new_password is None:
        return {"message": "Invalid form data"}

    result = reset_password_endpoint(recovery_code, username, new_password)

    return result
@app.post("/change-username")
async def change_username(request: AccountSettingsRequest):
    old_username = login.username
    new_username = "NewUsername"

    if old_username == new_username:
        raise HTTPException(status_code=400, detail="New username must be different from the old username.")

    if login.check_account_exists(new_username):
        raise HTTPException(status_code=400, detail="The new username is already taken.")

    login.update_username(old_username, new_username)
    login.username = new_username

    return {"message": "Username changed successfully!"}

@app.post("/change-password")
async def change_password(request: Request):
    form_data = await request.form()
    new_password = form_data.get("new_password")
    username = form_data.get("username")
    login.update_password(username, new_password)

    return {"message": "Password changed successfully!"}


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
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to add book")

@app.get("/account-settings", response_class=HTMLResponse)
def show_update_book_form(request: Request):
    return templates.TemplateResponse("account_settings.html", {"request": request})
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

@app.get("/update-book-edition", response_class=HTMLResponse)
def show_update_book_edition_form(request: Request):
    return templates.TemplateResponse("update_book_edition.html", {"request": request})
@app.post("/update-book-edition")
async def update_book_edition(book_name: str = Form(...), new_edition: int = Form(...)):
    if not library.logged_in:
        raise HTTPException(status_code=400, detail="You are not logged in.")
    library.update_book_edition(book_name, new_edition)
    return {"message": f"Edition updated for book: {book_name}"}


@app.get("/borrow-book", response_class=HTMLResponse)
def show_borrow_book_form(request: Request):
    return templates.TemplateResponse("borrowBook.html", {"request": request})

@app.post("/borrow-book")
def borrow_book(
    request: Request,
    book_number: int = Form(...),
    desired_date: date = Form(...)
):
    borrow_request = BorrowBookRequest(book_number=book_number, desired_date=desired_date)

    library = Library()
    result = library.borrow_book(borrow_request)
    library.finish_connection()

    return {"message": result}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
