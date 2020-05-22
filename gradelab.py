import json
import auto_grade as ag

def grade_lab(user_id, lab_name):
    input_content_file = lab_name + '.ipynb'
    parsed_json = ''
    with open(input_content_file) as json_data:
        parsed_json = json.load(json_data)

    code_content = ''
    cells = parsed_json['cells']
    for cell in cells:
        cell_type = cell['cell_type']

        if 'metadata' not in cell:
            # raise ValueError("No metadata found")
            code_cell = cell['source']
            for code_line in code_cell:
                code_content = code_content + '\n' + code_line

        if cell_type == 'code':
            if cell['metadata'].get('tags') == None or cell['metadata'].get('tags')[0] != 'grade':
                code_cell = cell['source']
                for code_line in code_cell:
                    code_content = code_content + '\n' + code_line
    result = send_lab_for_grading(user_id, lab_name,code_content)
    return result


def send_lab_for_grading(user_id, lab_name,lab_content):
    return ag.auto_grade(user_id, lab_name,lab_content)
