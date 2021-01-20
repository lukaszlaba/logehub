import sys
import subprocess
import os
import time
import re

class Manager() :
    def __init__(self, dirpath):
        self.script_dir = dirpath
        #----
        self.script_list = self.get_script_list()
        self.script_name = self.get_script_name()
        self.script_description = self.get_script_description()
        self.script_category = self.get_script_category()
        #-----
        self.categories = list(set(self.script_category.values())) + ['Any category']


    def get_script_list(self):
        scriptlist = []
        for root, dirs, files in os.walk(self.script_dir, topdown=False):
            for name in files:
                if 'see.py' in name:
                    if not '.pyc' in name:
                        scriptlist.append(os.path.join(root, name))
        return scriptlist

    def get_script_name(self):
        description_dict = {}
        for i in self.script_list:
            script_path = i
            file = open(script_path, 'r')
            script = file.read()
            description = None
            description = re.search(r"SeeName :[ ]*(.+)", script)
            if description :
                description  = description.group(1)
            else :
                description  = 'Brak nazwy'
            description_dict[i] = description
        return  description_dict

    def get_script_description(self):
        description_dict = {}
        for i in self.script_list:
            script_path = i
            file = open(script_path, 'r')
            script = file.read()
            description = None
            description = re.search(r"'''.*SeeDescription\s*:(.*?)'''", script, flags=re.DOTALL)
            if description :
                description  = description.group(1)   
            else :
                description  = 'Brak opisu'
            description_dict[i] = description
        return  description_dict

    def get_script_category(self):
        category_dict = {}
        for i in self.script_list:
            script_path = i
            file = open(script_path, 'r')
            script = file.read()
            category = None
            category = re.search(r"SeeCategory :[ ]*(.+)", script)
            if category :
                category  = category.group(1)   
            else :
                category  = 'Not defined'
            category_dict[i] = category
        return  category_dict
        
    def get_script_list_for_category (self, category= None):
        if category:
            scriptlist = []
            for i in self.script_category.keys():
                if self.script_category[i] == category:
                    print(i)
                    scriptlist.append(i)
        if (category== None) or (category== 'Any category'):
             scriptlist = self.script_list.keys()
        return scriptlist
        
    def run_some_script(self, scriptname):
        if scriptname in self.script_list.keys():
            script_path = self.script_list[scriptname]
            subprocess.Popen(['python', '-m', 'seepy.SeePy', script_path, '-r']) #run as read only 
        else:
            print('!! ' + scriptname + ' not find in ' + self.script_dir + ' !!')

if __name__ == "__main__":
    None
    script_maneger = Manager("C:\\Users\\Lenovo\\Documents\\logeweb\\scripts\\scriptbank")
    print(script_maneger.script_list)
    print(script_maneger.script_name)
    print(script_maneger.script_description)
    print(script_maneger.script_category)
    print(script_maneger.categories)
    #script_maneger.run_some_script(manager.script_list[1])
    #script_maneger.run_some_script('dsdsd')
    #print(script_maneger.get_script_list_for_category('Any category'))