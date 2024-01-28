
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


# With Serverless Framework you provide the entry point to your application as the handler for AWS Lambda. The framework manages the interaction between the serverless function
# and the external HTTP requests, so you don't need to explicitly call app.wsgi_app().
def lambda_handler(event, context):
    # Your custom handling logic here IF needed
    return flask_app(event, context)