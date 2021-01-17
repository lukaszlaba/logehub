from django.http import HttpResponse

def hello(request):
   text = """<h1>welcome to my apAp !</h1>"""
   return HttpResponse(text)

def index(request):
   text = """
   <h1>Logehub start page !</h1>
   <a href="/scripts/list/" > Go to script list </a>
   """
   return HttpResponse(text)

