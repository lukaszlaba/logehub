from os import path

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from scripts.core.Script import Script
from scripts.core.Shell import Shell
from scripts.core.script_manager import Manager

from scripts.models import ScriptRecord
from scripts.forms import NameForm

import random
import uuid
import string

import time

THIS_DIR = path.dirname(path.abspath(__file__))


def get_random_id(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

shell = Shell()
print(path.join(THIS_DIR, 'scriptbank'), '<<<<<<<<<<<<<<<<<<<,,,')
manager = Manager(path.join(THIS_DIR, 'scriptbank'))

script_dict = {}

def report(request, script_id):
   script = Script()
   shell.assign_code(script)
   #---
   print(script_id)
   script_path = manager.script_list[int(script_id)]
   print(script_path)
   script.openFile(script_path)
   #script.code_oryginal = get_object_or_404(ScriptRecord, pk=script_id).code
   #script.name = get_object_or_404(ScriptRecord, pk=script_id).name
   #---
   script.script_id = get_random_id(7)
   script_dict[script.script_id] = script
   #---
   script.parse()
   shell.run_parsed()
   return render(request, 'report.html', {'report': shell.report_html, 'script': script})

def report_edit(request):
   data = path.basename(request.META.get('PATH_INFO', None))
   script_id = data.split(';')[0]
   script_id = script_id.replace('script_id', '')
   line_id = data.split(';')[1]
   setvalues = data.split(';')[2]
   index = data.split(';')[3]
   print(script_id, line_id, setvalues, index)
   #----
   try:
      script = script_dict[script_id]
   except:
      time.sleep(3)
      script = script_dict[script_id]
   shell.assign_code(script)
   #---
   script.editCode(line_id, setvalues, index)
   #except process needed here
   #---
   script.parse()
   shell.run_parsed()
   return render(request, 'report.html', {'report': shell.report_html, 'script': script})

def script_list(request):
   all_scripts = ScriptRecord.objects.all()

   ID = range(len(manager.script_list))
   list_of_path = manager.script_list
   list_of_name = [manager.script_name[i] for i in list_of_path]
   list_of_description = [manager.script_description[i] for i in list_of_path]

   script_book = zip(ID, list_of_name, list_of_description, list_of_path)
   number_of_scripts = len(list_of_path)

   return render(request, 'scriptlist.html',
                 {'scripts': all_scripts,
                  'script_book': script_book,
                  'number_of_scripts': number_of_scripts}
                 )