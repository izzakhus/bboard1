from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from .models import Task


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
