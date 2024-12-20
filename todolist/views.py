from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from .models import Task


def todo_list(request):
    pass


def todo_detail(request, todo_id):
    pass


def todo_create(request):
    pass


def todo_update(request, todo_id):
    pass


def todo_delete(request, todo_id):
    pass


class TaskListView(ListView):
    model = Task
    template_name = 'todolist/task_list.html'
    context_object_name = 'tasks'


class TaskDetailView(DetailView):
    model = Task
    template_name = 'todolist/task_detail.html'
    context_object_name = 'task'


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'todolist/task_delete.html'
    success_url = reverse_lazy('task_list')
