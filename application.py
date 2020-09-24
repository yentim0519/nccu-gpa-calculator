import flask
from flask import request, jsonify,session
import os
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select 
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
import time
import threading
from flask_mysqldb import MySQL
from flask_session import Session
from rq import Queue
from rq.job import Job
from worker import conn
import json 


application = flask.Flask(__name__)
q = Queue(connection=conn)

# application.config['MYSQL_HOST'] = 'us-cdbr-east-02.cleardb.com'
# application.config['MYSQL_USER'] = 'b85e882ee53df8'
# application.config['MYSQL_PASSWORD'] = '0cc7e169'
# application.config['MYSQL_DB'] = 'heroku_1c0dd00304530b3'
# application.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# print(1)
# 要先設定global session variables
# session["finished"] = "false"
# session["data"] = 0


# print(2)
# SESSION_TYPE = 'filesystem'
# Session(application)

# Set the secret key to some random bytes. Keep this really secret!
# 一定要加這行，幫session簽名 
application.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# mysql = MySQL(application)

# 測試用pymysql
# import pymysql
# conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='35278479', db= 'us_states', charset='utf8')



@application.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']
        # grad_or_not = flask.request.form['password']

        task = q.enqueue(generate_data_thread, args=(username,password))
        task_id = task.get_id()

        # mysql和application都傳不進去，connection可以
        # global mysql
        # connection = mysql.connection 
        # session["finished"] = "false"
        # thread = threading.Thread(target=generate_data_thread, args=(username, password))
        # thread.daemon = True # 這會讓執行緒跟主程式一起結束
        # thread.start()
        # print("when start active_threading",threading.active_count())

        return flask.render_template('loading_page.html', task_id=task_id)

    return flask.render_template('index.html')




# get data
def generate_data_thread(username, password):
    # print(f'thread {threading.current_thread().name} is running...')
    
    
    # cur = connection.cursor()
    # print('cur', threading.current_thread().name)
    target_url = 'https://i.nccu.edu.tw/Home.aspx'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--no-sandbox") # 這個放前面才不會crash (尚未證實
    chrome_options.add_argument("--headless") #無頭模式
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.get(target_url)

    # try:
    #     cur.execute("INSERT INTO course_data (username, password) VALUES (%s,%s)", (username, password))
    # except Exception:
    #     global mysql # mysql傳不進去，但又會有斷線的問題
    #     connection = mysql.connection
    #     cur = connection.cursor()
    #     cur.execute("INSERT INTO course_data (username, password) VALUES (%s,%s)", (username, password))


    # print('cur_execute', threading.current_thread().name)
    # connection.commit()
    # print('commit', threading.current_thread().name)
    # print("active_threading:",threading.active_count(),threading.current_thread().name)
    
    # cur.execute("INSERT INTO course_data (username, password) VALUES (%s,%s)", (username, password))
    # connection.commit()

    # cur.close()
    # connection.close()
    # driver.close()
    # print("driver close:",threading.active_count(),threading.current_thread().name)
    
    wait = ui.WebDriverWait(driver,100) # 100秒內，每500毫秒掃描一次
    wait.until(lambda driver: driver.find_element_by_id("captcha_Login1_UserName"))

    # # connection.commit()
    
    # # 這邊要try catch一下
    driver.find_element_by_id("captcha_Login1_UserName").send_keys(username)
    driver.find_element_by_id("captcha_Login1_Password").send_keys(password)
    driver.find_element_by_id("captcha_Login1_ckbLogin").send_keys(Keys.ENTER)

    # # connection.commit()

    wait.until(lambda driver: driver.find_element_by_id("WidgetContainer730150_Widget730150_HyperLink1"))
    driver.find_element_by_id("WidgetContainer730150_Widget730150_HyperLink1").send_keys(Keys.ENTER)
    

    # # connection.commit()

    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(3) # 改成wait until
    driver.switch_to_alert().dismiss()
    # print(driver.current_url)
    wait.until(lambda driver: driver.find_elements_by_xpath("//li[@class='nav2']")[1])
    driver.find_elements_by_xpath("//li[@class='nav2']")[1].click()

    # # connection.commit()

    html = driver.page_source
    soup = BeautifulSoup(html)

    data = [] #要存進database
    all_table = soup.find_all("table")
    for table in all_table[5:]:
        
        table_data = []
        all_tr = table.find_all("tr")
        for tr in all_tr[2:]:
            
            tr_data = []
            all_td = tr.find_all("td")
            for td in all_td:
                tr_data.append(td.string)

            table_data.append(tr_data)
        data.append(table_data)
    driver.close()

    return "[1, 2, 3]"
    # return "hello"


    # # 將資料存入database
    # # cur = connection.cursor()
    # cur.execute('''INSERT INTO course_data (username, password, data) VALUES ({username}, {password}, {data}) '''.format(username = username, password = password, data = data))
    # # cur.execute('''INSERT INTO course_data (username, password) VALUES ({username}, {password}) '''.format(username = username, password = password))
    # # cur.execute("INSERT INTO course_data (username, password) VALUES (%s, %s)", (username, password))
    # connection.commit()

    

    

@application.route('/thread_status/', methods=["POST"])
def thread_status():
    task_id = flask.request.form['task_id']
    print(task_id)
    # global thread
    # if thread.is_alive == False: # 這裏無法確定有吃到
    #     finished = "True"
    task = Job.fetch(task_id, connection=conn)
    print(task.get_status())
    print(task.is_finished)

    
    if task.is_finished:
        return "true"
    else:
        return "false"
        
    



@application.route('/result', methods=["POST", "GET"]) 
def result():  
    # username 和 password從browser拿來
    # cur = mysql.connection.cursor()
    # cur.execute('''SELECT data FROM course_data WHERE username = '{username}' AND password LIKE '{password}' or middle_notes LIKE '%{brand_name}%' or base_notes LIKE '%{brand_name}%' '''.format(brand_name = brand_name))
    # # 一定要用.format
    # data = cur.fetchall()

    # finished = "False"
    
    task_id = flask.request.form['task_id']
    print("result", task_id)
    task = Job.fetch(task_id, connection=conn)
    print(task.result)
    result_list = json.loads(task.result) 
    print(result_list)

    return flask.render_template('page1.html', data_all = result_list)
    

            


if __name__ == '__main__':
    # application.debug=True
    application.run(host='0.0.0.0',threaded=True)


# Must:
# data這個變數每個人都可以access
# handle還沒修過的
# 密碼會加密（不會讓人看到
# handle result要按很多次才能跑出來
# 手機版的可以把不重要的資訊拿掉，讓table變小



# handle計算gpa進位
# handle 一個學期全選
# handle 在generate時refresh
# handle 有時result跑出來會什麼都沒有，要refresh url才有東西
# handle 晚上學校系統維修的狀況
# 符合各平台版本 --> 在手機上要大一點
# 紀錄使用人次
# 給延畢生
