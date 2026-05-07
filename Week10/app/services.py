# Service functions go here
def example_service():
    return "Example service function"
# lưu trữ trên RAM
users = []
tasks = []

# USER
def create_user(name):
    if not name:
        raise ValueError("Name is required")

    user = {
        "id": len(users) + 1,
        "name": name
    }
    users.append(user)
    return user

def get_users():
    return users


# TASK
def create_task(title, user_id):
    if not title:
        raise ValueError("Title is required")
    if not user_id:
        raise ValueError("User ID is required")
    if user_id not in [user["id"] for user in users]:
        raise ValueError("User ID does not exist")

    task = {
        "id": len(tasks) + 1,
        "title": title,
        "user_id": user_id
    }
    tasks.append(task)
    return task

def get_tasks():
    return tasks