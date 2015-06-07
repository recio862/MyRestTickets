__author__ = 'rjr862'

from time import gmtime, strftime
from flask import session
from app.dbconfig import db
from app import authservices, urlservices

import os, base64


def get_date():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def get_all_tickets(username, project, type = 'map'):

    result = None
    try:
        cur = db.cursor()
        cmd = 'SELECT * FROM projects_to_users WHERE username=%s'
        cur.execute(cmd, username)
        projects_to_users_rows = cur.fetchall()
        project_matches_user = False
        for row in projects_to_users_rows:
            if row[0] == project:
                project_matches_user = True
        if not project_matches_user:
            return result
        cmd = 'SELECT * FROM tickets WHERE tickets.p_id=%s'
        cur.execute(cmd, str(project))
        rows = cur.fetchall()
        headers = cur.description

        result_dict = {}
        for i in rows:
            result_sub_dict = {}
            result_sub_dict['xhref'] = urlservices.get_ticket_url(i[1], i[0])
            result_sub_dict['ticket_id'] = str(i[0])
            result_sub_dict['project_id'] = str(i[1])
            result_sub_dict['ticket_name'] = str(i[2])
            result_sub_dict['ticket_description'] = str(i[3])
            result_sub_dict['date_created'] = str(i[4])
            result_dict[str(i[0])] = result_sub_dict
    except:
        raise
    finally:
        if cur:
            cur.close()
    return result_dict


def get_all_projects(username, type = 'map'):
    result = None
    try:
        cur = db.cursor()
        cmd = 'SELECT * FROM projects_to_users WHERE projects_to_users.username = %s'
        cur.execute(cmd, username)
        p_to_users = cur.fetchall()
        result_list = []
        for row in p_to_users:
            p_id = row[0]
            cmd = 'SELECT * FROM projects WHERE projects.p_id=%s'
            cur.execute(cmd, p_id)
            rows = cur.fetchall()
            result_list.append(rows[0])
            headers = cur.description
        result_dict = {}
        for i in result_list:
            result_sub_dict = {}
            result_sub_dict['xhref'] = urlservices.base_url + 'projects/' + str(i[0])
            result_sub_dict['p_id'] = str(i[0])
            result_sub_dict['project_name'] = str(i[1])
            result_sub_dict['project_category'] = str(i[2])
            result_sub_dict['project_description'] = str(i[3])
            result_sub_dict['date_created'] = str(i[4])
            result_sub_dict['created_by'] = str(i[5])
            result_dict[i[0]] = result_sub_dict
    except:
        raise
    finally:
        if cur:
            cur.close()
    return result_dict

def get_ticket(project, ticket):
    result = None
    try:
        cur = db.cursor()
        cmd = 'SELECT * FROM tickets WHERE tickets.t_id=%s AND tickets.p_id=%s'
        cur.execute(cmd, (ticket, str(project)))
        result = convert_db_table_to_map(cur.fetchall(), cur.description)
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
        val = cur.fetchone()
        if val:
            result = val[0]
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

def put_ticket(json, username, project, ticket):
    result = None
    try:
        cur = db.cursor()
        cmd = 'UPDATE tickets SET tickets.ticket_name = %s, tickets.ticket_description = %s WHERE tickets.p_id = %s AND tickets.t_id = %s'
        cur.execute(cmd, (json.get('ticket_name'), json.get('ticket_description'), str(project), str(ticket)))
        db.commit()
        result = { 'xhref' : (str(cur.lastrowid)) }
        print(result)
    except:
        db.rollback()
        raise
    finally:
        if cur:
            cur.close()
    return result

def put_project(json, username, project):
    result = None
    try:
        cur = db.cursor()
        cmd = 'UPDATE projects SET projects.project_name = %s, projects.project_description=%s, projects.project_category=%s WHERE projects.p_id = %s'
        cur.execute(cmd, (json.get('project_name'), json.get('project_description'), json.get('project_category'),  project))
        db.commit()
        result = { 'xhref' : (str(cur.lastrowid)) }
        print(result)
    except:
        db.rollback()
        raise
    finally:
        if cur:
            cur.close()
    return result

def post_ticket(project, json):
    result = None
    if not json.get('ticket_name') and not json.get('ticket_description'):
        return result
    try:
        cur = db.cursor()
        cmd = 'INSERT INTO tickets(p_id, tickets.ticket_name, tickets.ticket_description, tickets.date_created) VALUES (%s, %s, %s, %s)'
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

def get_project(project):
    result = None
    try:
        cur = db.cursor()
        cmd = 'SELECT * FROM projects WHERE p_id=%s'
        cur.execute(cmd, project)
        result = convert_db_table_to_map(cur.fetchall(), cur.description)
    except:
        raise
    finally:
        if cur:
            cur.close()
    return result

def get_project_and_its_tickets(project):
    result = None
    try:
        cur = db.cursor()
        cmd = 'SELECT * FROM tickets INNER JOIN projects ON tickets.p_id = projects.p_id WHERE tickets.p_id=%s'
        cur.execute(cmd, project)
        result = convert_db_table_to_map(cur.fetchall(), cur.description)
    except:
        raise
    finally:
        if cur:
            cur.close()
    return result

def delete_project(username, project):
    result = False
    try:
        cur = db.cursor()
        print(username)
        cmd = 'SELECT * FROM projects_to_users WHERE username = %s AND p_id = %s'
        cur.execute(cmd, (username, project))
        rows = cur.fetchall()
        for row in rows:
            cmd = 'DELETE FROM projects WHERE p_id=%s'
            cur.execute(cmd, row[0])
            cmd = 'DELETE FROM projects_to_users WHERE p_id=%s'
            cur.execute(cmd, row[0])
        db.commit()
        result = True
    except:
        db.rollback()
        raise
    finally:
        if cur:
            cur.close()
    return result

def delete_ticket(project, ticket):
    result = False
    try:
        cur = db.cursor()
        cmd = 'DELETE FROM tickets WHERE p_id=%s AND t_id=%s'
        cur.execute(cmd, (project, ticket))
        db.commit()
        result = True
    except:
        db.rollback()
        raise
    finally:
        if cur:
            cur.close()
    return result

def delete_tickets(username, project):
    result = False
    try:
        cur = db.cursor()
        cmd = 'DELETE FROM tickets WHERE p_id=%s'
        cur.execute(cmd, project)
        db.commit()
        result = True
    except:
        db.rollback()
        raise
    finally:
        if cur:
            cur.close()
    return result

def delete_projects(username):
    result = False
    try:
        cur = db.cursor()
        cmd = 'SELECT * FROM projects_to_users WHERE username = %s'
        cur.execute(cmd, username)
        rows = cur.fetchall()
        for row in rows:
            cmd = 'DELETE FROM projects WHERE p_id=%s'
            cur.execute(cmd, row[0])
            cmd = 'DELETE FROM projects_to_users WHERE p_id=%s'
            cur.execute(cmd, row[0])
            cmd = 'DELETE FROM tickets WHERE p_id=%s'
            cur.execute(cmd, row[0])
        db.commit()
        result = True
    except:
        db.rollback()
        raise
    finally:
        if cur:
            cur.close()
    return result

def convert_db_table_to_map_old(rows, column_metadata):
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

def convert_db_table_to_map(rows, column_metadata):
    map = {}
    i = 0
    j = 0

    for row in rows:
        j = 0
        for col in row:
            map[column_metadata[j][0]] = col
            j+=1
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


