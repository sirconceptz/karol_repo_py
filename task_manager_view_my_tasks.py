# This program is a task management system that allows users to log in and view all tasks, view their assigned tasks, and register
# new users. If the user is an admin, they also have the option to add a new task and view statistics for the number of registered
# users and number of tasks. The program reads user and task information from 'user.txt' and 'tasks.txt' files, respectively. 
# The program also includes a login system to ensure only authorized users have access to the task management system.

# ==============================================================================================================================

# The code below defines all necessary functions and checks if the entered username and password match a valid combination in the user.txt file. 
# If a match is found, it logs the user in. If not, it prompts the user to enter their credentials again until a match is found 
# or the user quits.


import datetime

def login():
    while True:
        entered_username = input("Enter your username: ")
        entered_password = input("Enter your password: ")

        with open('user.txt', 'r') as f:
            contents = f.read()

        lines = contents.split('\n')
        login_successful = False
        is_admin = False

        for line in lines:
            if ',' in line:
                username, password = line.split(',', maxsplit=1)
                username = username.strip()
                password = password.strip()
                if entered_username == username and entered_password == password:
                    login_successful = True
                    is_admin = (username == 'admin')
                    break
        if login_successful:
            print("\nLogin successful!")
            logged_in_user = entered_username
            return login_successful, is_admin, username
        else:
            print("\nLogin unsuccessful. Please try again.")

login_successful, is_admin, logged_in_user = login()

# This function reads the contents of the user.txt and tasks.txt files and prints a statement saying how many users and tasks there are.
def print_statistics():
    # Count the number of registered users
    with open('user.txt', 'r') as f:
        contents = f.read()
        users = contents.split("\n")
        num_users = 0
    for user in users:
        if ',' in user:
            num_users += 1
    # Count the number of tasks
    with open('tasks.txt', 'r') as f:
        contents = f.read()
        tasks = contents.split("\n")
        num_tasks = 0
        for task in tasks:
            if ',' in task:
                num_tasks += 1
    # Print the statistics
    print(f"\nThere are currently {num_users} registered users and {num_tasks} tasks assigned.")
    return

# This function allows the admin to register new users. It writes the login details to users.txt 
def register_user(username):
    if username == 'admin':
        new_user = input("Enter a new username: ")
        while True:
            # check if the new_user already exists in the user.txt file
            with open('user.txt', 'r') as file:
                users = file.read().splitlines()
                for user in users:
                    if new_user in user:
                        print("Username already taken. Please choose a different one.")
                        new_user = input("Enter a new username: ")
                        # refresh the contents of the file
                        with open('user.txt', 'r') as file:
                            users = file.read().splitlines()
                        break
                else:
                    break
        password = input("Enter a new password: ")
        while True:
            password_confirmation = input("Confirm password: ")
            if password == password_confirmation:
                break
            else:
                print("Passwords do not match. Please try again.")
        with open('user.txt', 'a') as file:
            file.write(f'\n{new_user}, {password}\n')
            print("\nNew user added successfully!")
            
    else:
        print("You do not have permission to register new users.")

# This function allows the admin to assign tasks to users. It checks if username is found in user.txt and if so, adds tasks details to tasks.txt
def add_task(username):
    if username == 'admin':
        assigned_to = input("\nEnter username of person task is assigned to: ")
        with open('user.txt', 'r') as f:
            contents = f.read()
            users = contents.split("\n")
            found = False
            for user in users:
                if ',' in user:
                    username, password = user.split(',', maxsplit=1)
                    username = username.strip()
                    password = password.strip()
                    if assigned_to == username:
                        found = True
                        break
            if found:
                title = input("Enter task name: ")
                description = input("Enter task description: ")
                due_date = input("Enter task due date: ")
                current_date = datetime.datetime.now().strftime('%d/%m/%Y')
                with open('tasks.txt', 'a') as file:
                    file.write(f"{assigned_to}, {title}, {description}, {current_date}, {due_date}, No\n")
                    print("\nTask added successfully!")
                    # refresh the contents of the file
                    with open('tasks.txt', 'r') as file:
                        contents = file.read()
            else:
                print(f"\nUser '{assigned_to}' does not exist.")
    else:
        print("You do not have permission to add tasks.")

