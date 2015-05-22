__author__ = 'rjr862'

import dbservices
from flask import Flask, jsonify, request, abort
import time

app = Flask(__name__)



@app.route('/<int:project>/tickets', methods=['GET'])
def get_all_tickets(project):
    map = dbservices.get_all_tickets(project)
    return jsonify(map)

@app.route('/<int:project>/tickets/<int:ticket>', methods=['GET'])
def get_ticket(project, ticket):
    map = dbservices.get_ticket(project, ticket)
    return jsonify(map)


@app.route('/<int:project>/tickets/', methods=['POST'])
def post_ticket(project, ticket):
    if not request.json:
        abort(400)
    if not dbservices.validate_ticket(project, request.json):
        abort(400)
    map = dbservices.post_ticket(project, request.json)
    return jsonify(map)



if __name__ == '__main__':
    app.run()
