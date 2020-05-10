#!/usr/bin/env python
# coding:utf-8
"""
Author  : yabinli
Time    : 2020/5/7 0007 22:27
"""

from django.urls import path, include
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns

from snippets import views

urlpatterns = [
    # path('snippets/', views.snippet_list, name='snippet_list'),
    # path('snippets/<int:pk>/', views.snippet_detail, name='snippet_detail'),
    path('snippets/', views.SnippetListHigh.as_view()),
    path('snippets/<int:pk>/', views.SnippetDetailHigh.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG :
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns