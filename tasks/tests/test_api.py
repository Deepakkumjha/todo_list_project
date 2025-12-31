from rest_framework.test import APIClient
from django.db import connection
from datetime import date
import pytest 

pytestmark = pytest.mark.django_db


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture(scope="session")
def setup_tasks_table(django_db_setup, django_db_blocker):
    """
    Create tasks_task table in pytest test database
    """
    with django_db_blocker.unblock():
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks_task (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    due_date TEXT,
                    status TEXT DEFAULT 'pending'
                )
            """)


@pytest.fixture
def create_task(setup_tasks_table):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO tasks_task (title, description, due_date, status)
            VALUES (%s, %s, %s, %s)
            """,
            ["Test Task", "Test Desc", date.today().isoformat(), "pending"]
        )
        return cursor.lastrowid


def test_get_tasks(client):
    response = client.get("/api/tasks/")
    assert response.status_code == 200


def test_create_task(client):
    payload = {
        "title": "Go to gym",
        "description": "Workout",
        "due_date": date.today().isoformat(),
        "status": "pending"
    }

    response = client.post("/api/tasks/", payload, format="json")
    assert response.status_code == 201


def test_update_task(client, create_task):
    payload = {
        "title": "Updated Task",
        "description": "Updated Desc",
        "due_date": date.today().isoformat(),
        "status": "done"
    }

    response = client.put(
        f"/api/tasks/{create_task}/",
        payload,
        format="json"
    )

    assert response.status_code == 200


def test_delete_task(client, create_task):
    response = client.delete(f"/api/tasks/{create_task}/")
    assert response.status_code == 204
