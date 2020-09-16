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
    # q = Queue(connection=conn)
    
    # job = q.enqueue(get_course_data, username, password)

    target_url = 'https://i.nccu.edu.tw/Home.aspx'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless") #無頭模式
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.get(target_url)
    
    driver.find_element_by_id("captcha_Login1_UserName").send_keys(username)
    driver.find_element_by_id("captcha_Login1_Password").send_keys(password)
    driver.find_element_by_id("captcha_Login1_ckbLogin").send_keys(Keys.ENTER)
    time.sleep(4) #讓javasciprt的東西跑出來，才能進入全人系統 # 這邊應該改得更彈性
    driver.find_element_by_id("WidgetContainer730150_Widget730150_HyperLink1").send_keys(Keys.ENTER)
    driver.switch_to.window(driver.window_handles[-1])
    # print(driver.current_url) # 不知道為什麼一定要print才行
    time.sleep(3)
    driver.switch_to_alert().dismiss()
    # print(driver.current_url)
    time.sleep(2)
    driver.find_elements_by_xpath("//li[@class='nav2']")[1].click()

    html = driver.page_source
    soup = BeautifulSoup(html)
    
    return flask.render_template('page1.html', tables = [soup])


@application.route('/result1', methods=["GET"])
def result1():
    if job.status == True:
        return flask.render_template('page1.html', tables = [job.result])
    else:
        return flask.render_template('page1.html', tables = ["Not Yet!"])



if __name__ == '__main__':
    application.run(host='0.0.0.0')
