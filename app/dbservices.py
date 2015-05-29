__author__ = 'rjr862'

from time import gmtime, strftime
from flask import session
from app.dbconfig import db
from app import authservices

import os, base64


def get_date():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def get_all_tickets(project, type = 'map'):
    print(project)
    result = None
    try:
        cur = db.cursor()
        cmd = 'SELECT * FROM tickets WHERE tickets.p_id=%s'
        cur.execute(cmd, str(project))
        rows = cur.fetchall()
        headers = cur.description

        if type == 'map':
            result = convert_db_table_to_map(rows, headers)
        elif type == 'list':
            result = convert_db_table_to_list(rows, headers)
    except:
        raise
    finally:
        if cur:
            cur.close()
    return result

def get_ticket(project, ticket):
    result = None
    try:
        cur = db.cursor()
        cmd = 'SELECT * FROM tickets WHERE tickets.key=%s AND tickets.p_id=%s'
        cur.execute(cmd, (ticket, str(project)))
        result = cur.fetchone()[0]
    except:
        raise
    finally:
        if cur:
            cur.close()
    return result

def get_project_for_user(username):
    result = None
    try:
        cur = db.cursor()
        cmd = 'SELECT * FROM projects_to_users WHERE projects_to_users.username=%s'
        cur.execute(cmd, username)
        result = cur.fetchone()[0]
    except:
        raise
    finally:
        if cur:
            cur.close()
    return result



def post_user(request_body):
    try:
        cur = db.cursor()
        cmd = 'INSERT INTO users(username, password, email, sessionid, sessionstate) VALUES (%s, %s, %s, %s, %s)'
        #print(session['restticketssid'])
        # if not sessionid['restticketssid']
        # error handling - disabled cookies
        sessionid = authservices.start_session()
        cur.execute(cmd,(request_body.get('username'), request_body.get('password'), request_body.get('email'), sessionid, '1'))
        #this is now done in post_project
        #cmd = 'INSERT INTO projects_to_users(p_id, username) VALUES (%s, %s)'
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        if cur:
            cur.close()


def post_ticket(project, json):
    result = None
    try:
        cur = db.cursor()
        cmd = 'INSERT INTO tickets(p_id, ticket_name, ticket_description, date_created) ' \
            'VALUES (%s, %s, %s, %s)'
        cur.execute(cmd, (project, json.get('ticket_name'), json.get('ticket_description'), get_date()))
        db.commit()
        result = { 'xhref' : (str(cur.lastrowid)) }
    except:
        db.rollback()
        raise
    finally:
        if cur:
            cur.close()
    return result


def post_project(json, username):
    result = None
    try:
        cur = db.cursor()
        cmd = 'INSERT INTO projects(project_name, project_category, project_description, date_created, created_by) ' \
          'VALUES (%s, %s, %s, %s, %s)'
        cur.execute(cmd, (json.get('project_name'), json.get('project_category'), json.get('project_description'), get_date(), username))
        cmd = 'INSERT INTO projects_to_users(p_id, username) VALUES (%s, %s)'
        result = { 'xhref' : (str(cur.lastrowid)) } #project id
        cur.execute(cmd, (cur.lastrowid, username))
        db.commit()
        cur.close()
    except:
        db.rollback()
        raise
    finally:
        if cur:
            cur.close()
    return result



def convert_db_table_to_map(rows, column_metadata):
    map = {}
    i = 0
    j = -1

    for row in rows:
        i += 1
        map['Ticket #' + str(i)] = {}
        for col in row:
            j += 1
            map['Ticket #' + str(i)][j] = col
    return map

def convert_db_table_to_list(rows, column_metadata):
    list = []
    i = -1
    j = -1

    for row in rows:
        i += 1
        j = -1
        list.append({})
        list[i] = {}
        for col in row:
            j += 1
            list[i][j] = col
    return list

def validate_ticket(project, json):
    if json.get('ticket_name') and json.get('ticket_description'):
        return True
    else:
        return False


