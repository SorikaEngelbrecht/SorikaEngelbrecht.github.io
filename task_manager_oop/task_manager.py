'''
task_manager.py

This module comprises a login section with tailored
menu options for admin and non-admin users.
It allows tracking and updating of tasks.
It generates user and task reports for admin.
'''
# ===== Importing external modules ===========
from tabulate import tabulate  # Assists with user friendly output
from datetime import date  # Allows processing of dates
from datetime import datetime

# ==== Functions used in Class =========


def check_convert_date(date):
    '''
    This function receives a date in YYYY-MM-DD format
    and converts it to a written format (e.g. 2 Oct 2025)
    Args:
        date (str): a date that need conversion.
    Returns:
        new_date (str): The converted date.
    Raises:
        ValueError if incorrect format entered/no a date.
    '''
    try:
        new_date = datetime.strptime(date, "%Y-%m-%d")
        new_date = new_date.strftime("%d %b %Y")
        return new_date
    except ValueError as error:
        print("Invalid date entered")
        print(error)
        return None


# ===== Classes ===============================


class Task:
    '''A task with attributes'''
    def __init__(
            self,
            username,
            title,
            description,
            due_date,
            assign_date: date = None,
            completed: str = None
           ):
        '''Contructs the class Task
        Attributes
            username (str) :    The username to whom the task is assigned.
            title (str) :       The title of the task.
            description (str):  A description of the task.
            assign_date (str):  Date of assignment.
                                Default is today.
            due_date (str):     The due date of the task.
            completed (str):    Indicates completion. Defaults to No.
        '''
        self.username = username
        self.title = title
        self.description = description
        format_date = check_convert_date(str(date.today()))
        self.assign_date = assign_date or format_date
        self.due_date = due_date
        self.completed = completed or "No"

    def __str__(self):
        '''Specialiased string method
        Args:
            None
        Returns
            String of Class attributes separated by ', '
        '''
        string = (f"{self.username}, {self.title}, "
                  f"{self.description}, {self.assign_date}, "
                  f"{self.due_date}, {self.completed}"
                  )
        return string

    def pretty_output(self):
        '''Displays Class attributes in a user-friendly manner
        Args:
          None
        Returns:
          String of Multiple lines with headers and values separarted
          by tabs
        '''
        string = (f"Task:\t\t\t{self.title}\n"
                  f"Assigned to:\t\t{self.username}\n"
                  f"Date assigned:\t\t{self.assign_date}\n"
                  f"Due date:\t\t{self.due_date}\n"
                  f"Task complete?:\t\t{self.completed}\n"
                  f"Task description:\n {self.description}"
                  )
        return string

    def get_username(self):
        '''
        Outputs Task username assignment
        Args:
            None
        Returns:
            username (str): The assigned username.
        '''
        return self.username

    def is_completed(self):
        '''Returns boolean True if task is completed'''
        if self.completed == "No":
            return False
        else:
            return True

    def mark_complete(self):
        '''Updates the completed attribute
        Args:
            None
        Returns:
            No returns
        '''
        self.completed = "Yes"

    def update_username(self, new_user):
        '''Alters the class attribute username
        Args:
            new_user (str): The new username that the task is assigned to
        Returns
            No returns'''
        self.username = new_user

    def update_due_date(self, new_date):
        ''' Alters the due_date
        Args:
            new_date(str): The new due_due.
        Returns:
            No returns
        '''
        self.due_date = new_date

    def is_overdue(self):
        '''Determines if the task is overdue today.
        Args:
            None
        Returns
            Boolean: True if the task is overdue
        '''
        due_date = self.due_date
        due_date = datetime.strptime(due_date, "%d %b %Y").date()
        if (due_date) < date.today():
            return True
        else:
            return False


# ===== Define variables used in functions ====
# assign empty username directory
usernames = {}
# assign empty task list
tasks = []
#  assign file paths
path_users = "./user.txt"
path_tasks = "./tasks.txt"


# ==== Non-Class Functions ====================
def read_users():
    '''Reads all the users from user.txt into dictionary usernames'''
    try:
        global usernames
        usernames = {}
        # open user.txt and read usernames and passwords into directory
        with open(path_users, "r", encoding="utf-8") as user_file:
            for line in user_file:
                # split line into words found in a list
                words = line.split(", ")
                # assign username as key and password as value
                usernames[words[0]] = words[1].strip("\n")
    # raise a FileNotFoundError if the file is not found
    except FileNotFoundError as error:
        print("'user.txt' file was not found")
        print(error)


