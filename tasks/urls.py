from django.urls import path
from . import views

urlpatterns = [
    path("", views.task_page, name="index"),

    # APIs
    path("api/tasks/", views.task_list_create, name="api-task-list"),
    path("api/tasks/<int:pk>/", views.task_detail, name="api-task-detail"),
]
