from os import path

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from scripts.core.Script import Script
from scripts.core.Shell import Shell
from scripts.models import ScriptRecord
from scripts.forms import NameForm

import random
import uuid
import string

def get_random_id(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

shell = Shell()

script_dict = {}

def report(request, script_id):
   script = Script()
   shell.assign_code(script)
   #---
   script.code_oryginal = get_object_or_404(ScriptRecord, pk=script_id).code
   script.name = get_object_or_404(ScriptRecord, pk=script_id).name
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
   return render(request, 'scriptlist.html', {'scripts': all_scripts})