def read_tasks():
    '''
    Reads all task information from tasks.txt.
    Constructs a class for each task.
    Creates a list (tasks) of all the Task classes
    '''
    global tasks
    tasks = []
    try:
        with open(path_tasks, "r", encoding="utf-8") as task_file:
            for line in task_file:
                # Make sure there is no \n in the string
                line = line.strip("\n")
                # Separate items by ,
                words = line.split(", ")
                # Add to task list
                tasks.append(Task(words[0], words[1], words[2], words[3],
                             words[4], words[5]))

    except FileNotFoundError as error:
        print("'tasks.txt' not found")
        print(error)


def reg_user():
    '''
    Requests the relevant fields from user.
    Ensures no duplicate usernames.
    Confirms valid password
    Adds new users to user.txt
    '''
    while True:
        # Request new username
        new_username = input("Please enter your username:\n\t")
        # Check for duplicate usernames
        if new_username in usernames:
            print("This username is already taken. Please try another.")
            continue
        else:
            break
            # Allow multiple password attempts until confirmed
    while True:
        # Request input of a new password
        new_password = input("Please enter your password:\n\t")
        # Request input of password confirmation.
        confirm_password = input("Please confirm your password:\n\t")
        # Add new user to text file
        if new_password == confirm_password:
            try:
                with open(path_users, "a") as user_file:
                    string = f"\n{new_username}, {new_password}"
                    user_file.write(string)
                    print(f"\nNew user {new_username} has been added.\n")
                    break
            except FileNotFoundError as error:
                print("\n'user.txt' was not found")
                print(error)
        else:
            print("Confirmation password does not match. Please try again")


def add_task():
    '''
    Add new task to task list.
    Updates tasks.txt
    '''
    read_tasks()
    read_users()
    # This code block allows a user to add a new task to task.txt file
    print("\nADD NEW TASK")
    # Prompt user for username for assignment
    while True:  # Ensure valid username
        user_task = input("Please enter the username for the person\n"
                          "that you would like to assign the task to:\n\t")
        if user_task in usernames:
            break
        else:
            print("Username not found. Please enter a valid username")
    # Request task title. Ensure no commas.
    task_title = input("Please enter the name of the new task:"
                       "\n\t").replace(',', '')
    # Request description. Ensure no commas.
    task_description = input("Please enter a description of"
                             f" {task_title}:\n\t").replace(',', '')
    # Request and ensure valid due date
    while True:
        due_date = check_convert_date(input("Please enter the due date "
                                            "(YYYY-MM-DD) of the task:\n\t"))
        if not due_date:
            print("Please add valid date")
            continue
        # Ensure due date is today or in future
        if datetime.strptime(due_date, "%d %b %Y").date() < date.today():
            print("Invalid date entry. Due date cannot be before"
                  " assignment date.")
            continue
        else:
            break
    # Add new task to list
    tasks.append(Task(user_task, task_title, task_description, due_date))

    # Write updated task list to file
    try:
        with open(path_tasks, "a") as task_file:
            task_file.write(f"\n{tasks[-1]}")
            print(f"\n{task_title} has been added.")
    except FileNotFoundError as error:
        print('tasks.txt not found')
        print(error)


def view_all():
    '''
    Displays all tasks in an user-friendly manner
    '''
    # Ensure updated list
    read_tasks()
    print("\nVIEW ALL TASKS")
    for i, task in enumerate(tasks):
        print('_' * 50)  # Print seperation line
        print(f"Task number:\t\t{i}\n")
        print(task.pretty_output())
        print('_' * 50)


def update_tasks_file():
    # Updates task file with new task list
    try:
        with open(path_tasks, "w") as tasks_file:
            for task in tasks:
                tasks_file.write(f"{task}\n")
    except FileNotFoundError as error:
        print("tasks.txt was not found")
        print(error)


