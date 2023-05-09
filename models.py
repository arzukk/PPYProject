# database.py

from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# create base model
Base = declarative_base()


# define models
class Category(Base):
    __tablename__ = 'Category'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    tasks = relationship("Task", back_populates="category")


class Task(Base):
    __tablename__ = "Task"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    due_date = Column(Date)
    category_id = Column(Integer, ForeignKey("Category.id"))

    category = relationship("Category", back_populates="tasks")


# create engine and session
engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
