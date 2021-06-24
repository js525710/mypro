"""mypro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from api.views import apitest001,apitest002,apitest003,apitest004,apitest005,apitest006

urlpatterns = [
    path('admin/', admin.site.urls),
    # 从根路径开始的路径
    path('apitest001/', apitest001),
    path('apitest002', apitest002),
    path('apitest03', apitest003),
    path('apitest004', apitest004),
    path('apitest005/', apitest005),
    path('apitest006', apitest006),
]
