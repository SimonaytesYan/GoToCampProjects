"""brain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from MyApp.views import *
from django.conf.urls.static import static


urlpatterns = [
    path('', lobby),
    path('startcourse/', indexcourse),
    path('startstudent/', index),
    path('student/', details),
    path('course/', detailscourse),
    path('add/', add),
    path('addcourse/', addcourse),
    path('edit/', edit),
    path('editcourse/', editcourse),
    path('delete', delete),
    path('deletecourse', deletecourse),
    
    path('logout/', logout_page),
    path('login/', login_page),
    path('register/', register),
    path('admin/', admin.site.urls),
]   + static('avatars/', document_root='avatars/')
