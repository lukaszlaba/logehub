"""logeweb URL Configuration

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
from django.urls import path, include, re_path
from logeweb.views import index, contact, contribute, about
#from scripts.views import xbeam_home, xbeam_about, xbeam_contact

urlpatterns = [
    path('admin/', admin.site.urls),
    path('scripts/', include('scripts.urls')),
    re_path(r'^$', index, name='index'),
    path('contact/', contact, name='index'),
    path('contribute/', contribute, name='index'),
    path('about/', about, name='index'),
    path('xbeam/', include('xbeam.urls')),
]