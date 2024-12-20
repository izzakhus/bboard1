from django.urls import path, re_path
from django.views.generic.dates import WeekArchiveView, DayArchiveView
from django.views.generic.edit import CreateView

from bboard.models import Bb
from bboard.views import (index, by_rubric, BbCreateView,
                          add_and_save, bb_detail, BbRubricBbsView,
                          BbDetailView, BbEditView, BbDeleteView, BbIndexView,
                          BbRedirectView, edit)

app_name = 'bboard'

urlpatterns = [
    # path('<int:year>/week/<int:week>/',
    #      WeekArchiveView.as_view(model=Bb, date_field='published',
    #                              context_object_name='bbs')),
    # path('<int:year>/<int:month>/<int:day>/',
    #      DayArchiveView.as_view(model=Bb, date_field='published',
    #                             month_format='%m',
    #                             context_object_name='bbs')),
    path('<int:year>/<int:month>/<int:day>/', BbRedirectView.as_view(),
         name='old_archive'),

    path('add/', BbCreateView.as_view(), name='add'),
    path('edit/<int:pk>/', BbEditView.as_view(), name='edit'),
    # path('edit/<int:pk>/', edit, name='edit'),

    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),

    path('<int:rubric_id>/', BbRubricBbsView.as_view(), name='by_rubric'),

    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),

    path('', index, name='index'),
    # path('', BbIndexView.as_view(), name='index'),

    # Маршруты с регулярными выражениями
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', BbRedirectView.as_view(), name='old_archive'),
    re_path(r'^edit/(?P<pk>\d+)/$', BbEditView.as_view(), name='edit'),
    re_path(r'^delete/(?P<pk>\d+)/$', BbDeleteView.as_view(), name='delete'),
    re_path(r'^(?P<rubric_id>\d+)/$', BbRubricBbsView.as_view(), name='by_rubric'),
    re_path(r'^detail/(?P<pk>\d+)/$', BbDetailView.as_view(), name='detail'),
]
