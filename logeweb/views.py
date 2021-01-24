from django.http import HttpResponse

def hello(request):
   text = """<h1>welcome to my apAp !</h1>"""
   return HttpResponse(text)

def index(request):
   text = """
   <h1>Welocme to Logehub page !</h1>
   <a href="/scripts/list/" > <h3>Go to script list >></h3> </a>
   """
   return HttpResponse(text)
