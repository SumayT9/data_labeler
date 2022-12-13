"""data_labeler_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from data_labeler import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("data_labeler/write/",views.train_wrapper, name="data_labeler"),
    path("data_labeler/set_field/",views.set_field, name="setname"),
    path("data_labeler/extract_text/",views.extract_text, name="gettext"),
    path("data_labeler/debug/",views.debug, name="debug")
]
