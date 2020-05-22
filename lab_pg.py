import score_pg as spg
import psycopg2
import os

db_url = os.environ.get('GCP_DATABASE_URL', 'postgres://mani:qZJGbnA92MHpXNBt@db.colaberry.cloud:5432/manidb')
conn = psycopg2.connect(database="postgres", user = "rf", password = "rf", host = "127.0.0.1", port = "5432")
#conn = psycopg2.connect(db_url)

#print("Opened database successfully")

cur = conn.cursor()



def create_lab_source_table():
    try:
        cur.execute("""CREATE TABLE rf.lab_source (
                        lab_source_seq_id SERIAL, 
                        key text,
                        value text)""")
        cur.execute("""ALTER TABLE rf.lab_source ADD COLUMN created_at TIMESTAMP;""")
        cur.execute("""ALTER TABLE rf.lab_source ALTER COLUMN created_at SET DEFAULT now();""")
    except Exception as e:
        print(e)

def drop_lab_table():
    try:
        cur.execute("""DROP TABLE rf.lab_source """)
    except Exception as e:
        print(e)


def create(lab_name,lab_source):

    param = (lab_name,lab_source)
    cur.execute("INSERT INTO rf.lab_source (key,value) VALUES (%s,%s)", param )
    cur.execute('SELECT LASTVAL()')
    lastid = cur.fetchone()[0]
    #print(lastid)
    cur.execute("commit;")
    return lastid

def create_or_replace(lab_name,lab_source):
    param = (lab_name,lab_source)
    lab_name_from_db = get_key(lab_name)
    if lab_name_from_db == None:
        id = cur.execute("INSERT INTO rf.lab_source (key,value) VALUES (%s,%s)", param )
        cur.execute('SELECT LASTVAL()')
        lastid = cur.fetchone()[0]
        #print(lastid)
        cur.execute("commit;")
        return lastid
    else:
        param2 = (lab_source, lab_name_from_db)
        cur.execute("Update rf.lab_source set value = %s where key=%s", param2)
        cur.execute("commit;")
        cur.execute('SELECT LASTVAL()')
        lastid = cur.fetchone()[0]
        #print(lastid)
        return lastid


def delete(lab_id):

    param = (lab_id,)
    cur.execute("DELETE from rf.lab_sequence where lab_name=%s", param )
    cur.execute("SELECT * FROM rf.lab_sequence")
    query_test = cur.fetchall()
    print(query_test)
    cur.execute("commit;")


def get_source(key):

    param = (key,)
    cur.execute("SELECT value FROM rf.lab_source where key=%s", param)
    query_source = cur.fetchall()
    if (len(query_source) == 0):
        return None
    else:
        return query_source[0][0]

def get_key(key):

    param = (key,)
    cur.execute("SELECT key FROM rf.lab_source where key=%s", param)
    query_source = cur.fetchall()
    if (len(query_source) == 0):
        return None
    else:
        return query_source[0][0]


#def create_lab(lab_id, lab_solution):

#    db['data:README'] = b"""
#    ==============
#    package README
#    ==============
#
#    This is the README for ``package``.
#    """
#    db['labs.__init__'] = b"""
#message = 'This message is in package.__init__'
#    """
#    db['labs.' + lab_id] = lab_solution

#    for key in sorted(db.keys()):
#        print('  ', key)
#    db.close()


def create_labs(lab_id, lab_solution):
    try:
        create_or_replace('labs.' + lab_id, lab_solution)

    except Exception as e:
        print('Exception while creating labs :', e)


def create_lab_answer(lab_id, lab_solution):
    try:
        create_or_replace('labanswer.' + lab_id, lab_solution)

    except Exception as e:
        print('Exception while adding lab answers :', e)


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

#create_lab_source_table()

##One time activity
key = 'labs.__init__'
value = """
message = 'This message is in labs.__init__'
            """
#create(key, value)
#print('Created Key ', key)

key2 = 'labanswer.__init__'
value2 = """
message = 'This message is in labanswer.__init__'
            """
#create(key2, value2)
#print('Created Key ', key2)

dir_name = '/home/mani/workspace/flat_labs/'
input_file = 'Lab-dealing-with-strings-and-dates.ipynb'
#input_file = 'Lab-data-structures-in-python.ipynb'

#code_cont = get_code_cell(dir_name + input_file)
#print(code_cont)
lab_name = 'Lab-dealing-with-strings-and-dates'
#lab_name = 'LabTest'

#lab_name = 'Lab-data-structures-in-python'
#lab_id = spg.get_lab_id(lab_name)
#print(lab_id)
#create_labs(lab_id, code_cont)
#print('Created Lab ', lab_id)
#print(get_key('Lab1'))
#print(get_source('Lab1'))



#print(get_lab_name('Lab3'))
#add_lab('Lab1')
#delete_lab('Lab1')
#drop_lab_table()

#print ("Operation done successfully")
#conn.close()
