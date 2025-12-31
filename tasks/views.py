from django.shortcuts import render
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .utils import execute_select, execute_query
import logging
from datetime import date

logger = logging.getLogger(__name__)


def task_page(request):
    return render(request, "tasks/index.html", {
        "today": date.today().isoformat()
    })


@api_view(['GET', 'POST'])
def task_list_create(request):

    if request.method == 'GET':
        try:
            tasks = execute_select("SELECT * FROM tasks_task")
            return Response(tasks)
        except Exception:
            logger.exception("Error in task_list_create")
            return Response(
                {"error": "Failed to fetch tasks"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    elif request.method == 'POST':
        try:
            data = request.data
            title = " ".join(data.get("title").split())
            description = data.get("description", "")
            due_date = data.get("due_date")
            status_val = data.get("status", "pending")
            existing = execute_select(
                "SELECT id FROM tasks_task WHERE title = %s AND due_date = %s",
                [title, due_date]
            )
            if existing:
                return Response(
                    {"error": "Task already exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            execute_query("""
                    INSERT INTO tasks_task (title, description, due_date, status)
                    VALUES (%s, %s, %s, %s)
                    """,
                    [title, description, due_date, status_val])
            return Response(
                {"message": "Task created"},
                status=status.HTTP_201_CREATED
            )
        except Exception:
            logger.exception("Error in task_list_create")
            return Response(
                {"error": "Failed to create task"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, pk):
    task = execute_select("SELECT * FROM tasks_task WHERE id = %s", [pk])
    if not task:
        return Response(
            {"error": "Task not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        return Response(task[0])

    elif request.method == 'PUT':
        try:
            data = request.data
            title = data.get("title", task[0]["title"])
            description = data.get("description", task[0]["description"])
            due_date = data.get("due_date", task[0]["due_date"])
            status_val = data.get("status", task[0]["status"])
            execute_query( """
                    UPDATE tasks_task
                    SET title=%s, description=%s, due_date=%s, status=%s
                    WHERE id=%s
                    """,[title, description, due_date, status_val, pk])
            return Response({"message": "Task updated"})
        except Exception:
            logger.exception("Error in task_detail")
            return Response(
                {"error": "Update failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    elif request.method == 'DELETE':
        try:
            execute_query("DELETE FROM tasks_task WHERE id=%s", [pk])
            return Response(
                {"message": "Task deleted"},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception:
            logger.exception("Error in task_detail")
            return Response(
                {"error": "Delete failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
