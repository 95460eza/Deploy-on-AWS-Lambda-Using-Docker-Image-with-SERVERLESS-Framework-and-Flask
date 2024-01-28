
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

    try:
        # wsgi_env = event.get('wsgi_environ', {})
        # wsgi_env = event['wsgi_environ']
        wsgi_env = {
            # 'wsgi.version': event['wsgi.version'],
            'wsgi.version': (1, 0),  # Use a default version
            'wsgi.url_scheme': event['headers']['CloudFront-Forwarded-Proto'],
            'REQUEST_METHOD': event['httpMethod']
            # Add more relevant headers as needed
        }

        # Log information
        logging.info("The Lambda function-generated EVENT HAS BEEN SUCCESSFULLY PARSED : %s", event)

        # Call the Flask app with the translated environment
        #flask_response = flask_app.wsgi_app(wsgi_env, lambda response, start_response: "None")
        flask_response = flask_app.wsgi_app(wsgi_env, lambda response, start_response: None)
        # flask_response = ClosingIterator(flask_app.wsgi_app(wsgi_env, lambda response, start_response: None))

        # Log success
        logging.info("The Flask OBJECT HAS SUCCESSFULLY PROCESSED the event generated by the Lambda function.")
        logging.info(f"RESPONSE of Flask App OBJECT : {flask_response}")

        # In Flask the response object is typically an iterable and should be iterated over instead of trying to access it like a list
        if flask_response is not None:

            if hasattr(flask_response, '__iter__'):
                # Assuming flask_response is already of the type ClosingIterator object
                logging.info(f"The RESPONSE of the Flask App object is of the TYPE : {type(flask_response)}")
                #  The b prefix before a string indicates to treat it as a bytes literal rather than a string literal. Bytes literals are sequences of bytes, each representing
                #  a character in ASCII (or more generally in the Unicode character set).
                logging.info(f"The CONTENT of the Flask App Response is: {b''.join(flask_response)}")

                # response_in_bytes_format = b''.join(flask_response)
                # body = response_in_bytes_format.decode('utf-8')
                body = "PAPA1"

            else:
                logging.info(f"Flask response is Not Iterable")
                body = body = "PAPA2"
                # body = [b''.join(flask_response)]

        else:
            logging.info(f"Flask response is None")
            body = "PAPA3"
            # body = [b'Error: Flask response is None']

        # Now you can use the 'body' variable as needed
        return body
        # return {
        #     'statusCode': 200,
        #     'body': body
        # }

    except Exception as e:

        # Log the exception
        logging.info("Lambda Event: %s", event)
        logging.error("An error HAS occurred: %s", event)
        logging.error("An error HAS occurred: %s", str(e))

        # Handle exceptions and return an error response if needed
        return {
            'statusCode': 850,
            'body': f'Error: {str(e)}'
        }
