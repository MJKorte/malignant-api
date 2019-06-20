FROM python:3

#set work directory
WORKDIR /usr/src/app

#install required packages
RUN pip install numpy
RUN pip install pandas
RUN pip install mysql.connector

#copy all files to work directory
COPY . .

#run VCFparser.py
CMD [ "python", "./VCFparser.py" ]
