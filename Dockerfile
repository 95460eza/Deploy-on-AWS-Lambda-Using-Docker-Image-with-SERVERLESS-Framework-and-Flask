# Choosing one of the AWS ECR public image repository "base image" FOR AWS LAMBDA FUNCTIONS. Here the Python 3.12 one!
FROM public.ecr.aws/lambda/python:3.12

# First copy ONLY the requirements.txt  to leverage Docker cache
# Copy RELATIVE to the Dockerfile location FROM .... INTO a folder WHOSE NAME IS STORED IN the variable LAMBDA_TASK_ROOT
# This COPIES the FILE from the app FOLDER INTO a LOCATION that will be assigned at DEPLOYMENT by AWS (i.e. it is the above AWS-emanaged ENVIRONMENTAL VARIABLE)
# "COPY /app /app" refers to an ABSOLUTE path at the root of the host machine WHILE "COPY app/ app/" refers to a path RELATIVE to the build context (i.e. where the Dockerfile is)
# IF THE Dockerfile is AT THE ROOT OF YOUR PROJECT, THEY ARE THE SAME. SO USE THE RELATIVE APPROACH
COPY app/requirements.txt   ${LAMBDA_TASK_ROOT}

# pip3 is used when you run python3, but using pip will MOST of the time AUTOMATICALLY point to pip for you if needed
# install INSIDE THE CONTAINER the dependencies found in requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --upgrade flask


# Copy ALL content FROM (Relative to Dockerfile location).... INTO the work directory /app INSIDE the Docker Image (Destination)
# COPY /app ${LAMBDA_TASK_ROOT} copies the contents of the /app directory (including its subdirectories and files) into the "ROOT" of the Docker image
# Otherwis BELOW CODE would copy the contents of the app directory (including its folder structure) into the "SPECIFIED" destination directory ${LAMBDA_TASK_ROOT} within the Docker image
# After that Docker knows in which file everything is located (kind of indexing)
COPY app/   ${LAMBDA_TASK_ROOT}


# Using "EXPOSE" won't create an error when deploying with Zappa, but it won't have any impact on the deployment EITHER!!
# The EXPOSE instruction in a Dockerfile is used to inform Docker that the APP INSIDE the container listens on the specified ports at runtime (FROM THE APP Definition code),
# But Docker doesn't publish this ports! To ALLOW EXTERNAL access to the application running inside the container, you need to MAP THAT port to a port of your LOCAL HOST (ex: 5000)
# using for Ex: ********* docker run -p 8000:5000 my-container ******************
#EXPOSE 8000

# You don't need the CMD ["app.lambda_handler"] in your Dockerfile when deploying a Flask application with "SERVERLESS FRAMEWORK".
# The Serverless Framework is designed to handle the execution of serverless functions and doesn't rely on Docker's CMD for specifying the command to run.
# Specify rather SERVERLESS FRAMEWORK configurations in the "serverless.yml" file!!!!!!!!!!!!!!
#CMD [ "app.lambda_handler" ]
CMD [ "lambda_handler" ]
