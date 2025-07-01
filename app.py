import json
from datetime import datetime, timedelta

TASKS_FILE = "tasks.txt"

class Task:
    def __init__(self, description, due_date, priority, completed=False):
        self.description = description 
        self.due_date = due_date  
        self.priority = int(priority) 
        self.completed = completed

    def to_dict(self):
        return {
            'description': self.description,
            'due_date': self.due_date,
            'priority': self.priority,
            'completed': self.completed
        }

    @staticmethod
    def from_dict(data):
        return Task(data['description'], data['due_date'], data['priority'], data['completed'])

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump([task.to_dict() for task in tasks], f, indent=4)

def load_tasks():
    try:
        with open(TASKS_FILE, 'r') as f:
            return [Task.from_dict(t) for t in json.load(f)]
    except FileNotFoundError:
        return []

def add_task(tasks):
    description = input("Task description: ")
    due_date = input("Due date (YYYY-MM-DD): ")
    priority = input("Priority (1=High, 2=Medium, 3=Low): ")
    task = Task(description, due_date, priority)
    tasks.append(task)
    print("✅ Task added.")

def view_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return []
    tasks_sorted = sorted(tasks, key=lambda t: (t.priority, t.due_date))
    for idx, task in enumerate(tasks_sorted, 1):
        status = "✅" if task.completed else "❌"
        print(f"{idx}. [{status}] {task.description} (Due: {task.due_date}, Priority: {task.priority})")
    return tasks_sorted

def mark_complete(tasks):
    tasks_sorted = view_tasks(tasks)
    if not tasks_sorted:
        return
    try:
        task_number = int(input("Enter task number to mark as complete: "))
        if 0 < task_number <= len(tasks_sorted):
            tasks_sorted[task_number - 1].completed = True
            print("✅ Task marked as complete.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def edit_task(tasks):
    tasks_sorted = view_tasks(tasks)
    if not tasks_sorted:
        return
    try:
        task_number = int(input("Enter task number to edit: "))
        if 0 < task_number <= len(tasks_sorted):
            task = tasks_sorted[task_number - 1]
            print("Leave blank to keep current value.")
            new_desc = input(f"New description (current: {task.description}): ") or task.description
            new_due = input(f"New due date (YYYY-MM-DD, current: {task.due_date}): ") or task.due_date
            new_prio = input(f"New priority (1-3, current: {task.priority}): ") or task.priority
            task.description = new_desc
            task.due_date = new_due
            task.priority = int(new_prio)
            print("✏️ Task updated.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def delete_task(tasks):
    tasks_sorted = view_tasks(tasks)
    if not tasks_sorted:
        return
    try:
        task_number = int(input("Enter task number to delete: "))
        if 0 < task_number <= len(tasks_sorted):
            task_to_remove = tasks_sorted[task_number - 1]
            tasks.remove(task_to_remove)
            print("🗑️ Task deleted.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def search_tasks(tasks):
    keyword = input("Enter keyword to search: ").lower()
    matches = [t for t in tasks if keyword in t.description.lower()]
    if not matches:
        print("🔍 No tasks found with that keyword.")
        return
    print("🔍 Search results:")
    for i, task in enumerate(matches, 1):
        status = "✅" if task.completed else "❌"
        print(f"{i}. [{status}] {task.description} (Due: {task.due_date}, Priority: {task.priority})")

def show_reminders(tasks):
    today = datetime.today().date()
    upcoming = []
    overdue = []

    for task in tasks:
        try:
            due_date = datetime.strptime(task.due_date, "%Y-%m-%d").date()
            if not task.completed:
                if due_date < today:
                    overdue.append(task)
                elif due_date <= today + timedelta(days=3):
                    upcoming.append(task)
        except ValueError:
            continue  # Skip invalid dates

    if overdue:
        print("\n⚠️ Overdue Tasks:")
        for task in overdue:
            print(f"❌ {task.description} (Due: {task.due_date})")

    if upcoming:
        print("\n📆 Upcoming Tasks (within 3 days):")
        for task in upcoming:
            print(f"📌 {task.description} (Due: {task.due_date})")

    if not overdue and not upcoming:
        print("🎉 No overdue or upcoming tasks!")

def main():
    tasks = load_tasks()
    while True:
        print("\n--- TO-DO LIST MANAGER ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Complete")
        print("4. Edit Task")
        print("5. Delete Task")
        print("6. Search Tasks")
        print("7. Show Reminders")
        print("8. Save Tasks")
        print("9. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            mark_complete(tasks)
        elif choice == '4':
            edit_task(tasks)
        elif choice == '5':
            delete_task(tasks)
        elif choice == '6':
            search_tasks(tasks)
        elif choice == '7':
            show_reminders(tasks)
        elif choice == '8':
            save_tasks(tasks)
            print("💾 Tasks saved.")
        elif choice == '9':
            save_tasks(tasks)
            print("👋 Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
