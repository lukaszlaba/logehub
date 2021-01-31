from django.http import HttpResponse
from django.shortcuts import render

def index(request):
   #return render(request, 'startpage.html')
   return render(request, 'index_1.html')

def contact(request):
   #return render(request, 'startpage.html')
   return render(request, 'contact.html')

def contribute(request):
   #return render(request, 'startpage.html')
   return render(request, 'contribute.html')

def about(request):
   #return render(request, 'startpage.html')
   return render(request, 'about.html')