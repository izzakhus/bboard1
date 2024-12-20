from django.urls import path

from todolist.views import todo_list, todo_detail, todo_create, todo_update, todo_delete, TaskListView, TaskDetailView, TaskDeleteView
app_name = 'todolist'

urlpatterns = [
    path('', todo_list, name='todo_list'),
    path('<int:todo_id>/', todo_detail, name='todo_detail'),
    path('create/', todo_create, name='todo_create'),
    path('update/<int:todo_id>/', todo_update, name='todo_update'),
    path('delete/<int:todo_id>/', todo_delete, name='todo_delete'),


    path('', TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),

]
