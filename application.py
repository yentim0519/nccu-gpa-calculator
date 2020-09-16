import flask
import os
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select 
from selenium.webdriver.common.keys import Keys
import time
from rq import Queue
from worker import conn
from get_course_data import get_course_data

application = flask.Flask(__name__)
# # engine = sqlalchemy.create_engine("mysql+pymysql://yentim0519:helloyen@database-1.crc98fdcbodi.us-east-2.rds.amazonaws.com/innodb")
# # db = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker(bind=engine))  # 這行出問題
# # Config MySQL

@application.route('/')
def index():
    return flask.render_template('index.html')
    
@application.route('/result', methods=["POST"])
def result():
    username = flask.request.form['username']
    password = flask.request.form['password']
    q = Queue(connection=conn)
    
    job = q.enqueue(get_course_data, username, password)
    
    return flask.render_template('page1.html', tables = ["processing"])


@application.route('/result1', methods=["POST"])
def result1():
    if job.status == True:
        return flask.render_template('page1.html', tables = [job.result])



if __name__ == '__main__':
    application.run(host='0.0.0.0')
