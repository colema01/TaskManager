import json
from datetime import datetime
from tabulate import tabulate

TASK_FILE = "tasks.json"

# Load tasks from JSON file
def load_tasks():
    try:
        with open(TASK_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save tasks to JSON file
def save_tasks(tasks):
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# Add a new task
def add_task(tasks):
    print("\n--- Add Task ---")
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    priority = input("Enter priority (low/medium/high): ").lower()
    due_date = input("Enter due date (YYYY-MM-DD) [optional]: ")
    
    try:
        if due_date:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Task not added.")
        return

    task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_date or None,
        "completed": False
    }
    tasks.append(task)
    save_tasks(tasks)
    print("Task added successfully!")

# Display all tasks
def display_tasks(tasks, filters=None):
    print("\n--- Task List ---")
    filtered_tasks = tasks
    if filters:
        for key, value in filters.items():
            filtered_tasks = [task for task in filtered_tasks if task.get(key) == value]
    if not filtered_tasks:
        print("No tasks found.")
        return
    print(tabulate(filtered_tasks, headers="keys", tablefmt="grid"))

# Mark a task as completed
def mark_task_complete(tasks):
    print("\n--- Mark Task as Complete ---")
    task_id = input("Enter the task ID to mark as complete: ")
    try:
        task_id = int(task_id)
        for task in tasks:
            if task["id"] == task_id:
                task["completed"] = True
                save_tasks(tasks)
                print(f"Task ID {task_id} marked as complete!")
                return
        print(f"No task found with ID {task_id}.")
    except ValueError:
        print("Invalid task ID. Please enter a number.")

# Delete a task
def delete_task(tasks):
    print("\n--- Delete Task ---")
    task_id = input("Enter the task ID to delete: ")
    try:
        task_id = int(task_id)
        for task in tasks:
            if task["id"] == task_id:
                tasks.remove(task)
                save_tasks(tasks)
                print(f"Task ID {task_id} deleted successfully!")
                return
        print(f"No task found with ID {task_id}.")
    except ValueError:
        print("Invalid task ID. Please enter a number.")

# Update an existing task
def update_task(tasks):
    print("\n--- Update Task ---")
    task_id = input("Enter the task ID to update: ")
    try:
        task_id = int(task_id)
        for task in tasks:
            if task["id"] == task_id:
                print("Leave fields blank to keep the current value.")
                new_title = input(f"Enter new title [{task['title']}]: ") or task["title"]
                new_description = input(f"Enter new description [{task['description']}]: ") or task["description"]
                new_priority = input(f"Enter new priority [{task['priority']}]: ") or task["priority"]
                new_due_date = input(f"Enter new due date (YYYY-MM-DD) [{task['due_date']}] [optional]: ") or task["due_date"]
                
                if new_due_date:
                    try:
                        new_due_date = datetime.strptime(new_due_date, "%Y-%m-%d").strftime("%Y-%m-%d")
                    except ValueError:
                        print("Invalid date format. Update aborted.")
                        return
                
                task["title"] = new_title
                task["description"] = new_description
                task["priority"] = new_priority
                task["due_date"] = new_due_date
                save_tasks(tasks)
                print("Task updated successfully!")
                return
        print(f"No task found with ID {task_id}.")
    except ValueError:
        print("Invalid task ID. Please enter a number.")

# Filter tasks
def filter_tasks(tasks):
    print("\n--- Filter Tasks ---")
    print("1. Filter by priority")
    print("2. Filter by completion status")
    choice = input("Enter your choice: ")
    
    if choice == "1":
        priority = input("Enter priority to filter by (low/medium/high): ").lower()
        display_tasks(tasks, filters={"priority": priority})
    elif choice == "2":
        completed = input("Show only completed tasks? (yes/no): ").lower()
        display_tasks(tasks, filters={"completed": completed == "yes"})
    else:
        print("Invalid choice. Returning to menu.")

# Main menu loop
def main():
    tasks = load_tasks()

    while True:
        print("\n--- Task Manager Menu ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Mark Task as Complete")
        print("5. Delete Task")
        print("6. Filter Tasks")
        print("7. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            display_tasks(tasks)
        elif choice == "3":
            update_task(tasks)
        elif choice == "4":
            mark_task_complete(tasks)
        elif choice == "5":
            delete_task(tasks)
        elif choice == "6":
            filter_tasks(tasks)
        elif choice == "7":
            print("Exiting Task Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
