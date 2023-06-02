# import sqlite3
# from fastapi import FastAPI, Request
# from fastapi.exceptions import HTTPException
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from pydantic import BaseModel
#
# app = FastAPI()
# templates = Jinja2Templates(directory="/Users/arzukilic/PycharmProjects/PPYProject/templates")
#
#
# class AddBookRequest(BaseModel):
#     name: str
#     writer: str
#     publisher: str
#     type: str
#     number_of_page: int
#     edition: int
#
#
# class Book:
#     def __init__(self, name, writer, publisher, type, number_of_page, edition):
#         self.name = name
#         self.writer = writer
#         self.publisher = publisher
#         self.type = type
#         self.number_of_page = number_of_page
#         self.edition = edition
#
#     def __str__(self):
#         return " Name: {}\n Writer: {}\n Publisher: {}\n Type: {}\n Number of Page: {}\n Edition: {}".format(
#             self.name,
#             self.writer,
#             self.publisher,
#             self.type,
#             self.number_of_page,
#             self.edition
#         )
#
#
# class Library:
#     def __init__(self):
#         self.create_connection()
#         self.logged_in = False
#
#     def create_connection(self):
#         self.connection = sqlite3.connect("Books.db")
#         self.cursor = self.connection.cursor()
#         query = "CREATE TABLE IF NOT EXISTS Books (Name TEXT,Writer TEXT,Publisher TEXT,Type TEXT, Number_Of_Page INT, Edition INT)"
#         self.cursor.execute(query)
#         self.connection.commit()
#
#     def finish_connection(self):
#         self.connection.close()
#
#     def add_book(self, name, writer, publisher, type, number_of_page, edition):
#         query = "INSERT INTO Books VALUES (?,?,?,?,?,?)"
#         book = Book(name, writer, publisher, type, number_of_page, edition)
#         self.cursor.execute(query,
#                             (book.name, book.writer, book.publisher, book.type, book.number_of_page, book.edition))
#         self.connection.commit()
#
#
# library = Library()
#
# @app.get("/add-book", response_class=HTMLResponse)
# def show_add_book_form(request: Request):
#     return templates.TemplateResponse("add_book.html", {"request": request})
#
#
# @app.post("/add-book")
# def add_book(request: AddBookRequest):
#     library.add_book(request.name, request.writer, request.publisher, request.type, request.number_of_page,
#                      request.edition)
#     return {"message": "Book added successfully!"}
