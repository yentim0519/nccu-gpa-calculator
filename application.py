import flask
from flask import request, jsonify
import os
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select 
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
import time
from threading import Thread
from generate_data_thread import generate_data_thread


application = flask.Flask(__name__)

@application.route('/')
def index():
    return flask.render_template('index.html')


# try catch 還沒做好
@application.route('/generate_data', methods=["GET", "POST"])
def generate_data():  
    username = flask.request.form['username']
    password = flask.request.form['password']

    thread = Thread(target=generate_data_thread, args=(username, password))
    thread.daemon = True
    thread.start()

    return jsonify({'thread_name': str(thread.name),
                    'started': True})

            


if __name__ == '__main__':
    application.run(host='0.0.0.0')


# handle登入錯誤, handle chrome 找不到item, handle sleep
# handle 重新按一次/result的
# handle beautiful soup那行有時會有問題
# handle selenium.common.exceptions.WebDriverException: Message: unknown error: Chrome failed to start: crashed.
# handle還沒修過的
# handle 晚上學校系統維修的狀況
# 符合各平台版本
# 紀錄使用人次
#
