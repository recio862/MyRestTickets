__author__ = 'rjr862'
from functools import wraps
from flask import request, jsonify
from app.dbconfig import db

def authenticate(fn):
    @wraps(fn)
    def auth_user(*args, **kwargs):
        auth = request.authorization
        if (auth):
            user = auth.username
            pwd = auth.password
            verified = verify_login(user,pwd)
            return fn(verified)
        else:
            return fn(False)
    return auth_user


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

    return False #login error



def validate_password(password, confirmation):
    if password != confirmation:
        return False

    if len(password) <= 6:
        return False

    if not int in password and not str in password:
        return False

    return True

def validate_username(username):
    if (len(username) <= 6):
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

    return False #error checking db or user exists

#To-do: email validation
def validate_email(email):
    return True

def validate_new_user(fn):
    @wraps(fn)
    def validate(*args, **kwargs):
        if request.json:
            if request.get('username') and request.get('password') and request.get('confirmation') and request.get('email)'):
                username = request.get('username')
                password = request.get('password')
                confirmation = request.get('confirmation')
                email = request.get('email')
                if validate_username(username) and validate_password(password,  confirmation) and validate_email(email):
                    return fn(request.json)

        return fn(None)
    return validate