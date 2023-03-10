from os import path
import re
import random
import string
from datetime import datetime
import pytz

from django.shortcuts import render
from django.http import HttpResponseRedirect

from scripts.core.Script import Script
from scripts.core.Shell import Shell
from scripts.core.script_manager import Manager
from scripts.forms import Value_form, Choice_form
from scripts.models import ScriptRecord

THIS_DIR = path.dirname(path.abspath(__file__))
shell = Shell()
manager = Manager(path.join(THIS_DIR, 'scriptbank'))

def get_random_id():
    length = 10
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def script_list(request):
   #list_of_path = manager.script_list
   list_of_path = manager.get_script_list_for_field('Demo')
   ID = [manager.script_ID[i] for i in list_of_path]
   list_of_name = [manager.script_name[i] for i in list_of_path]
   list_of_description = [manager.script_description[i] for i in list_of_path]
   list_of_category = [manager.script_category[i] for i in list_of_path]
   list_of_codelock = [manager.script_codelock[i] for i in list_of_path]
   script_book = zip(ID, list_of_name, list_of_description, list_of_path,list_of_category, list_of_codelock)
   number_of_scripts = len(list_of_path)
   return render(request, 'scriptlist.html',
                 {'script_book': script_book,
                  'number_of_scripts': number_of_scripts})

def report(request, script_ID):
   #global script_dict
   script = Script()
   shell.assign_code(script)
   #---
   script_ID = int(script_ID) # this is permanent script ID
   script_path = manager.give_me_path_for_ID(script_ID)
   script.openFile(script_path)
   #---
   script.script_id = get_random_id() # this is temporary id for user that use this script
   script.name = manager.script_name[script_path]
   ScriptRecord.objects.create(script_id=script.script_id,
                               name = script.name,
                               code = script.code_oryginal,
                               path = script.script_path,
                               last_time_used = str(datetime.now(tz=pytz.timezone('Europe/Warsaw'))))
   #---
   script.parse()
   shell.run_parsed()
   return render(request, 'report.html', {'report': shell.report_html, 'script': script})

def source(request, script_ID):
   script_ID = int(script_ID) # this is permanent script ID
   script_path = manager.give_me_path_for_ID(script_ID)
   #---
   script = Script()
   script.name = manager.script_name[script_path]
   script.openFile(script_path)
   if manager.script_codelock[script_path]:
       script.code_oryginal = '>>>>> Sorry, but this source code is protected <<<<<'
   #---
   return render(request, 'source.html', {'script': script})

def report_show(request):
    # --data from request
    data = path.basename(request.META.get('PATH_INFO', None))
    script_id = data.split(';')[0]
    script_id = script_id.replace('script_id', '')
    # --build script
    script = Script()
    db_record = ScriptRecord.objects.get(script_id=script_id)
    script.script_id = db_record.script_id
    script.name = db_record.name
    script.code_oryginal = db_record.code
    script.script_path = db_record.path
    shell.assign_code(script)
    # ---run script to get html
    if db_record.html_tmp_holder == 'None':
        script.parse()
        shell.run_parsed()
    else:
        shell.report_html = db_record.html_tmp_holder
        db_record.html_tmp_holder = 'None'
        db_record.save()
    return render(request, 'report.html', {'report': shell.report_html, 'script': script})

