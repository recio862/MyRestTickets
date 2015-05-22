__author__ = 'rjr862'

from dbconfig import db
from time import gmtime, strftime

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

def validate_ticket(json):
    if json.get('ticket_name'):
        return True
    else:
        return False


def post_ticket(json):
    pass
