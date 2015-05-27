__author__ = 'rjr862'

from flask import Flask, jsonify, request, abort
from flask import render_template
from jinja2 import evalcontextfilter, Markup, escape
from app import dbservices, app, authservices
import re


@app.route('/projects/<int:project>/tickets', methods=['GET'])
def get_all_tickets(project):
    map = dbservices.get_all_tickets(project)
    return jsonify(map)


@app.route('/projects/<int:project>/tickets/<int:ticket>', methods=['GET'])
def get_ticket(project, ticket):
    map = dbservices.get_ticket(project, ticket)
    return jsonify(map)


@app.route('/projects/<int:project>/tickets/5', methods=['POST'])
def post_ticket(project):
    if not request.json:
        abort(400)
    if not dbservices.validate_ticket(project, request.json):
        abort(400)
    map = dbservices.post_ticket(project, request.json)
    return jsonify(map)

@app.route('/projects/', methods=['POST'])
@authservices.get_user_from_session
def post_project(username):
    print(username)
    if not request.json or not username:
        abort(400)
    map = dbservices.post_project(request.json, username)
    return 'hi'

@app.route('/')
@authservices.authenticate_with_sessionid
def home_page(username):
    if not username:
        return render_template('signin.html')
    else:
        project = dbservices.get_project_for_user(username)
        ticket_list = dbservices.get_all_tickets(project, type = 'list')
        return render_template('index2.html', tickets=ticket_list)


@app.route('/login', methods=['POST'])
@authservices.authenticate_with_form_fields
def user_login_form(username):
    if not username:
        return 'You didn\'t type in the fields right, you imbecile!'
    authservices.start_session(username)
    return 'You logged in, good work chap.'


@app.route('/auth/login', methods=['POST'])
@authservices.authenticate_with_auth_header
def user_login_auth(key):
    if not key:
        return 'You didn\'t type in the fields right, you imbecile!'
    return 'You logged in, good work chap.'


@app.route('/register', methods=['POST'])
@authservices.validate_new_user
def post_user(request_body):
    if not request_body:
        return 'You didn\'t type in the fields right, you imbecile!'
    # return render_template('dashboard.html')
    else:
        dbservices.post_user(request_body)
    return 'You registered, I\'m satisfied.'


_paragraph_re = re.compile(r'(?:\r\n|\r(?!\n)|\n){2,}')


@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n') \
                          for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


@app.template_filter()
@evalcontextfilter
def space2nbsp(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace(' ', '&nbsp') \
                          for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result