def report_edit(request):
    # --data from request
    data = request.META.get('PATH_INFO', None)
    data = data.replace('/scripts/report/', '')
    script_id = data.split(';')[0]
    script_id = script_id.replace('script_id', '')
    line_id = data.split(';')[1]
    setvalues = data.split(';')[2]
    if setvalues == 'None':
        setvalues = None
    # ---------unzipping--------
    if setvalues:
        import zlib
        import binascii
        setvalues = eval(setvalues)
        setvalues = binascii.a2b_hex(setvalues)
        setvalues = zlib.decompress(setvalues)
        setvalues = setvalues.decode('UTF-8')
    # -------------------------
    index = data.split(';')[3]
    # --build script
    script = Script()
    db_record = ScriptRecord.objects.get(script_id=script_id)
    script.script_id = db_record.script_id
    script.name = db_record.name
    script.code_oryginal = db_record.code
    script.script_path = db_record.path
    shell.assign_code(script)
    # --getting data about variable to be edited
    script_code = script.code_oryginal
    # ---
    script_code = re.sub(r'#(<{2,})', r"#\1_idx_", script_code)
    no = 1
    while re.search(r"#<{2,}_idx_", script_code):
        script_code = script_code.replace(r'<_idx_', r"<_id%s_" % no, 1)
        no += 1
    expresion = re.search(r'(\w+)\s*=\s*(.+)\s*#<{2,}_%s_' % line_id, script_code)
    variable = expresion.group(1)
    old_value = expresion.group(2)
    old_value = old_value.rstrip()
    #---------------------------
    if old_value in ('True', 'False'):
        try:
            # ---update scripy to new value
            script.editCode(line_id, setvalues, index)
            # ---run script to get html
            script.parse()
            shell.run_parsed()
        except Exception as e:
            massage = 'Error - ' + str(e)
            return render(request, 'edit_error.html', {'data': data,
                                                       'script_id': script_id,
                                                       'massage': massage,
                                                       'script': script})
        # ---save updated code
        db_record.last_time_used = str(datetime.now(tz=pytz.timezone('Europe/Warsaw')))
        db_record.code = script.code_oryginal
        db_record.html_tmp_holder = shell.report_html
        db_record.save()
        # ---display report
        return HttpResponseRedirect('/scripts/report/script_id%s' % script_id)

    if request.method == 'POST' :
       #---what is new data from form
       form = Value_form(request.POST)
       new_value = form['value'].value()
       try :
           #---update scripy to new value
           script.editCode(line_id, setvalues, index, new_value = new_value)
           #---run script to get html
           script.parse()
           shell.run_parsed()
       except Exception as e:
           massage = 'Error - ' + str(e)
           return render(request, 'edit_error.html', {'data': data,
                                                      'script_id': script_id,
                                                      'massage': massage,
                                                      'script': script})
       #---save updated code
       db_record.last_time_used = str(datetime.now(tz=pytz.timezone('Europe/Warsaw') ))
       db_record.code = script.code_oryginal
       db_record.html_tmp_holder = shell.report_html
       db_record.save()
       #---display report
       return HttpResponseRedirect('/scripts/report/script_id%s'%script_id)
    else:
        if setvalues:
            setvalues = re.search(r'[[](.+)[]]', setvalues).group(1)
            setvalues = setvalues.replace("'", "")
            setvalues = setvalues.split(', ')
            #---
            expresion = re.search(r'(\w+)\s*=\s*(\w+)\s*[[](\d+)[]]\s*#<{2,}_%s_'%line_id, script_code)
            variable = expresion.group(1)
            listindex = int(expresion.group(3))
            #---
            form = Choice_form()
            form.fields['value'].label = variable + ' = '
            choices = [(setvalues[i], setvalues[i]) for i in range(len(setvalues))]
            form.fields['value'].choices = choices
            form.fields['value'].initial = choices[listindex][0]
            return render(request, 'edit_form.html', {'form': form, 'script': script})
        else:
            #---
            expresion = re.search(r'(\w+)\s*=\s*(.+)\s*#<{2,}_%s_' % line_id, script_code)
            variable = expresion.group(1)
            oldvalue = expresion.group(2)
            oldvalue = oldvalue.rstrip()  # for now this hotfix delete whitespace from the end of oldvalue string
            #---
            form = Value_form()
            form.fields['value'].label = variable + ' = '
            form.fields['value'].initial = oldvalue
            return render(request, 'edit_form.html', {'form': form, 'script': script})