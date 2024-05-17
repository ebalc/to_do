from datetime import datetime
import mysql.connector

### Create a new section called "view old tasks" and give user option to delete them

# Database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="todo"

)
mycursor = db.cursor()
# Datetime
current_date = datetime.now().date()
current_day = datetime.now().strftime('%A')

def counting_rows():
    query = "SELECT COUNT(*) FROM Tasks WHERE DATE(do_date) = %s"
    mycursor.execute(query, (current_date, ))
    row_count = mycursor.fetchone()[0]
    x = "SELECT"
    return row_count


def ask_question():
    question = input(f"\nChoose option to do:\n"
                     f"1. See todays ToDo's\n"
                     f"2. Add ToDo\n"
                     f"3. View upcoming days\n"
                     f"4. Delete ToDo\n"
                     f"5. Old Tasks Management\n"
                     f"6. Exit\n")
    return question


def get_user_input(prompt):
    return input(prompt)


def prompt_add_task():
    while True:
        due_date = get_user_input("Enter date for the task (e.g '01-01-2024'): ")
        if due_date.lower() == 'back':
            return  # Return to the main menu
        task_name = get_user_input("Enter the task: ")
        if task_name.lower() == 'back':
            return  # Return to the main menu
        try:
            insert_todo_database(task_name, due_date)
            print("Task added")
            break
        except ValueError:
            print("Date format incorrect")


def insert_todo_database(task, do_date):

    # Convert do_date string to datetime object
    do_date = datetime.strptime(do_date, '%d-%m-%Y')

    # Insert into the database
    mycursor.execute("INSERT INTO Tasks (task, created, do_date) VALUES (%s, %s, %s)", (task, datetime.now().date(), do_date))
    db.commit()


def view_tasks_today():
    # SQL query to fetch tasks scheduled for today
    sql_query = "SELECT * FROM Tasks WHERE DATE(do_date) = %s ORDER BY do_date ASC"
    # Execute the query with the current date parameter
    mycursor.execute(sql_query, (current_date,))
    # Fetch all rows
    rows = mycursor.fetchall()
    # Check if there are tasks for today
    if len(rows) == 0:
        print("No tasks scheduled for today.")
        return
    # Print each row with sequential numbering
    print("Today's Tasks:")
    for idx, row in enumerate(rows, start=1):
        task = row[0]
        do_date = row[2].strftime("%d-%m-%Y")
        print(f"{idx}. {task}\nDue: {do_date}")


def display_tasks():

    # Execute query to fetch tasks with due_date today or in the future
    query = ("SELECT * FROM Tasks WHERE do_date >= %s ORDER BY do_date ASC")
    mycursor.execute(query, (current_date,))
    # Fetch all rows
    rows = mycursor.fetchall()

    # Print each row with sequential numbering
    for idx, row in enumerate(rows, start=1):
        task = row[0]
        do_date = row[2].strftime("%d-%m-%Y")
        print(f"{idx}. {task}\nDue: {do_date}")


def delete_todo():
    # Execute query to fetch all rows ordered by due_date
    mycursor.execute("SELECT * FROM Tasks ORDER BY do_date ASC")

    # Fetch all rows
    rows = mycursor.fetchall()

    # Display tasks with sequential numbering
    display_tasks()

    while True:
        # Get the sequential number of the task to delete from the user
        while True:
            record_to_delete_num = input("\nEnter the number of the task to delete: ")
            if record_to_delete_num == "back":
                return
            if record_to_delete_num.isdigit():  # Check if input is a digit
                record_to_delete_num = int(record_to_delete_num)
                break
            else:
                print("Please enter a valid integer.")

        # Check if the entered number is within the range of displayed tasks
        if 1 <= record_to_delete_num <= len(rows):
            # Find the corresponding database ID for the selected task
            record_to_delete_id = rows[record_to_delete_num - 1][3]

            # Execute the DELETE statement with the ID parameter
            mycursor.execute("DELETE FROM Tasks WHERE ID = %s", (record_to_delete_id,))

            # Commit the changes to the database
            db.commit()

            print(f"Task number {record_to_delete_num} has been deleted.")
            break
        else:
            print("Please enter a number within the range of tasks.")


def view_old_tasks():
    query = "SELECT * FROM Tasks WHERE do_date < %s ORDER BY do_date ASC"
    mycursor.execute(query, (current_date,))
    rows = mycursor.fetchall()
    if len(rows) == 0:
        print("No old tasks found.")
        return
    print("Old and Missed Tasks:")
    for idx, row in enumerate(rows, start=1):
        task = row[0]
        do_date = row[2].strftime("%d-%m-%Y")
        print(f"{idx}. {task}\nDue: {do_date}")

    while True:
        action = input("\nType 'back' or enter number of task to delte it: ")
        if action.lower() == "back":
            return
        elif action.isdigit():
            record_to_delete_num = int(action)
            if 1 <= record_to_delete_num <= len(rows):
                record_to_delete_id = rows[record_to_delete_num - 1][3]

                mycursor.execute("DELETE FROM Tasks WHERE ID = %s", (record_to_delete_id,))
                db.commit()

                print(f"Task number {record_to_delete_num} has been deleted.")
                break
            else:
                print("Please enter a number within the range of tasks.")
        else:
            print("Invalid input. Please try again.")



## Creating database "todo"
# mycursor.execute("CREATE DATABASE IF NOT EXISTS todo")


## Creating table "tasks"
# mycursor.execute("CREATE TABLE Tasks (task varchar(255) NOT NULL,"
#                  " created datetime NOT NULL, do_date datetime NOT NULL)")

# mycursor.execute("ALTER TABLE Tasks ADD COLUMN id int PRIMARY KEY NOT NULL AUTO_INCREMENT")


## Actual code
print(f"It's {current_day}, {current_date} you have {counting_rows()} ToDo's.\n\n"
          f"To return to the main menu at any time, just type 'back'.")
while True:
    question = ask_question()
    if question == "1":
        view_tasks_today()
    if question == "2":
        prompt_add_task()
    if question == "3":
        display_tasks()
    if question == "4":
        delete_todo()
    if question == "5":
        view_old_tasks()
    if question == "6":
        break


