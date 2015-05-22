__author__ = 'rjr862'

from dbconfig import db
from time import gmtime, strftime

def get_date():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def convert_db_table_to_map(rows, column_metadata):
    map  = {}
    i = 0
    j = -1

    for row in rows:
        i+=1
        map['Ticket #' + str(i)] = {}
        for col in row:
            j+=1
            map['Ticket #' + str(i)][column_metadata[j][0]] = col
            print(col)
    return map

def get_all_tickets(project):
    cur = db.cursor()
    cmd = 'SELECT * FROM tickets WHERE tickets.p_id=%s'
    cur.execute(cmd, str(project))
    return convert_db_table_to_map(cur.fetchall(), cur.description)


def get_ticket(project, ticket):
    cur = db.cursor()
    cmd = 'SELECT * FROM tickets WHERE tickets.key=%s AND tickets.p_id=%s'
    cur.execute(cmd, (ticket, str(project)))

def validate_ticket(project, json):
    if json.get('ticket_name') and json.get('ticket_description'):
        return True
    else:
        return False


def post_ticket(project, json):
    cur = db.cursor()
    cmd = 'INSERT INTO tickets(p_id, ticket_name, ticket_description, date_created) ' \
          'VALUES (%s, %s, %s, %s)'
    cur.execute(cmd, (project, json.get('ticket_name'), json.get('ticket_description'), get_date()))
