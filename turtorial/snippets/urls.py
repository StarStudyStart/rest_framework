#!/usr/bin/env python
# coding:utf-8
"""
Author  : yabinli
Time    : 2020/5/7 0007 22:27
"""

from django.urls import path
from snippets import views

urlpatterns = [
    path('snippet_list/', views.snippet_list, name='snippet_list'),
]
