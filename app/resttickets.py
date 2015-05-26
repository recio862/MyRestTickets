__author__ = 'rjr862'

from flask import Flask, jsonify, request, abort
from flask import render_template
from app import dbservices, app, loginservices


@app.route('/<int:project>/tickets', methods=['GET'])
def get_all_tickets(project):
    map = dbservices.get_all_tickets(project)
    return jsonify(map)

@app.route('/<int:project>/tickets/<int:ticket>', methods=['GET'])
def get_ticket(project, ticket):
    map = dbservices.get_ticket(project, ticket)
    return jsonify(map)


@app.route('/<int:project>/tickets/5', methods=['POST'])
def post_ticket(project):
    if not request.json:
        abort(400)
    if not dbservices.validate_ticket(project, request.json):
        abort(400)
    map = dbservices.post_ticket(project, request.json)
    return jsonify(map)

@app.route('/')
def home_page():
    return render_template('signin.html')

@app.route('/login')
@loginservices.authenticate
def user_login(key):
    if not key:
        return 'You failed to log in, I\'m dissapointed.'
    #return render_template('dashboard.html')
    return 'You logged in, I\'m impressed!'


@app.route('/register')
@loginservices.validate_new_user
def post_user(request_body):
    if not request_body:
        return 'You didn\'t type in the fields right, you imbecile!'
    #return render_template('dashboard.html')
    else:
        dbservices.post_user(request_body)
    return 'You registered, I\'m satisfied.'