def view_mine():
    '''
    Only displays logged in user's assigned tasks.
    Allows for updating.
    '''
    print("\nVIEW MY TASKS")
    read_tasks()
    my_tasks = []
    task_count = 0
    for task_num, task in enumerate(tasks):
        if username == task.get_username():
            # Make sure displayed task number correlates with task list
            # Create list that keeps record of relevant task numbers
            my_tasks.append(task_num)
            print('_' * 50)
            print(f"Task number:\t\t{task_num}")
            print(task.pretty_output())
            print('_' * 50)
            task_count += 1
    print(f"\nTotal tasks = {task_count}")

    # ensure valid selection
    while True:
        try:
            selection = int(input("Please select a task number to update "
                                  "or -1 to return to menu:\n\t"))
            if selection == -1:
                return
            # Make sure selected task is relevant to user
            elif selection in my_tasks:
                # Only incompleted tasks can be edited
                if tasks[selection].is_completed() is True:
                    print("Only incomplete tasks can be edited, please "
                          "select another task.")
                    continue
                else:
                    break
            else:
                print("Please select a valid task number.")
                continue
        except ValueError as error:
            print("Please enter a valid task number")
            print(error)
    while True:
        # Present edit options
        update_option = input("Please select one of the following options to "
                              f" perform with Task {selection}:\n"
                              "mc \t- mark as complete\n"
                              "ed \t- edit\n\t").lower()
        # Selected mark complete
        if update_option == "mc":
            tasks[selection].mark_complete()
            # Communicate succesful update
            print(f"{tasks[selection].pretty_output()}")
            break
        elif update_option == "ed":
            while True:
                edit_option = input("\nPlease select an option:\n"
                                    "eu\t- edit username\n"
                                    "edd\t- edit due date\n\t").lower()
                # Selected edit username
                if edit_option == "eu":
                    while True:
                        new_username = input("Please enter the username that"
                                             "the task is assigned to:\n\t")
                        read_users()
                        # Ensure valid username
                        if new_username in usernames:
                            tasks[selection].update_username(new_username)
                            print(tasks[selection].pretty_output())
                            break
                        else:
                            print("\nInvalid username. Please select valid "
                                  "username")
                    break
                # Selected edit due date
                elif edit_option == "edd":
                    while True:
                        # Ensure valid date and preferred format
                        try:
                            new_due_date = input("Please enter"
                                                 " the new due"
                                                 " date (YYYY-MM-DD):")
                            new_due_date = check_convert_date(new_due_date)
                            break
                        except ValueError:
                            print("Please try again")
                    # Update due date
                    tasks[selection].update_due_date(new_due_date)
                    print(new_due_date)
                    # Display update
                    print(tasks[selection].pretty_output())
                    break
                else:
                    print("Please enter a valid option")
            break
        else:
            print("Please enter valid selction option")
    # Write changes to file
    update_tasks_file()


def view_completed():
    ''' Finds and displays completed tasks'''
    read_tasks()
    print('\nVIEW COMPLTETED TASKS\n')
    num_completed = 0
    for task in tasks:
        if task.is_completed() is True:
            num_completed += 1
            print('_' * 50)
            print(task.pretty_output())
            print('_' * 50)
    print(f"\nNumber of completed tasks = {num_completed}.")


def delete_task():
    '''Deletes requested task'''
    read_tasks()
    # Shows available tasks for selection
    view_all()
    while True:
        try:
            # Ensure number entered
            del_index = int(input("Please enter the number of the task to "
                                  "delete: "))
            break
        except ValueError as error:
            print('Value entered was not a number. Please nter a number')
            print(error)
    # Check that task number exists
    if int(del_index) in range(len(tasks) + 1):
        # Temporray hold of data to be deleted
        del_task = tasks[del_index].pretty_output()
        # Delete from task list
        del tasks[del_index]
        try:
            # Change file
            update_tasks_file()
            print("\nThe following task was deleted:\n")
            print(del_task)
            # Display update
        except FileNotFoundError as error:
            print('tasks.txt was not found.')
            print(error)
    else:
        print("Please select a valid task number")


def find_completed():
    # Finds and returns the number of completed tasks
    tasks_complete = 0
    for task in tasks:
        if task.is_completed() is True:
            tasks_complete += 1
    return tasks_complete


def find_overdue():
    # Finds and returns the number of overdue tasks
    num_overdue = 0
    for task in tasks:
        if (task.is_completed() is False) and (task.is_overdue() is True):
            num_overdue += 1
    return num_overdue


def find_tasks_per_user(total_tasks):
    '''Finds the stats of all tasks as grouped by users'''
    all_users = []
    # Outside loop: all users
    for name in usernames:
        num_tasks = 0
        comp_tasks = 0
        num_overdue = 0
        # Inside loop: all tasks associated with ouside user
        for task in tasks:
            if task.get_username() == name:
                num_tasks += 1
                if task.is_completed():
                    comp_tasks += 1
                elif task.is_overdue():
                    num_overdue += 1
        # Prevent devision by 0
        percent_assigned = 0
        percent_complete = 0
        percent_incomplete = 0
        percent_overdue = 0
        # Calculate stats
        if num_tasks > 0:
            percent_assigned = round((num_tasks/total_tasks) * 100, 2)
            percent_complete = round((comp_tasks/num_tasks) * 100, 2)
            percent_incomplete = round(100 - percent_complete, 2)
            percent_overdue = round((num_overdue/num_tasks) * 100, 2)
        # Create a row for each user: list format so tabulate possible
        user_row = [name,
                    num_tasks,
                    comp_tasks,
                    num_overdue,
                    percent_assigned,
                    percent_complete,
                    percent_incomplete,
                    percent_overdue]
        # Create a 2D list of all users
        all_users.append(user_row)
    return all_users


