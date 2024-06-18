# Use the official Python base image
FROM python:3.8

# Set the working directory
WORKDIR /loadtest-api-server

# Copy the current directory contents into the container at /loadtest-api-server
COPY ./loadtest-api-server/app.py ./loadtest-api-server/app.py
#COPY ./loadtest-api-server/app.py ./loadtest-api-server/app.py
COPY ./requirements.txt ./requirements.txt

RUN chmod +x /usr/local/bin/python

# Install dependencies
# RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt --progress-bar off

# Expose the port Flask is running on
EXPOSE 5000

# Define the command to run your application
CMD ["python", "/loadtest-api-server/loadtest-api-server/app.py"]