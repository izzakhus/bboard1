from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from testapp.models import Comment


def get_comment(request):
    comments = Comment.objects.all()
    comments


def delete_comment(request, sms_id):
