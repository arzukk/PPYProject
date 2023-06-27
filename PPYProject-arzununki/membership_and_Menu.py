import random
import time
import sqlite3
import time
from http.client import HTTPException
from typing import List
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi import Response, RedirectResponse
import lib
from fastapi import FastAPI
from pydantic import BaseModel
from project import app


class Membership():
    def __init__(self):
        self.Create_Connection()

    def Create_Connection(self):
        self.connection = sqlite3.connect("Members.db")
        self.cursor = self.connection.cursor()
        query = "CREATE TABLE IF NOT EXISTS Members (Username TEXT,Password TEXT,Email TEXT,Recovery_Code INT)"
        self.cursor.execute(query)
        self.connection.commit()

    def Finish_Connection(self):
        self.connection.close()

    def Delete_Account(self, name, email):
        query = "SELECT * FROM Members WHERE Username = ? and Email = ?"
        self.cursor.execute(query, (name, email))
        list1 = self.cursor.fetchall()

        if len(list1) == 0:
            print("There is no such account!")

        else:
            sure = input("Are you sure? (Y or N) ")
            if sure == "N":
                print("Loading...")
                time.sleep(2)
                print("Canceled")
            elif sure == "Y":
                query2 = "DELETE FROM Members WHERE Username =?"
                self.cursor.execute(query2, (name,))
                self.connection.commit()
                print("Loading...")
                time.sleep(2)
                print("Deleted")

    def Change_Username(self, name, new_name):
        query = "SELECT * FROM Members WHERE Username = ? "
        self.cursor.execute(query, (name,))
        list1 = self.cursor.fetchall()

        if len(list1) == 0:
            print("There is no such account!")

        else:
            sure = input("Are you sure: (Y or N)")
            if sure == "N":
                print("Loading...")
                time.sleep(2)
                print("Canceled")
            elif sure == "Y":
                query2 = "UPDATE   Members SET Username = ? WHERE Username =?"
                self.cursor.execute(query2, (new_name, name))
                self.connection.commit()
                print("Loading...")
                time.sleep(2)
                print("Changed")

    def Change_Password(self, name, password, new_password):
        pass

        query = "SELECT * FROM Members WHERE Username = ? AND Password=?"
        self.cursor.execute(query, (name, password))
        list1 = self.cursor.fetchall()

        if len(list1) == 0:
            print("There is no such account!")

        else:
            sure = input("Are you sure: (Y or N)")
            if sure == "N":
                print("Loading...")
                time.sleep(2)
                print("Canceled")
            elif sure == "Y":
                query2 = "UPDATE   Members SET Password = ? WHERE Username =?"
                self.cursor.execute(query2, (new_password, name))
                self.connection.commit()
                print("Loading...")
                time.sleep(2)
                print("Changed")

    def Recovery_Code(self, username, email):
        query = "SELECT * FROM Members WHERE Username = ? and Email =?"
        self.cursor.execute(query, (username, email))
        list1 = self.cursor.fetchall()

        if len(list1) == 0:
            print("No found any data!")
        else:
            if email == list1[0][2] and username == list1[0][0]:

                recovery_code = int(input("Enter your recovery code:"))
                if recovery_code == list1[0][3]:
                    print("Loading.....")
                    time.sleep(4)
                    print("Your password is:", list1[0][1])
                else:
                    print("Your recovery code is false try later!")

            else:
                print("Loading...")
                time.sleep(4)
                print("Your email or username are false try later")
