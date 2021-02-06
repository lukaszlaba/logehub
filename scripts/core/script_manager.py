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
        self.script_ID = self.get_script_ID()
        self.script_name = self.get_script_name()
        self.script_description = self.get_script_description()
        self.script_category = self.get_script_category()
        self.script_field = self.get_script_field()
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

    def get_script_ID(self):
        ID_dict = {}
        ID_if_not_exist = 6767
        for i in self.script_list:
            script_path = i
            file = open(script_path, 'r')
            script = file.read()
            ID = None
            ID = re.search(r"SeeID :[ ]*(.+)", script)
            if ID :
                ID = int(ID.group(1))
            else :
                ID = ID_if_not_exist
                ID_if_not_exist += 123
            ID_dict[i] = ID
        return ID_dict

    def get_script_name(self):
        name_dict = {}
        for i in self.script_list:
            script_path = i
            file = open(script_path, 'r')
            script = file.read()
            name = None
            name = re.search(r"SeeName :[ ]*(.+)", script)
            if name :
                name = name.group(1)
            else :
                name = 'Brak nazwy'
            name_dict[i] = name
        return name_dict

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
        return description_dict

    def get_script_category(self):
        category_dict = {}
        for i in self.script_list:
            script_path = i
            file = open(script_path, 'r')
            script = file.read()
            category = None
            category = re.search(r"SeeCategory :[ ]*(.+)", script)
            if category :
                category = category.group(1)
            else :
                category = 'Not defined'
            category_dict[i] = category
        return category_dict

    def get_script_field(self):
        field_dict = {}
        for i in self.script_list:
            script_path = i
            file = open(script_path, 'r')
            script = file.read()
            field = None
            field = re.search(r"SeeField :[ ]*(.+)", script)
            if field :
                field = field.group(1)
            else :
                field = 'Not defined'
            field_dict[i] = field
        return field_dict

    def get_script_list_for_field(self, field):
        scriptlist = []
        for path in self.script_list:
            if field in self.script_field[path]:
                scriptlist.append(path)
        return scriptlist

    def give_me_path_for_ID(self, ID):
        return dict(zip(self.script_ID.values(), self.script_ID.keys()))[ID]


if __name__ == "__main__":
    None
    script_maneger = Manager("C:\\Users\\Lenovo\\Dropbox\\DJANGO\\logeweb\\scripts\\scriptbank")
    print(script_maneger.script_list)
    print(script_maneger.script_ID)
    print(script_maneger.script_name)
    print(script_maneger.script_description)
    print(script_maneger.script_category)
    print(script_maneger.script_field)
    print(script_maneger.categories)
    script_maneger.run_some_script(manager.script_list[1])
    script_maneger.run_some_script('dsdsd')
    print(script_maneger.get_script_list_for_field('Structure'))