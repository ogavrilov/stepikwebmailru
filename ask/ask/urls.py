"""ask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.urls import re_path
from qa import views

urlpatterns = [
    path('', views.question_list_latest, name='root'),
    re_path(r'^question/(?P<question_id>\d+)/', views.question_object, name='question'),
    re_path(r'^login', views.test, name='login'),
    re_path(r'^signup', views.test, name='signup'),
    re_path(r'^ask', views.askform, name='ask'),
    re_path(r'^popular', views.question_list_popular, name='popular'),
    re_path(r'^new', views.question_list_latest, name='new')
]
