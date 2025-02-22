from django.urls import path
from . import views
from testapp.views import test_cookie, test_mail

app_name = 'testapp'

urlpatterns = [
    path('cookie/', test_cookie, name='test_cookie'),
    path('email/', test_mail, name='test_mail'),
    path('populate/', views.populate_data, name='populate_data'),
    path('courses-students/', views.course_students, name='course_students'),
]