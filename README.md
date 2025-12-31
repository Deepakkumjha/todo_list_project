# To-Do List Application (APIs + Templates)

## Project Overview

This is a To-Do List web application built using Python and Django. The application provides RESTful APIs for managing tasks and uses HTML templates to render a simple web interface. As per the assignment instructions, Django ORM is NOT used and all database operations are performed using raw SQL queries.

## Tech Stack

- Python
- Django
- Django REST Framework
- SQLite
- Pytest

## Features

- Create, retrieve, update, and delete tasks using RESTful APIs
- Store tasks in an SQLite database
- HTML templates for displaying the task list and adding new tasks
- Logging and exception handling implemented
- Automated API testing using pytest
- No Django ORM or Generic ViewSets used

## Setup Instructions

1. Download the project or clone the repository:
   https://github.com/Deepakkumjha/todo_list_project.git

   Navigate to the project directory:
   cd todo_list_project

2. Create and activate virtual environment  
   python -m venv venv  
   source venv/bin/activate

3. Install dependencies  
   pip install -r requirements.txt

4. Run the application  
   python manage.py runserver

Application URL:  
http://127.0.0.1:8000/

## Database Setup

This project does not use Django ORM for application data.
The task table (`tasks_task`) is created using a raw SQL script.

Steps to set up the database:

1. Run Django migrations for internal tables (sessions, auth, etc.)
   python manage.py migrate

2. Create the tasks table using the provided SQL script
   python todo_list_project/setup_database.py

## API Documentation

# GET /api/tasks/

Response(200 OK):
[
{
"id": 1,
"title": "Go to gym",
"description": "Workout",
"due_date": "2025-01-10",
"status": "pending"
}
]

# POST /api/tasks/

Request Body:
{
"title": "Go to gym",
"description": "Workout",
"due_date": "2025-01-10",
"status": "pending"
}

Response(201 Created):
{
"message": "Task created"
}

# PUT /api/tasks/<id>/

Request Body:
{
"title": "Updated Task",
"description": "Updated description",
"due_date": "2025-01-12",
"status": "done"
}

Response(200 OK):
{
"message": "Task updated"
}

Response(404 Not Found):
{
"error": "Task not found"
}

# DELETE /api/tasks/<id>/

Response(204 No Content):
{
"message": "Task deleted"
}

Response(404 Not Found):
{
"error": "Task not found"
}

## Template Usage

Django templates are used to render the web interface. A page displays all tasks and a form is provided to add new tasks. All UI actions internally call the corresponding API endpoints.

## Testing

Automated tests are written using pytest and pytest-django.  
Run tests using:  
pytest

Tests cover create, retrieve, update, and delete task APIs.

## Assignment Compliance Summary

CRUD APIs implemented  
Raw SQL used (No ORM)  
Templates integrated with APIs  
Logging and exception handling implemented  
Pytest-based automated tests added  
API documentation provided
