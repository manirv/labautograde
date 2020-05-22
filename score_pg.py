import psycopg2
import os

db_url = os.environ.get('GCP_DATABASE_URL', 'postgres://mani:qZJGbnA92MHpXNBt@db.colaberry.cloud:5432/manidb')

conn = psycopg2.connect(database="postgres", user = "rf", password = "rf", host = "127.0.0.1", port = "5432")
#conn = psycopg2.connect(db_url)

#print("Opened database successfully")

cur = conn.cursor()


def create_lab_table():
    try:
        cur.execute("""CREATE TABLE rf.lab_sequence (
                        lab_seq_id SERIAL, 
                        lab_id text,
                        lab_name text)""")
    except Exception as e:
        print(e)

def drop_lab_table():
    try:
        cur.execute("""DROP TABLE rf.lab_sequence """)
    except Exception as e:
        print(e)

def create_score_table():
    try:
        cur.execute("""CREATE TABLE rf.score (
                        score_id SERIAL, 
                        lab_id text,
                        user_id text,
                        score text)""")
        cur.execute("""ALTER TABLE rf.score ADD COLUMN created_at TIMESTAMP;""")
        cur.execute("""ALTER TABLE rf.score ALTER COLUMN created_at SET DEFAULT now();""")
    except Exception as e:
        print(e)

def drop_score_table():
    try:
        cur.execute("""DROP TABLE rf.score """)
    except Exception as e:
        print(e)


def add_lab(lab_name):

    param = (lab_name,)
    cur.execute("INSERT INTO rf.lab_sequence (lab_name) VALUES (%s)", param )
    cur.execute('SELECT LASTVAL()')
    lastid = cur.fetchone()[0]
    id = lastid
    param = ('Lab{}'.format(id),lab_name)
    cur.execute("Update rf.lab_sequence set lab_id = %s where lab_name=%s", param )
    cur.execute("commit;")
    param = (lab_name,)
    cur.execute("SELECT lab_id FROM rf.lab_sequence where lab_name=%s", param )
    query_test = cur.fetchall()
    return query_test[0][0]

def delete_lab(lab_id):

    param = (lab_id,)
    cur.execute("DELETE from rf.lab_sequence where lab_name=%s", param )
    cur.execute("SELECT * FROM rf.lab_sequence")
    query_test = cur.fetchall()
    print(query_test)
    cur.execute("commit;")

def add_score(user_id,lab_id, score):

    param = (user_id,lab_id,score)
    cur.execute("INSERT INTO rf.score (user_id,lab_id,score) VALUES (%s,%s,%s)", param )
    cur.execute("commit;")
    param = (user_id,lab_id)
    cur.execute("SELECT score_id FROM rf.score where user_id=%s and lab_id=%s", param )
    query_test = cur.fetchall()
    return query_test[0][0]

def delete_score(user_id,lab_id):

    param = (user_id,lab_id)
    cur.execute("DELETE from rf.score where user_id=%s and lab_id=%s", param )
    cur.execute("SELECT * FROM rf.score  where user_id=%s and lab_id=%s", param )
    query_test = cur.fetchall()
    print(query_test)
    cur.execute("commit;")

def get_lab_id(lab_name):

    param = (lab_name,)
    cur.execute("SELECT lab_id FROM rf.lab_sequence where lab_name=%s", param)
    query_lab = cur.fetchall()
    if (len(query_lab) == 0):
        return add_lab(lab_name)
    else:
        return query_lab[0][0]

def get_lab_name(lab_id):

    param = (lab_id,)
    cur.execute("SELECT lab_name FROM rf.lab_sequence where lab_id=%s", param)
    query_lab = cur.fetchall()
    if (len(query_lab) == 0):
        return None
    else:
        return query_lab[0][0]

def get_score(score_id):

    param = (score_id,)
    cur.execute("SELECT * FROM rf.score where score_id=%s", param)
    query_lab = cur.fetchall()
    if (len(query_lab) == 0):
        return None
    else:
        return '{} - {} - {} - {}'.format(query_lab[0][0],query_lab[0][1],query_lab[0][2],query_lab[0][3])

def get_score_by_id(user_id,lab_id):

    param = (user_id,lab_id)
    cur.execute("SELECT * FROM rf.score where user_id=%s and lab_id=%s", param )
    query_lab = cur.fetchall()
    if (len(query_lab) == 0):
        return None
    else:
        if (len(query_lab) > 1):
            return query_lab
        else:

            return '{} - {} - {} - {}'.format(query_lab[0][0],query_lab[0][1],query_lab[0][2],query_lab[0][3])


#create_lab_table()
#create_score_table()
#add_score('user1','Lab1','{"result":"PASS","score": 5}')
#print(get_score(8))

#print(get_score_by_id('manirv','Lab1'))


#print(get_lab_name('Lab3'))
#add_lab('Lab1')
#delete_lab('Lab1')
#drop_lab_table()
