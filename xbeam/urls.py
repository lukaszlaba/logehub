from django.urls import path
from xbeam.views import home, about, contact

urlpatterns = [
    path('', home),
    path('home/', home),
    path('about/', about),
    path('contact/', contact),
]