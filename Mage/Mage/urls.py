"""Mage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.template.backends import django
from django.urls import path, include
from accounts import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("home/", views.EnteringView.as_view(), name="home_list"),
    path("register/", views.registerPage, name="register_page"),
    path("accounts/profile/", views.EnteringView.as_view()),
    path("home/succes",views.succes_view, name="succes_prompt"),
    path("accounts/logout/login", views.LoginView.as_view()),
    path('accounts/', include('django.contrib.auth.urls')),
    path("history/<int:pk>/", views.HistoryDetail, name="basket"),

]
