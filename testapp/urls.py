from django.urls import path

from testapp.views import get_comment, delete_comment

urlpatterns = [
    path('comments/', get_comment, name='get_comment'),
    path('<int:sms_id>/', delete_comment, name='delete_comment'),

]
path('comments/', get_comment)