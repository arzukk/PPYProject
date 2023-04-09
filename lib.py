import time

import sqlite3


class Book():
    def __init__(self, name, writer, publisher, type, number_of_page, edition):
        self.name = name
        self.writer = writer
        self.publisher = publisher
        self.type = type
        self.number_of_page = number_of_page
        self.edition = edition

    def __str__(self):
        return " Name: {}\n Writer: {}\n Publisher: {}\n Type: {}\n Number of Page: {}\n Edition: {}".format(self.name,
                                                                                                             self.writer,
                                                                                                             self.publisher,
                                                                                                             self.type,
                                                                                                             self.number_of_page,
                                                                                                             self.edition)


class Library():
    def __init__(self):
        self.Create_Connection()

    def Create_Connection(self):
        self.connection = sqlite3.connect("Books.db")
        self.cursor = self.connection.cursor()
        query = "CREATE TABLE IF NOT EXISTS Books (Name TEXT,Writer TEXT ,Publisher TEXT,Type TEXT,Number of Page INT,Edition INT)"
        self.cursor.execute(query)
        self.connection.commit()

    def Finish_Connection(self):
        self.connection.close()

    def Show_ALL_Books(self):
        query = "SELECT * FROM Books "
        self.cursor.execute(query)
        Books = self.cursor.fetchall()

        if len(Books) == 0:
            print("No book in library")
        else:
            for i in Books:
                book1 = Book(i[0], i[1], i[2], i[3], i[4], i[5])
                print(book1)
                print("*************************")

    def Query_To_Book(self, name):
        query = "SELECT * FROM Books WHERE Name = ? "
        self.cursor.execute(query, (name,))
        books = self.cursor.fetchall()

        if len(books) == 0:
            print("This book not in library")
        else:
            book = Book(books[0][0], books[0][1], books[0][2], books[0][3], books[0][4], books[0][5])
            print("************************************************")
            print(book)
            print("************************************************")

    def Add_To_Book(self, name, writer, publisher, type, number_of_page, edition):
        query = "INSERT INTO Books VALUES (?,?,?,?,?,?)"
        book = Book(name, writer, publisher, type, number_of_page, edition)
        self.cursor.execute(query,
                            (book.name, book.writer, book.publisher, book.type, book.number_of_page, book.edition))
        self.connection.commit()

    def Delete_Book(self, name):
        query = "SELECT * FROM Books WHERE Name = ?"
        self.cursor.execute(query, (name,))
        Books = self.cursor.fetchall()

        if len(Books) == 0:
            print("Loading...")
            time.sleep(2)
            print("This book not in library so not deleted")
        else:
            print("Loading...")
            time.sleep(3)

            query = "DELETE FROM Books WHERE Name = ?"

            self.cursor.execute(query, (name,))
            self.connection.commit()
            print("The book has been deleted.")

    def Update_Edition(self, name):
        query = "SELECT * FROM Books WHERE Name = ?"
        self.cursor.execute(query, (name,))
        Books = self.cursor.fetchall()

        if len(Books) == 0:
            print("Loading...")
            time.sleep(2)
            print("This book not in library so not deleted")

        # yeni update yeri burasi, ekleme yaptim kitap odunc alimi icin
        else:
            print("Loading...")
            time.sleep(3)

            new_edition = int(input("Enter the new edition number: "))

            query = "UPDATE Books SET Edition = ? WHERE Name = ?"
            self.cursor.execute(query, (new_edition, name))
            self.connection.commit()
            print("The edition of the book has been updated.")

    def Borrow_Book(self, name, deadline):
        query = "SELECT * FROM Books WHERE Name = ?"
        self.cursor.execute(query, (name,))
        book = self.cursor.fetchone()

        if book:
            if book[5] == 0:
                query = "UPDATE Books SET IsBorrowed = ?, Deadline = ? WHERE Name = ?"
                self.cursor.execute(query, (1, deadline, name,))
                self.connection.commit()
                print(f"Book '{name}' is successfully borrowed. Please return by {deadline}.")
            else:
                print(f"Book '{name}' is already borrowed.")
        else:
            print(f"Book '{name}' not found in the library.")

    def Return_Book(self, name):
        query = "SELECT * FROM Books WHERE Name = ?"
        self.cursor.execute(query, (name,))
        book = self.cursor.fetchone()

        if book is None:
            print("Loading...")
            time.sleep(2)
            print("This book is not in the library.")
        elif book[5] == 0:
            print("Loading...")
            time.sleep(2)
            print("This book is not borrowed.")
        else:
            print("Loading...")
            time.sleep(3)

            query = "UPDATE Books SET Borrowed = ?, Deadline = ? WHERE Name = ?"
            self.cursor.execute(query, (0, "", name))
            self.connection.commit()
            print("The book has been returned.")
