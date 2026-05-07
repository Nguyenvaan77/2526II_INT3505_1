import pytest
from app import create_app

@pytest.fixture(autouse=True)
def reset_data():
    from app.services import users, tasks
    users.clear()
    tasks.clear()

@pytest.fixture
def client():
    app = create_app()
    return app.test_client()


# ======================
# USER TEST
# ======================

def test_create_user_success(client):
    response = client.post("/users", json={"name": "An"})

    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "An"
    assert "id" in data


def test_create_user_empty_name(client):
    response = client.post("/users", json={"name": ""})

    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_create_user_missing_name(client):
    response = client.post("/users", json={})

    assert response.status_code == 400

def test_get_users_after_insert(client):
    client.post("/users", json={"name": "An"})
    client.post("/users", json={"name": "Binh"})

    response = client.get("/users")

    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2


# ======================
# TASK TEST
# ======================

def test_create_task_success(client):
    client.post("/users", json={"name": "An"})

    response = client.post("/tasks", json={
        "title": "Task 1",
        "user_id": 1
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Task 1"
    assert data["user_id"] == 1


def test_create_task_missing_title(client):
    client.post("/users", json={"name": "An"})

    response = client.post("/tasks", json={
        "user_id": 1
    })

    assert response.status_code == 400


def test_create_task_empty_title(client):
    client.post("/users", json={"name": "An"})

    response = client.post("/tasks", json={
        "title": "",
        "user_id": 1
    })

    assert response.status_code == 400


def test_create_task_missing_user_id(client):
    response = client.post("/tasks", json={
        "title": "Task 1"
    })

    assert response.status_code == 400


def test_create_task_invalid_user_id(client):
    response = client.post("/tasks", json={
        "title": "Task 1",
        "user_id": 999
    })

    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data



def test_get_tasks_after_insert(client):
    client.post("/users", json={"name": "An"})

    client.post("/tasks", json={
        "title": "Task 1",
        "user_id": 1
    })

    client.post("/tasks", json={
        "title": "Task 2",
        "user_id": 1
    })

    response = client.get("/tasks")

    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2


# ======================
# INTEGRATION TEST
# ======================

# def test_user_task_flow(client):
#     # tạo user
#     user_res = client.post("/users", json={"name": "An"})
#     user_id = user_res.get_json()["id"]

#     # tạo task
#     task_res = client.post("/tasks", json={
#         "title": "Task Integration",
#         "user_id": user_id
#     })

#     assert task_res.status_code == 201

#     # lấy task
#     tasks_res = client.get("/tasks")
#     tasks = tasks_res.get_json()

#     assert any(t["title"] == "Task Integration" for t in tasks)