# This function prints the contents of tasks.txt in an organised way, allowing the user to see all existing tasks
def view_all_tasks():
    with open('tasks.txt', 'r') as tasks_read:
        data = tasks_read.readlines()
        for pos, line in enumerate(data, 1):
            split_data = line.split(', ')
            try:
                output = f'──────[{pos}]──────\n'
                output += '\n'
                output += f'Assigned to: \t\t{split_data[0]}\n'
                output += f'Task: \t\t\t{split_data[1]}\n'
                output += f'Description: \t\t{split_data[2]}\n'
                output += f'Assigned Date: \t\t{split_data[3]}\n'
                output += f'Due Date: \t\t{split_data[4]}\n'
                output += f'Is completed: \t\t{split_data[5].strip()}\n'
                output += '\n'
                output += '────────────\n'
            except IndexError:
                continue

            print(output)

#### nie moge ogarnac tej funkcji za chuja, zle edytuje tasks. txt. usuwa wartosc. pogubilem sie!
## Do not use polish language in source files. It's very bad practice. Every dev must know english enough to understand.
# This function allows the user to view their tasks and edit them.
def view_my_tasks(logged_in_user):
    def edit_task(task, field, new_value):
        data = task.split(', ')
        data[field] = new_value
        return ', '.join(data)

    with open('tasks.txt', 'r') as tasks_read:
        data = tasks_read.readlines()
        my_tasks = []
        for line in data:
            if line.startswith(logged_in_user + ', '):
                my_tasks.append(line)

        if my_tasks:
            for pos, line in enumerate(my_tasks, 1):
                split_data = line.split(', ')
                output = f'──────[{pos}]──────\n'
                output += '\n'
                output += f'Assigned to: \t\t{split_data[0]}\n'
                output += f'Task: \t\t\t{split_data[1]}\n'
                output += f'Description: \t\t{split_data[2]}\n'
                output += f'Assigned Date: \t\t{split_data[3]}\n'
                output += f'Due Date: \t\t{split_data[4]}\n'
                output += f'Is completed: \t\t{split_data[5]}\n'
                output += '\n'
                output += '────────────\n'
                print(output)

            with open('user.txt', 'r') as f:
                contents = f.read()
                users = [line.split(',')[0].strip() for line in contents.split('\n') if line]

            task_number = input("Enter the number of the task you want to mark as complete or edit (or -1 to go back): ")
            if task_number != "-1":
                task_number = int(task_number)
                task = my_tasks[task_number - 1]
                split_data = task.split(', ')

                if split_data[5].strip() == "Yes":
                    print("Task is already marked as complete and cannot be edited.")
                    return

                complete = input("Mark as complete? (yes/no): ")
                if complete == 'yes':
                    my_tasks[task_number - 1] = edit_task(task, 5, 'Yes\n')
                    with open('tasks.txt', 'w') as tasks_write:
                        tasks_write.writelines(my_tasks)
                    print("Task marked as complete.")
                    view_my_tasks(logged_in_user)
                else:
                    edit_field = input("Enter 0 to edit 'Assigned to' or 4 to edit 'Due date': ")
                    if edit_field == '0':
                        new_value = input(f"Enter the new value for 'Assigned to': ")
                        if new_value in users:
                            assigned_to, task, description, assigned_date, due_date, is_completed = task.split(', ')
                            updated_task = f"Assigned to: {new_value}, Task: {task}, Description: {description}, Assigned Date: {assigned_date}, Due Date: {due_date}, Is completed: {is_completed}"
                            my_tasks[task_number - 1] = updated_task
                            with open('tasks.txt', 'w') as tasks_write:
                                tasks_write.writelines(my_tasks)
                            print("Assigned to value updated.")
                            view_my_tasks(logged_in_user)
                        else:
                            print("Invalid user")
                    elif edit_field == '4':
                        new_value = input(f"Enter the new value for 'Due date': ")
                        assigned_to, task, description, assigned_date, due_date, is_completed = task.split(', ')
                        updated_task = f"Assigned to: {assigned_to}, Task: {task}, Description: {description}, Assigned Date: {assigned_date}, Due Date: {new_value}, Is completed: {is_completed}"
                        my_tasks[task_number - 1] = updated_task
                        with open('tasks.txt', 'w') as tasks_write:
                            tasks_write.writelines(my_tasks)
                        print("Due date updated.")
                        view_my_tasks(logged_in_user)
                    else:
                        print("Invalid field")
            else:
                return


