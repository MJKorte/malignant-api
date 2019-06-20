FROM python:3

#this is to connect to flask with curl on port 5000
EXPOSE 5000

#set workdir
WORKDIR /flask_api

#install required packages
RUN pip install Flask
RUN pip install mysql-connector

#copy files inside flask_api to work directory
COPY . /flask_api

#run flask_api.py
CMD ["python", "flask_api.py"]
