import shelve
import os
import score_db as sdb

filename = 'lab.shelve'
if os.path.exists(filename + '.db'):
    os.unlink(filename + '.db')
db = shelve.open(filename)


def create_lab(lab_id,lab_solution):

        db['data:README'] = b"""
    ==============
    package README
    ==============
    
    This is the README for ``lab``.
    """
        db['labs.__init__'] = b"""
print('labs imported')
message = 'This message is in package.__init__'
    """
        db['labs.' + lab_id] = lab_solution

        for key in sorted(db.keys()):
            print('  ', key)


def create_lab_answer(lab_id, lab_answer):
    db['data:README'] = b"""
    ==============
    package README
    ==============

    This is the README for ``lab answer``.
    """
    db['answer.__init__'] = b"""
print('lab answer imported')
message = 'This message is in answer.__init__'
    """
    db['answer.' + lab_id] = lab_answer

    for key in sorted(db.keys()):
        print('  ', key)


import json


def get_code_cell(input_content_file):
    parsed_json = ''
    with open(input_content_file) as json_data:
        parsed_json = json.load(json_data)

    code_content = ''
    cells = parsed_json['cells']

    for cell in cells:
        cell_type = cell['cell_type']

        if 'metadata' not in cell:
            # raise ValueError("No metadata found")
            print("No metadata found")

        if cell_type == 'code':
            if cell['metadata'].get('tags') != None and cell['metadata'].get('tags')[0] == 'solution':
                code_cell = cell['source']
                for code_line in code_cell:
                    code_content = code_content + '\n' + code_line

    return code_content

#dir_name = '/home/mani/workspace/flat_labs/'
#input_file = 'Lab-dealing-with-strings-and-dates.ipynb'
#input_file = 'Lab-data-structures-in-python.ipynb'

#code_cont = get_code_cell(dir_name + input_file)
#print(code_cont)
#lab_name = 'Lab-dealing-with-strings-and-dates'
#lab_name = 'Lab-data-structures-in-python'
#lab_id = sdb.get_lab_id(lab_name)
#create_lab(lab_id, code_cont)