def generate_reports():
    total_tasks = 0
    completed_tasks = 0
    uncompleted_tasks = 0
    total_overdue_tasks = 0
    tasks_uncomplete_percentage = 0.0
    tasks_complete_percentage = 0.0
    tasks_overdue_percentage = 0.0
    total_users = 0
    with open('user.txt', 'r') as f:            #get tasks. you used tasks as a argument of method, but you didn't had initialized any variables with these values
        contents = f.read()
        users = contents.split("\n")
        users.pop()
    total_users = len(users)
    with open('tasks.txt', 'r') as f:           #this same like above
        contents = f.read()
        tasks = contents.split("\n")
        tasks.pop()
    total_tasks = len(tasks)
    for task in tasks:                          #check is task complete by checking is exist string "Yes" in whole task string
        is_completed = task.rsplit(',', 1)[-1]  #extract last item from this line of string
        if "Yes" in is_completed:
            completed_tasks += 1
        else:
            uncompleted_tasks += 1

    tasks_complete_percentage = ( completed_tasks / total_tasks ) * 100         #process values not there where you want to display something, but create variables. it's easier to read and understand the invention of code
    tasks_uncomplete_percentage = ( uncompleted_tasks / total_tasks ) * 100
    task_overview = []
    task_overview.append(f"Total number of tasks: {total_tasks}")
    task_overview.append(f"Total number of completed tasks: {completed_tasks}")
    task_overview.append(f"Total number of uncompleted tasks: {uncompleted_tasks}")
    task_overview.append(f"Total number of overdue tasks: {total_overdue_tasks}")
    task_overview.append(f"Percentage of tasks that are incomplete: {tasks_uncomplete_percentage}%")
    task_overview.append(f"Percentage of tasks that are overdue: {tasks_overdue_percentage}%")

    with open("task_overview.txt", "w+") as file:
        file.write("\n".join(task_overview))

    user_overview = []
    user_overview.append(f"Total number of users: {total_users}")
    user_overview.append(f"Total number of tasks: {total_tasks}")
    for user in users:
        total_tasks = 0
        completed_tasks = 0
        uncompleted_tasks = 0
        total_overdue_tasks = 0
        tasks_uncomplete_percentage = 0.0
        tasks_complete_percentage = 0.0
        tasks_overdue_percentage = 0.0
    #    user_overview.append(f"\nUser: {user['name']}")
    #    user_overview.append(f"Total number of tasks assigned to user: {len(user_tasks)}")
    #    user_overview.append(f"Percentage of tasks assigned to user: {len(user_tasks) / len(tasks) * 100}%")
    #    completed_user_tasks = [task for task in user_tasks if task["status"] == "completed"]
        user_overview.append(f"Percentage of completed tasks assigned to user: {tasks_complete_percentage}%")
    #    uncompleted_user_tasks = [task for task in user_tasks if task["status"] != "completed"]
        user_overview.append(f"Percentage of uncompleted tasks assigned to user: {tasks_uncomplete_percentage}%")
    #    overdue_user_tasks = [task for task in uncompleted_user_tasks if task["due_date"] < datetime.now()]
    #    user_overview.append(f"Percentage of overdue tasks assigned to user: {len(overdue_user_tasks) / len(user_tasks) * 100}%")

    with open("user_overview.txt", "w+") as file:
        file.write("\n".join(user_overview))

# This part of the code shows the user two different menus and options depending on whether the logged in user is the admin or not.
while True:
    print("\n╔══════════════════════════════════════╗")
    # Non-admin user options
    if not is_admin:
        print("║ Select one of the following options: ║")
        print("╠══════════════════════════════════════╣")
        print("║ va - View all tasks                  ║")
        print("║ vm - View my tasks                   ║")
        print("║ e - Exit                             ║")
        print("╚══════════════════════════════════════╝")
        menu = input(": ").lower()
    # Admin user options
    else:
        print("║ Select one of the following options: ║")
        print("╠══════════════════════════════════════╣")
        print("║ r - Registering a user               ║")
        print("║ a - Adding a task                    ║")
        print("║ s - View statistics                  ║")
        print("║ va - View all tasks                  ║")
        print("║ vm - View my tasks                   ║")
        print("║ gr - Generate reports                ║")
        print("║ e - Exit                             ║")
        print("╚══════════════════════════════════════╝")
        menu = input(": ").lower()

# I said you before, that You have to use if-elif-else, not just single ifs and else to the last if
# The code that follows allows the selection of a particular menu item and calls the relevant function
# Avoid nesting if statements. That's what operators like And or Or should be used for. Something like that it neither efficient or comfortable to read.
    if menu == 's' and is_admin:
        print_statistics()
    elif menu == 'r' and is_admin:
        register_user(logged_in_user)
    elif menu == 'a' and is_admin:
        add_task(logged_in_user)
    elif menu == 'va':
        view_all_tasks()
    elif menu == 'vm':
        view_my_tasks(logged_in_user)
    elif menu == 'e':
        print("\nGoodbye!")
        break
    elif menu == 'gr' and is_admin:
        generate_reports()
    else:
    	print("\nInvalid input. Please try again.")
