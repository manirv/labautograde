import collections
import re
import importlib
import sys
import score_pg as spg
import lab_pg as lpg
import sys_db_importer
import inspect
import random
from radon.visitors import ComplexityVisitor
from radon.raw import analyze
import radon.metrics as rm
from sklearn.model_selection import KFold


fields_master = {}
fields_master['KFold'] = ['n_splits']
fields_master['OLS'] = ['n_splits']
fields_master['KFold'] = ['n_splits']


def auto_grade(user_id,lab_name, lab_answer_from_user):
    try:
        #print(spg.get_lab_id(lab_name))
        temp_name = user_id + '_' + str(spg.get_lab_id(lab_name)) + '_' + 'sub' + str(random.randint(100,999))
        lpg.create_lab_answer(temp_name, lab_answer_from_user)
        filename = '/home/mani/workspace/rfvalidator/refactored/tmp.shelve'
        sys.path_hooks.append(sys_db_importer.DBFinder)
        sys.path.insert(0, filename)
        lab_id = spg.get_lab_id(lab_name)
        lab_key = importlib.import_module('labs.' + lab_id)
        lab_answer = importlib.import_module('labanswer.' + temp_name)
        result = check_lab(lab_answer,lab_key)
        check_code_complexity(lab_answer, lab_key)
        score_id = spg.add_score(user_id, lab_id, str(result))
        return result

    except:
        result = {'result': 'FAIL', 'score': 0, 'message': ['Error while grading lab. Please contact admin.']}
        print("Unexpected error:", sys.exc_info()[0])
        raise
        return result

    finally:
        del lab_answer
        #del lab_key
        #print(lab_answer.answer)


def save_lab_key(lab_name, lab_key):
    try:
        #print(spg.get_lab_id(lab_name))
        temp_name = str(spg.get_lab_id(lab_name))
        lpg.create_labs(temp_name, lab_key)
        result = {'result': 'SUCCESS'}

    except:
        result = {'result': 'ERROR'}
        print("Unexpected error:", sys.exc_info()[0])
        raise
    return result


def check_lab(lab_answer,lab_key):
    result_status = 'PASS'
    result_score = 1
    result_message = []
    # ut_output = unittest.test_variable('answer', lab_key.answer)
    ut_output = False
    try:
        ut_output = False
        score,tot_answers = check_answer(lab_answer,lab_key)
        if score >= 1 and score == tot_answers:
            ut_output = True

    except AttributeError as error:
        print('AttributeError')
        ut_output = False

    if ut_output:
        result_score = 3
        result_status =  'PASS'
        result_message.append('Good Job')
    else:
        result_score = 0
        result_status = 'FAIL'
        result_message.append('Please retry your solution')

    source = inspect.getsourcelines(lab_answer)
    sourcelines = ' '.join(list(source[0]))
    #if check_literal_answer(sourcelines, lab_key.get_answer_1()):
    if False:
        result_score = 0
        result_status = 'FAIL'
        result_message = ['Wrong answer. You must not explicitly type your answer']
    else:
        step_check,step_message = validate_steps(lab_answer, lab_key)
        if step_check:
            result_score = result_score + 2
        else:
            result_status = 'FAIL'
            result_message = step_message

    result = {'result': result_status, 'score': result_score, 'message': result_message}
    return result


def check_answer(lab_answer, lab_key):
    score = 0
    tot_answers = 0
    for i in range (1,6):
        for k, v in inspect.getmembers(lab_key):
            if k == 'get_answer_'+ str(i):
                tot_answers = i
                break
    for i in range(1,tot_answers+1):
        print('Looking for get_answer_' + str(i))
        key_ans = getattr(lab_key, 'get_answer_' + str(i))()
        try:
            sub_ans = getattr(lab_answer, 'get_answer_' + str(i))()
        except AttributeError as error:
            print('sub_ans:: AttributeError')
            sub_ans = None
        print('key_ans',key_ans)
        print('sub_ans',sub_ans)
        result = key_ans == sub_ans
        #result = lab_answer.answer == lab_key.answer
        if result:
            score = score + 1
    return score,tot_answers


def check_literal_answer(source, answer_key):
    import re
    source = 'answer = ' + source
    source = re.sub('\s+',' ',source)
    result = re.search(str(answer_key),source)
    return result


def check_steps(lab_key):
    tot_steps = 0
    for i in range (1,6):
        for k, v in inspect.getmembers(lab_key):
            if k == 'step'+ str(i):
                tot_steps = i
                break

    return tot_steps


def validate_steps(lab_answer, lab_key):
    result = True
    a = lab_key.steps
    messages = []

    l = 0
    if a['steps'] is not None:
        l = len(a['steps'])

    for i in range(1,l + 1):
        code = a['steps'][i]['code']
        message = a['steps'][i]['message']
        val = getattr(lab_key, code)
        ret = match_answer_steps(lab_answer, val)
        if ret is not True:
            messages.append(message)
            result = ret
            continue
    return (result, messages)


def match_answer_steps(lab_answer, val):
    result = False

    for k, v in inspect.getmembers(lab_answer):
        if v == val:
            result = True

    return result


def check_answer_steps(lab_answer, lab_key, step_no):
    result = False
    tmp_step_obj = None
    message = None
    for k, v in inspect.getmembers(lab_key):
        if k == 'step'+ str(step_no):
            tmp_step_obj = v
            #print('%s :' % k, v)
        if k == 'message'+ str(step_no):
            message = v

    for k, v in inspect.getmembers(lab_answer):
        if v == tmp_step_obj:
            #print('Matched - %s :' % k, v)
            result = True

    return (result, message)


def check_code_complexity(lab_answer, lab_key):

    result = {}
    source = inspect.getsource(lab_answer)
    h = rm.h_visit(source)
    hm = rm.h_visit_ast(h)
    v = analyze(source)
    return result

def compare_objects(a,b):

    fields = fields_master[type(a).__name__]
    fields_left = []
    fields_right = []
    for k, v in inspect.getmembers(a):
        if k in fields:
            fields_left.append(v)
            print(k,v)
    for k, v in inspect.getmembers(b):
        if k in fields:
            fields_right.append(v)
            print(k,v)
    result = fields_left == fields_right
    print(result)




