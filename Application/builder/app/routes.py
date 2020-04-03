from app import app
from app.builder import builder
from flask import request, Response
import json
import logging

@app.route('/build', methods=['POST'])
def build():

    response = None

    if request.json is None:
        # Expect application/json request
        response = Response("", status=415)
    else:
        message = dict()
        try:
            message = request.json
            print(message)
           
            task = builder(int(message['id']))
            task.start()

            response = Response("", status=200)
        except Exception as ex:
            logging.exception('Error processing message: %s' % request.json)
            response = Response(ex.message, status=500)

    return response

@app.route('/')
@app.route('/index')
def index():
    return "Runnings"




