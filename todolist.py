from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)


def main():
    today = datetime.today()
    while True:
        print("1) Today's tasks")
        print("2) Week's tasks")
        print("3) All tasks")
        print("4) Missed tasks")
        print("5) Add task")
        print("6) Delete task")
        print("0) Exit")
        choice = input()
        print()

        if choice == "1":
            print(today.date().strftime("Today %d %b:"))
            print_day_tasks(today.date())
        elif choice == "2":
            for day in range(7):
                weekday = today + timedelta(days=day)
                print(weekday.strftime("%A %d %b:"))
                print_day_tasks(weekday.date())
                print()
        elif choice == "3":
            print("All tasks:")
            tasks = session.query(Table).order_by(Table.deadline).all()
            print_all_tasks(tasks)
        elif choice == "4":
            print("Missed tasks:")
            tasks = session.query(Table).order_by(Table.deadline).filter(Table.deadline < today.date()).all()
            print_all_tasks(tasks, "Nothing is missed!")
        elif choice == "5":
            print("Enter task")
            task = input()
            print("Enter deadline")
            deadline = datetime.strptime(input(), "%Y-%m-%d").date()

            session.add(Table(task=task, deadline=deadline))
            session.commit()
            print("The task has been added!")
        elif choice == "6":
            print("Choose the number of task you want to delete:")
            tasks = session.query(Table).order_by(Table.deadline).all()
            print_all_tasks(tasks)
            num_del = input()
            try:
                session.delete(tasks[int(num_del) - 1])
                session.commit()
                print("The task has been deleted")
            except Exception:
                print("Invalid task choice")
        elif choice == "0":
            break
        else:
            print("Invalid choice!")
        print()
    print("Bye!")


def print_all_tasks(tasks, message="Nothing to do!"):
    if tasks:
        for i, task in enumerate(tasks):
            print(f"{i + 1}. {task.task}. {task.deadline.strftime('%d %b')}")
    else:
        print(message)


def print_day_tasks(date):
    tasks = session.query(Table).filter(Table.deadline == date).all()
    if tasks:
        for i, task in enumerate(tasks):
            print(f"{i + 1}. {task}")
    else:
        print("Nothing to do!")


if __name__ == '__main__':
    main()
