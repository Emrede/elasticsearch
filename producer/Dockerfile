# set base image (host OS)
FROM python:3.9

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local directories to the working directory
COPY src/ .
COPY data/ .

# command to run on container start
CMD [ "python", "-u", "./producer.py" ]