def display_stats():
    # Ensure updated tasks
    read_tasks()
    # Determine total number of tasks
    total_tasks = len(tasks)
    num_complete = find_completed()
    num_incomplete = total_tasks - num_complete
    num_overdue = find_overdue()
    # Calculate percentages
    percent_incomplete = round((num_incomplete/total_tasks)*100, 2)
    percent_overdue = round((num_overdue/total_tasks)*100, 2)
    # Reader-freindly display
    tasks_stats = (f"TASKS STATS {date.today()}\n"
                   f"Total tasks:\t\t{total_tasks}\n"
                   f"Completed tasks:\t{num_complete}\n"
                   f"Incomplete tasks:\t{num_incomplete}\n"
                   f"Incomplete(%):\t\t{percent_incomplete}\n"
                   f"Overdue tasks:\t\t{num_overdue}\n"
                   f"Percentage overdue:\t{percent_overdue}\n\n"
                   )
    # Display tasks statistics
    print(tasks_stats)

    # Get users statistics
    # Ensure updated list
    read_users()
    # Determine total number of users
    total_users = len(usernames)
    # Get 2D list of task attributes grouped per user
    user_tasks = find_tasks_per_user(total_tasks)
    # Assign headings for table
    headings = ('Username', 'Assigned tasks', 'Completed', 'Overdue',
                'Assigned(%)', 'Complete(%)', 'Incomplete(%)', 'Overdue(%)')
    # Create page heading
    output = (
              f"USER OVERVIEW {date.today()}\n"
              f"Total users: {total_users}\n"
             )
    print(output)
    # Print user stats table
    print(tabulate(user_tasks, headers=headings, tablefmt="grid",
                   stralign="center", numalign="center"))
    # Write task report to file
    try:
        with open('./task_overview.txt', "w") as task_overview:
            task_overview.write(tasks_stats)
    except FileNotFoundError as error:
        print("task_overview not found")
        print(error)

    # Write user report to file
    try:
        with open('./user_overview.txt', "w") as user_overview:
            user_overview.write(output)
        with open('./user_overview.txt', "a") as user_overview:
            user_overview.write(tabulate(user_tasks, headers=headings,
                                         tablefmt="grid", stralign="center",
                                         numalign="center"))
    except Exception:
        print('Could not write to file user_overview.txt')


# ==== Define main program variables ====

# Define admin and non-admin menus
admin_menu = {'r': '- register a user',
              'a': '- add task',
              'va': '- view all tasks',
              'vm': '- view my tasks',
              'vc': '- view completed tasks',
              'del': '- delete tasks',
              'ds': '- display statistics',
              'e': '- exit'
              }

user_menu = {'a': '- add task',
             'va': '- view all tasks',
             'vm': '- view my tasks',
             'e': '- exit',
             }


# ==== Login Section ====
read_users()

# Allow repeated attempts to login until valid entry
while True:
    print("\nLOGIN")
    # Request user login details
    username = input("Please enter your username: \n\t")
    password = input("Please enter your password: \n\t")
    # Find username in directory
    if username in usernames:
        if usernames[username] == password:
            # End loop if username found and
            # Password matches
            break
        else:
            # No match
            print("Invalid password")
    else:
        # Username not in dictionary
        print("Username was not found. Please try again.")

while True:
    print("\nMENU")
    # Display different menu options depending on username
    if username == 'admin':
        options = admin_menu
    else:
        options = user_menu
    for selections in options:
        print(f"{selections}\t{options[selections]}")

    # Make sure that the user input is converted to lower case.
    menu = input('\nSelect one of the above options:').lower()

    if menu == 'r':
        if username == 'admin':
            '''This code block request new user details and writes
                them to the user file upon password confirmation'''
            print("\nREGISTER NEW USER")
            reg_user()
        else:
            print('Only admin is allowed to register a new user.')
    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    # Admin only options
    # Even if non-admin users enter these options
    # without menu options displayed code will not execute
    elif menu == 'vc':
        if username == 'admin':
            view_completed()
        else:
            print('Only admin can view completed tasks.')

    elif menu == 'del':
        if username == 'admin':
            delete_task()
        else:
            print('Only admin is allowed to delete tasks.')
    elif menu == 'ds':
        if username == 'admin':
            display_stats()
        else:
            print("Only admin can display statistics")
            print("Please select another option")

    else:
        print("You have entered an invalid input. Please try again")
