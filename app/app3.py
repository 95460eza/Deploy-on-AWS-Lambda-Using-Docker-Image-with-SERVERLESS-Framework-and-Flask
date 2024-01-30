
import logging
from flask import Flask, jsonify
from werkzeug.wrappers import Request
#from werkzeug.wsgi import ClosingIterator



# Configure logging
logging.basicConfig(level=logging.INFO)


flask_app = Flask(__name__)


@flask_app.route('/', methods=['GET'])
def index():
    return jsonify(message='NATOU MPON AMOUR tu la? FINALEMENT Manifeste toi DONC HEIN!!')


# ONLY If you're running the App locally (not on AWS Lambda), you might want to start the Flask development server. OTHERWISE it is NOT suitable for a PRODUCTION environment like
# AWS Lambda!
# if __name__ == '__main__':
#     flask_app.run(host='0.0.0.0', port=8000, debug=False)
#     flask_app.run()



# AWS Lambda when used with the "SERVERLESS FRAMEWORK" EXPECTS to interfaces with WSGI (Web Server Gateway Interface) compatible applications. The Flask .wsgi_app() METHOD
# returns a WSGI application as the correct interface type.
def lambda_handler(event, context):

    # Create a WSGI-compatible environment from Lambda event
    env = {
        'wsgi.version': (1, 0),
        'wsgi.input': event['body'],
        'wsgi.url_scheme': 'https',
        'REQUEST_METHOD': event['httpMethod'],
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'HTTP_ACCEPT': event['headers'].get('Accept', ''),
        'HTTP_ACCEPT_ENCODING': event['headers'].get('Accept-Encoding', ''),
        'HTTP_USER_AGENT': event['headers'].get('User-Agent', ''),
        'PATH_INFO': event['path'],
        'QUERY_STRING': event['queryStringParameters'] or '',
        'CONTENT_TYPE': event['headers'].get('Content-Type', ''),
        'CONTENT_LENGTH': event['headers'].get('Content-Length', '0'),
        'SERVER_NAME': event['requestContext']['domainName'],
        'SERVER_PORT': '443',
        'SCRIPT_NAME': '',
        'wsgi.errors': None,  # You might want to set this to a log file or similar
        'wsgi.multiprocess': False,
        'wsgi.multithread': False,
        'wsgi.run_once': False
        # Add more headers as needed
    }

    logging.info(f"AWS Lambda-generated ENVENT SUCESSFULLY PARSED: %s", event)

    # Call the Flask app with the translated environment
    with flask_app.request_context(env):
        response = flask_app.dispatch_request()

    # Return the response
    return {
        'statusCode': response.status_code,
        'body': response.get_data(),
        'headers': dict(response.headers),
    }
