import pytest
from app.services import (
    create_user, get_users,
    create_task, get_tasks,
    users, tasks
)

# ======================
# FIXTURE: reset dữ liệu
# ======================
@pytest.fixture(autouse=True)
def reset_data():
    users.clear()
    tasks.clear()


# ======================
# USER TEST
# ======================

def test_create_user_success():
    user = create_user("An")

    assert user["name"] == "An"
    assert user["id"] == 1
    assert len(users) == 1


def test_create_user_multiple():
    create_user("An")
    create_user("Binh")

    assert len(users) == 2
    assert users[1]["name"] == "Binh"


def test_create_user_empty_name():
    with pytest.raises(ValueError) as exc:
        create_user("")

    assert str(exc.value) == "Name is required"


def test_create_user_none_name():
    with pytest.raises(ValueError):
        create_user(None)


def test_get_users_empty():
    result = get_users()

    assert isinstance(result, list)
    assert len(result) == 0


def test_get_users_after_insert():
    create_user("An")
    create_user("Binh")

    result = get_users()

    assert len(result) == 2


# ======================
# TASK TEST
# ======================

def test_create_task_success():
    create_user("An")

    task = create_task("Task 1", 1)

    assert task["title"] == "Task 1"
    assert task["user_id"] == 1
    assert task["id"] == 1


def test_create_task_missing_title():
    create_user("An")

    with pytest.raises(ValueError) as exc:
        create_task("", 1)

    assert str(exc.value) == "Title is required"


def test_create_task_none_title():
    create_user("An")

    with pytest.raises(ValueError):
        create_task(None, 1)


def test_create_task_missing_user_id():
    create_user("An")

    with pytest.raises(ValueError) as exc:
        create_task("Task 1", None)

    assert str(exc.value) == "User ID is required"


def test_create_task_invalid_user_id():
    with pytest.raises(ValueError) as exc:
        create_task("Task 1", 999)

    assert str(exc.value) == "User ID does not exist"


def test_get_tasks_empty():
    result = get_tasks()

    assert isinstance(result, list)
    assert len(result) == 0


def test_get_tasks_after_insert():
    create_user("An")

    create_task("Task 1", 1)
    create_task("Task 2", 1)

    result = get_tasks()

    assert len(result) == 2
    assert result[0]["title"] == "Task 1"