__author__ = 'rjr862'

from flask import Flask

app = Flask(__name__)
app.secret_key = 'r5n1l5b1m2j2' #i give you my secret key, use it wisely
from app import resttickets