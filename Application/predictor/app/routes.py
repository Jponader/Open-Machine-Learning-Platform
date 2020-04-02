from app import app
from app.predictor import predictor
from flask import request, Response

@app.route('/predict', methods=['POST'])
def predict():

    response = None

    if request.json is None:
        # Expect application/json request
        response = Response("", status=415)
    else:
        message = dict()
        try:
            message = request.json
            print(message)
           
            task = predictor(message['id'])
            task.start()

            response = Response("", status=200)
        except Exception as ex:
            logging.exception('Error processing message: %s' % request.json)
            response = Response(ex.message, status=500)

    return response

@app.route('/')
@app.route('/index')
def index():
    return "Running"




