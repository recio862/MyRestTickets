__author__ = 'rjr862'
from functools import wraps
from flask import request, jsonify, session
from app.dbconfig import db
import base64, os


def authenticate_with_auth_header(fn):
    @wraps(fn)
    def auth_user(*args, **kwargs):
        auth = request.authorization
        if (auth):
            user = auth.username
            pwd = auth.password
            verified = verify_login(user, pwd)
            return fn(verified)
        else:
            return fn(False)

    return auth_user


def authenticate_with_form_fields(fn):
    @wraps(fn)
    def auth_user(*args, **kwargs):
        user = request.form.get('username', None)
        pwd = request.form.get('password', None)
        verified = verify_login(user, pwd)
        return fn(verified)

    return auth_user


def authenticate_with_sessionid(fn):
    @wraps(fn)
    def auth_user(*args, **kwargs):
        verified = False
        print(session.get('restticketssid'))
        if 'restticketssid' in session:
            sessionid = session.get('restticketssid')
            verified = verify_session(str(sessionid)[2:len(str(sessionid)) - 1])
        return fn(verified)

    return auth_user


def verify_session(sessionid):
    try:
        cur = db.cursor()
        cmd = 'SELECT * FROM users WHERE users.sessionid=%s AND users.sessionstate=%s'
        cur.execute(cmd, (str(sessionid), 1))
        rows = cur.fetchall()
        if rows:
            return True
    except:
        raise
    finally:
        if cur:
            cur.close()

    return False  # login error


def verify_login(username, password):
    try:
        cur = db.cursor()
        cmd = 'SELECT * FROM users WHERE users.username=%s AND users.password=%s'
        cur.execute(cmd, (str(username), str(password)))
        db.commit()
        rows = cur.fetchall()
        if rows:
            return True
    except:
        raise
    finally:
        if cur:
            cur.close()

    return False  # login error


def validate_password(password, confirmation):
    if not password or not confirmation:
        return False

    if password != confirmation:
        return False

    if len(password) <= 6:
        return False

    return True


def validate_username(username):
    if not username or len(username) < 6:
        return False
    try:
        cur = db.cursor()
        cmd = 'SELECT * FROM users WHERE users.username=%s'
        cur.execute(cmd, str(username))
        db.commit()
        rows = cur.fetchall()
        if not rows:
            return True
    except:
        raise
    finally:
        if cur:
            cur.close()

    return False  # error checking db or user exists


# To-do: email validation
def validate_email(email):
    return True


def validate_new_user(fn):
    @wraps(fn)
    def validate(*args, **kwargs):
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirm-password')
        email = request.form.get('email')
        if validate_username(username) and validate_password(password, confirmation) and validate_email(email):
            result = {'username': username,
                      'password': password,
                      'confirmation': confirmation,
                      'email': email}
            return fn(result)

        return fn(None)

    return validate


def post_user(request_body):
    cur = db.cursor()
    cmd = 'INSERT INTO users(username, password, email, sessionid, sessionstate) VALUES (%s, %s, %s, %s, %s)'
    sessionid = generate_session()
    session['restticketssid'] = sessionid
    print(sessionid)
    print(session.get('restticketssid'))

    # if not sessionid['restticketssid']
    # error handling - disabled cookies
    cur.execute(cmd,
                (request_body.get('username'), request_body.get('password'), request_body.get('email'), sessionid, '1'))

    cmd = 'INSERT INTO projects_to_users(p_id, username) VALUES (%s, %s)'
    db.commit()
    cur.close()


def generate_session():
    return base64.b64encode(os.urandom(16))
