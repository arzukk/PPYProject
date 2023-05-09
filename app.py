# app.py

from datetime import datetime
from sqlalchemy.orm import sessionmaker
from models import Task, Category, Base, engine, session, Session


class App:
    def __init__(self):
        self.Session = sessionmaker(bind=engine)

    def create_category(self, name):
        session = self.Session()
        category = Category(name=name)
        session.add(category)
        session.commit()
        return category.id

    def create_task(self, title, description, due_date, category_id):
        session = self.Session()
        task = Task(title=title, description=description, due_date=due_date, category_id=category_id)
        session.add(task)
        session.commit()
        return task.id

    def get_task(self, id):
        session = self.Session()
        task = session.query(Task).filter(Task.id == id).first()
        return task

    def update_task(self, id, title=None, description=None, due_date=None, category_id=None):
        session = self.Session()
        task = self.get_task(id)
        if title:
            task.title = title
        if description:
            task.description = description
        if due_date:
            task.due_date = due_date
        if category_id:
            task.category_id = category_id
        session.commit()

    def delete_task(self, session, task_id):
        task = session.query(Task).filter_by(id=task_id).one()
        session.delete(task)
        session.commit()


# sample usage
app = App()
category_id = app.create_category('Work')
task_id = app.create_task('Finish project', 'Complete the project by end of week', datetime(2023, 5, 12), category_id)
task = app.get_task(task_id)
print(task.title, task.description, task.due_date, task.category.name)

app.update_task(task_id, title='Finish project earlier')
task = app.get_task(task_id)
print(task.title, task.description, task.due_date, task.category.name)

# this two lines can be wrong i couldn't make it
def db_session():
    return Session()

task_id = 1
session = db_session()
app = App()

app.delete_task(session, task_id)
task = app.get_task(task_id)
print(task)  # will print None
