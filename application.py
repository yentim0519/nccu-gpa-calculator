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
from flask_mysqldb import MySQL



application = flask.Flask(__name__)

application.config['MYSQL_HOST'] = 'us-cdbr-east-02.cleardb.com'
application.config['MYSQL_USER'] = 'b85e882ee53df8'
application.config['MYSQL_PASSWORD'] = '0cc7e169'
application.config['MYSQL_DB'] = 'heroku_1c0dd00304530b3'
application.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql = MySQL(application)



@application.route('/')
def index():
    return flask.render_template('index.html')


# try catch 還沒做好
@application.route('/generate_data', methods=["GET", "POST"])       
def generate_data():  
    username = flask.request.form['username']
    password = flask.request.form['password']
    # grad_or_not = flask.request.form['password']

    # mysql和application都傳不進去，connection可以
    global mysql
    connection = mysql.connection
    thread = Thread(target=generate_data_thread, args=(username, password, connection))
    thread.daemon = True
    thread.start()

    return flask.render_template('error_page.html')

# get data
def generate_data_thread(username, password, connection):
    
    cur = connection.cursor()
    target_url = 'https://i.nccu.edu.tw/Home.aspx'

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # chrome_options.add_argument("--no-sandbox") # 這個放前面才不會crash (尚未證實
    # chrome_options.add_argument("--headless") #無頭模式
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")

    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    # driver.get(target_url)

    cur.execute("INSERT INTO course_data (username, password) VALUES (%s,%s)", (username, password))
    connection.commit()
    
    cur.execute("INSERT INTO course_data (username, password) VALUES (%s,%s)", (username, password))
    connection.commit()

    cur.close()
    connection.close()
    driver.close()
    
    # wait = ui.WebDriverWait(driver,100) # 100秒內，每500毫秒掃描一次
    # wait.until(lambda driver: driver.find_element_by_id("captcha_Login1_UserName"))

    # # connection.commit()
    
    # # 這邊要try catch一下
    # driver.find_element_by_id("captcha_Login1_UserName").send_keys(username)
    # driver.find_element_by_id("captcha_Login1_Password").send_keys(password)
    # driver.find_element_by_id("captcha_Login1_ckbLogin").send_keys(Keys.ENTER)

    # # connection.commit()

    # wait.until(lambda driver: driver.find_element_by_id("WidgetContainer730150_Widget730150_HyperLink1"))
    # driver.find_element_by_id("WidgetContainer730150_Widget730150_HyperLink1").send_keys(Keys.ENTER)
    

    # # connection.commit()

    # driver.switch_to.window(driver.window_handles[-1])
    # time.sleep(3) # 改成wait until
    # driver.switch_to_alert().dismiss()
    # # print(driver.current_url)
    # wait.until(lambda driver: driver.find_elements_by_xpath("//li[@class='nav2']")[1])
    # driver.find_elements_by_xpath("//li[@class='nav2']")[1].click()

    # # connection.commit()

    # html = driver.page_source
    # soup = BeautifulSoup(html)

    # data = [] #要存進database
    # all_table = soup.find_all("table")
    # for table in all_table[5:]:
        
    #     table_data = []
    #     all_tr = table.find_all("tr")
    #     for tr in all_tr[2:]:
            
    #         tr_data = []
    #         all_td = tr.find_all("td")
    #         for td in all_td:
    #             tr_data.append(td.string)

    #         table_data.append(tr_data)
    #     data.append(table_data)
    # driver.close()


    # # 將資料存入database
    # # cur = connection.cursor()
    # cur.execute('''INSERT INTO course_data (username, password, data) VALUES ({username}, {password}, {data}) '''.format(username = username, password = password, data = data))
    # # cur.execute('''INSERT INTO course_data (username, password) VALUES ({username}, {password}) '''.format(username = username, password = password))
    # # cur.execute("INSERT INTO course_data (username, password) VALUES (%s, %s)", (username, password))
    # connection.commit()

    

    

# @application.route('/thread_status/')
# def thread_status():
#     global finished
#     # global thread
#     # if thread.is_alive == False: # 這裏無法確定有吃到
#     #     finished = "True"
    
#     return finished 



@application.route('/result', methods=["POST"]) 
def result():  
    # username 和 password從browser拿來
    cur = mysql.connection.cursor()
    cur.execute('''SELECT data FROM course_data WHERE username = '{username}' AND password LIKE '{password}' or middle_notes LIKE '%{brand_name}%' or base_notes LIKE '%{brand_name}%' '''.format(brand_name = brand_name))
    # 一定要用.format
    data = cur.fetchall()

    # finished = "False"
    return flask.render_template('page1.html', data_all = data)
    

            


if __name__ == '__main__':
    # application.debug=True
    application.run(host='0.0.0.0')


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
