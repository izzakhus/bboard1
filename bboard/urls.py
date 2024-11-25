from django.urls import re_path, path

from bboard.views import index, by_rubric, BbCreateView, add, add_save, add_and_save

app_name = 'bboard'

# vals = {'mode': 'index'}

urlpatterns = [
    path('add/', BbCreateView.as_view(), name='add'),
    path('add/save/', add_save, name='add_save'),
    path('add/', add, name='add'),
    path('add/', add_and_save, name='add'),
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('', index, name='index'),


    # re_path(r'^add/$', BbCreateView.as_view(), name='add'),
    # re_path(r'^(?P<rubric_id>[0-9]*)/$', by_rubric, name='by_rubric')
    # re_path('^$', index, name='index'),
]
