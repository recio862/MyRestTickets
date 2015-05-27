__author__ = 'rjr862'

from flask import Flask, jsonify, request, abort
from flask import render_template
from jinja2 import evalcontextfilter, Markup, escape
from app import dbservices, app, loginservices
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


@app.route('/')
@loginservices.authenticate_with_sessionid
def home_page(project, key):
    if not key:
        return render_template('signin.html')
    if key:
        posts = dbservices.get_all_tickets(project)
        return render_template('index2.html')


@app.route('/login', methods=['POST'])
@loginservices.authenticate_with_form_fields
def user_login_form(key):
    if not key:
        return 'You didn\'t type in the fields right, you imbecile!'
    return 'You logged in, good work chap.'


@app.route('/auth/login', methods=['POST'])
@loginservices.authenticate_with_auth_header
def user_login_auth(key):
    if not key:
        return 'You didn\'t type in the fields right, you imbecile!'
    return 'You logged in, good work chap.'


@app.route('/register', methods=['POST'])
@loginservices.validate_new_user
def post_user(request_body):
    if not request_body:
        return 'You didn\'t type in the fields right, you imbecile!'
    # return render_template('dashboard.html')
    else:
        loginservices.post_user(request_body)
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
