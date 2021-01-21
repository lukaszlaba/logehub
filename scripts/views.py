from os import path

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from scripts.core.Script import Script
from scripts.core.Shell import Shell
from scripts.core.script_manager import Manager


from scripts.models import ScriptRecord
from scripts.forms import NameForm


import random
import string
from datetime import datetime
import pytz

THIS_DIR = path.dirname(path.abspath(__file__))

def get_random_id(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

shell = Shell()
print(path.join(THIS_DIR, 'scriptbank'), '<<<<<<<<<<<<<<<<<<<,,,')
manager = Manager(path.join(THIS_DIR, 'scriptbank'))

#script_dict = {}

def report(request, script_id):
   global script_dict
   script = Script()
   shell.assign_code(script)
   #---
   script_path = manager.script_list[int(script_id)]
   script.openFile(script_path)
   #---
   script.script_id = get_random_id(7)
   script.name = manager.script_name[script_path]
   #script_dict[script.script_id] = script

   ScriptRecord.objects.create(script_id=script.script_id,
                               name = script.name,
                               code = script.code_oryginal,
                               path = script.script_path,
                               last_time_used = str(datetime.now(tz=pytz.timezone('Europe/Warsaw') ))
                               )
   #---
   script.parse()
   shell.run_parsed()
   return render(request, 'report.html', {'report': shell.report_html, 'script': script})

def report_edit(request):
   global script_dict
   data = path.basename(request.META.get('PATH_INFO', None))
   script_id = data.split(';')[0]
   script_id = script_id.replace('script_id', '')
   line_id = data.split(';')[1]
   setvalues = data.split(';')[2]
   index = data.split(';')[3]
   print(script_id, line_id, setvalues, index)
   #----
   script = Script()
   db_record = ScriptRecord.objects.get(script_id=script_id)

   script.script_id = db_record.script_id
   script.name = db_record.name
   script.code_oryginal = db_record.code
   script.script_path = db_record.path




   shell.assign_code(script)
   #---
   script.editCode(line_id, setvalues, index)
   #except process needed here
   #---
   script.parse()
   shell.run_parsed()

   db_record.last_time_used = str(datetime.now(tz=pytz.timezone('Europe/Warsaw') ))
   db_record.code = script.code_oryginal
   db_record.save()

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