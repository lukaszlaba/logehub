from django.shortcuts import render

from scripts.views import manager

def home(request):
   list_of_path = manager.get_script_list_for_field('Structure')
   ID = [manager.script_ID[i] for i in list_of_path]
   list_of_name = [manager.script_name[i] for i in list_of_path]
   list_of_description = [manager.script_description[i] for i in list_of_path]
   list_of_category = [manager.script_category[i] for i in list_of_path]

   script_book = zip(ID, list_of_name, list_of_description, list_of_path,list_of_category)
   number_of_scripts = len(list_of_path)

   return render(request, 'xbeam_home.html',
                 {'script_book': script_book,
                  'number_of_scripts': number_of_scripts}
                 )

def contact(request):
   return render(request, 'xbeam_contact.html')

def about(request):
   return render(request, 'xbeam_about.html')