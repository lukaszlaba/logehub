# -*- coding: utf-8 -*-
#-----------------------------------------------------------------
# Copyright (C) 2017-2020, the Loge development team
#
# This file is part of Loge
# Loge is distributed under the terms of GNU General Public License
# The full license can be found in 'license.txt'
# Loge development team can be found in 'development.txt'
#-----------------------------------------------------------------


import re
import copy
import os

import io
import base64
import urllib

try:
    import svgwrite
except ImportError:
    pass
try:
    pass
    import matplotlib.pyplot as plt
except ImportError:
    pass
    
#----------------------------------------------

r_shell = None
variables = vars()

script_ID = 'aassTESTassas'

def vars_formated():
    out = copy.copy(variables)
    for key in out:
        if type(out[key]) is float:
            out[key] = round(out[key], r_shell.float_display_precison)
    return out

#----------------------------------------------

def r_comment(object):
    r_shell.report_markdown += str(object) + '\n\n'
    
def r_seepywarning(warning):
    r_comment('>>*!!! SeePyWarning - %s !!!*'%warning)

def r_mathcomment(object):
    comment_string = str(object)
    comment_string_formated = codeformat(comment_string)
    r_comment(comment_string_formated)
            
def r_adj(text = 'text', link = 'link', comment = 'somecomment', mode = 1, code = ''):
    script_id = script_ID #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<logeweb edit
    script_id = 'script_id'+ str(script_id) #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<logeweb edit
    islist = re.search(r'(\w+)\s*=\s*(\w+)\s*[[](\d+)[]]\s*', code)
    setvalues = None
    index = None
    #---changing True False display on report
    if text == 'True':
        text = '☑'
    if text == 'False':
        text = '☐'
    #---
    if islist:
        variable = islist.group(2)
        index = int(islist.group(3))
        setvalues = ('%(' + str(variable) + ')s') % vars_formated()
        setvalues = setvalues.replace(' ', '') #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<logeweb edit
    if mode == 1:
        href='[{0}]({5};{1};{3};{4}) {2}'.format(text, link, comment, setvalues, index, script_id) #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<logeweb edit
    if mode == 2:
        href='{2} [{0}]({5};{1};{3};{4})'.format(text, link, comment, setvalues, index, script_id) #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<logeweb edit
        #href = href.replace(' ', '')
    r_shell.report_markdown += href +'\n\n'
    
def r_img(imagename):
    script_dir = os.path.basename(os.path.dirname(r_shell.Script.script_path))
    image_path = os.path.join(script_dir, imagename)
    image_path = os.path.join('/static', image_path)
    r_shell.report_markdown += '![Alt text](%s)\n\n' % image_path

def r_plt(pltObject):
    try:
        buf = io.BytesIO()
        pltObject.savefig(buf, dpi=(60), format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        r_shell.report_markdown += '![Matplotlib plot](data: image / png; base64, %s)'%uri +'\n\n'
        r_shell._id += 1
        #pltObject.close()
    except Exception as e :
        r_seepywarning('Matplotlib plt image save failure - %s' %str(e))

def r_tab(tabulateObject):
    r_comment('''```\n%s\n```''' % str(tabulateObject))
        
def r_pil(PilImageObject):
    try:
        buf = io.BytesIO()
        PilImageObject.save(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        r_shell.report_markdown += '![Pillow image](data: image / png; base64, %s)'%uri +'\n\n'
        r_shell._id += 1
    except Exception as e :
        r_seepywarning('Pillow image save failure - %s' %str(e))

def r_tex(string):
    plt.figure(frameon=False)
    plt.axes(frameon=0)
    if string[0] != '$' and string[-1] != '$':
        string = '$' + string + '$'
    plt.text(0.0, 0.0, string, fontsize=600)
    plt.xticks(())
    plt.yticks(())
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, bbox_inches='tight', dpi=(2), format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    r_shell.report_markdown += '![Tex figure](data: image / png; base64, %s)' % uri + '\n\n'
    plt.close()
    r_shell._id += 1

def r_codetex(string):
    r_tex(codeformat(string))

def r_svg(svgObject):
    if type(svgObject) in [str]:
        svgObject= svgObject.replace('<svg', '<svg xmlns = "http://www.w3.org/2000/svg"')
        svgObject = svgObject.replace('\n', '')
        r_shell.report_markdown += '![svg image](data:image/svg+xml; utf8, %s)'%svgObject + '\n\n'
        r_shell._id += 1
    elif type(svgObject) is svgwrite.drawing.Drawing:
        print(svgObject.tostring())
        r_shell.report_markdown += '![svg image](data:image/svg+xml; utf8, %s)'%svgObject.tostring() + '\n\n'
        r_shell._id += 1
    else:
        r_seepywarning('Unknown SVG format given')
#----------

def codeformat(string):
    #changing 3**3 to 3^2
    string = string.replace('**', '^')
    #changing math.sin(1) to sin(1)
    string = string.replace('math.', '')
    #changing 3 * u.mm to 3[mm] - usable when Unum SI units system used in script
    string = re.sub(    r'\s*\*\s*u.(\w+)',
                        r'[\1]',
                        string  )
    #changing (3*u.mm + 3*u.m).asUnit(u.mm) to 3*u.mm + 3*u.m - usable when Unum SI units system used in script
    string = re.sub(    r'\((.+)\).asUnit\((.+)\)',
                        r'\1',
                        string  )            
    return string