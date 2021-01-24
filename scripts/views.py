from os import path
import re

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from scripts.core.Script import Script
from scripts.core.Shell import Shell
from scripts.core.script_manager import Manager

from scripts.forms import NaszForm, Choice_form


from scripts.models import ScriptRecord

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
manager = Manager(path.join(THIS_DIR, 'scriptbank'))

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
   global script_dict #! <<<<<<<<<!!!!!!!!!!!!!!!!! delete
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

def nowy_form(request):
    if request.method == 'POST':
        form = NaszForm(request.POST)
        if form.is_valid():
            print('Form is valid')
        text = """
        <h1>Blallalala! %s</h1>
        """ %form['imie'].value()
        return HttpResponse(text)
    else:
        form = NaszForm()
        form.fields['imie'].initial = 'ala'
    return render(request, 'nasz_form.html', {'form': form})

def nowy_form_1(request):
    if request.method == 'POST':
        form = Choice_form(request.POST)
        if form.is_valid():
            print('Form is valid')
        text = """
        <h1>Blallalala! %s</h1>
        """ %form['value'].value()
        return HttpResponse(text)
    else:
        form = Choice_form()
        #form.fields['imi'].initial = 'ala'
    return render(request, 'nasz_form.html', {'form': form})

def report_edit_1(request):
    # --data from request
    data = path.basename(request.META.get('PATH_INFO', None))
    script_id = data.split(';')[0]
    script_id = script_id.replace('script_id', '')
    line_id = data.split(';')[1]
    setvalues = data.split(';')[2]
    if setvalues == 'None':
        setvalues = None
    index = data.split(';')[3]
    print(script_id, line_id, setvalues, index)

    # --build script
    script = Script()
    db_record = ScriptRecord.objects.get(script_id=script_id)
    script.script_id = db_record.script_id
    script.name = db_record.name
    script.code_oryginal = db_record.code
    script.script_path = db_record.path
    shell.assign_code(script)

    if request.method == 'POST':

       #---what is new data from form
       form = NaszForm(request.POST)
       new_value = form['imie'].value()

       #---update scripy to new value
       script.editCode(line_id, setvalues, index, new_value = new_value)
       #except process needed here

       #---run script to get html
       script.parse()
       shell.run_parsed()

       #---save updated code
       db_record.last_time_used = str(datetime.now(tz=pytz.timezone('Europe/Warsaw') ))
       db_record.code = script.code_oryginal
       db_record.save()

       #---display report
       return render(request, 'report.html', {'report': shell.report_html, 'script': script})

    else:
        # --geting data about variable to be edited
        script_code = script.code_oryginal
        #---
        script_code = re.sub(r'#(<{2,})', r"#\1_idx_", script_code)
        no = 1
        while re.search(r"#<{2,}_idx_", script_code):
            script_code = script_code.replace(r'<_idx_', r"<_id%s_" % no, 1)
            no += 1
        if setvalues:
            setvalues = re.search(r'[[](.+)[]]', setvalues).group(1)
            setvalues = setvalues.replace(" ", "")
            setvalues = setvalues.replace("'", "")
            setvalues = setvalues.split(',')
            #---
            expresion = re.search(r'(\w+)\s*=\s*(\w+)\s*[[](\d+)[]]\s*#<{2,}_%s_'%line_id, script_code)
            variable = expresion.group(1)
            listindex = int(expresion.group(3))
            #---
            form = Choice_form()
            form.fields['value'].label = variable + ' = '
            choices = [(str(i), setvalues[i]) for i in range(len(setvalues))]
            form.fields['value'].choices = choices
            return render(request, 'nasz_form.html', {'form': form})

        else:
            #---
            expresion = re.search(r'(\w+)\s*=\s*(.+)\s*#<{2,}_%s_' % line_id, script_code)
            variable = expresion.group(1)
            oldvalue = expresion.group(2)
            oldvalue = oldvalue.rstrip()  # for now this hotfix delete whitespace from the end of oldvalue string


            form = NaszForm()
            form.fields['imie'].label = variable + ' = '
            form.fields['imie'].initial = oldvalue
            return render(request, 'nasz_form.html', {'form': form})

