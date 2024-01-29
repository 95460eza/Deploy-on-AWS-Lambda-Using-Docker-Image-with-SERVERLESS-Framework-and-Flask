
import logging
from flask import Flask, jsonify
#from werkzeug.wsgi import ClosingIterator


# Configure logging
logging.basicConfig(level=logging.INFO)



flask_app = Flask(__name__)

@flask_app.route('/', methods=['GET'])
def index():
    return jsonify(message='NATOU est tu la? Manifeste toi DONC!!')



# If you're running the App locally (not on AWS Lambda), you might want to start the Flask development server which is NOT suitable for a PRODUCTION environment like AWS Lambda
#if __name__ == '__main__':
    #flask_app.run(host='0.0.0.0', port=8000, debug=False)
    # flask_app.run()

# AWS Lambda when used with the "SERVERLESS FRAMEWORK" EXPECTS to interfaces with WSGI (Web Server Gateway Interface) compatible applications. The Flask .wsgi_app() METHOD
# returns a WSGI application as the correct interface type.

body = "PAPA0" 

def lambda_handler(event, context):
    return flask_app(event, context)