"""matchinfluence URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import re_path, path
from main import views

urlpatterns = [
	path('riot.txt/', views.verify, name = 'verify'),
        re_path(r'^summoner/(?P<summoner_name>[\w|\W]+)/', views.summonerSummary, name = 'summoner_summary'),	
        re_path(r'^match/(?P<match_id>[0-9]{10})/', views.matchDetails, name = 'match_details'),
        path('', views.search, name = 'search'),
]
