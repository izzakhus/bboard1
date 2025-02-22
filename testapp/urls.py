from django.urls import path

from testapp.views import test_cookie, test_mail
from . import views

app_name = 'testapp'

urlpatterns = [
    path('cookie/', test_cookie, name='test_cookie'),
    path('email/', test_mail, name='test_mail'),
    path('course-students/', views.course_students, name='course_students'),
]
