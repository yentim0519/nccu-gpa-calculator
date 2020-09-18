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
import concurrent.futures

# from generate_data_thread import generate_data_thread


application = flask.Flask(__name__)
finished = "False"

@application.route('/')
def index():
    return flask.render_template('index.html')


# try catch 還沒做好
@application.route('/generate_data', methods=["GET", "POST"])       
def generate_data():  
    username = flask.request.form['username']
    password = flask.request.form['password']

    global thread
    global finished # 在外面定義，這裏代表這個def在用global的finish
    finished = "False"
    with concurrent.futures.ThreadPoolExecutor() as executor:
        global future
        future = executor.submit(generate_data_thread, username, password)
    # thread = Thread(target=generate_data_thread, args=(username, password))
    # thread.daemon = True
    # thread.start()

    return flask.render_template('loading_page.html')

# get data
def generate_data_thread(username, password):
   
            
    target_url = 'https://i.nccu.edu.tw/Home.aspx'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--no-sandbox") # 這個放前面才不會crash (尚未證實
    chrome_options.add_argument("--headless") #無頭模式
    chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.get(target_url)
    
    wait = ui.WebDriverWait(driver,100) # 100秒內，每500毫秒掃描一次
    wait.until(lambda driver: driver.find_element_by_id("captcha_Login1_UserName"))
    
    # 這邊要try catch一下
    driver.find_element_by_id("captcha_Login1_UserName").send_keys(username)
    driver.find_element_by_id("captcha_Login1_Password").send_keys(password)
    driver.find_element_by_id("captcha_Login1_ckbLogin").send_keys(Keys.ENTER)

    wait.until(lambda driver: driver.find_element_by_id("WidgetContainer730150_Widget730150_HyperLink1"))
    driver.find_element_by_id("WidgetContainer730150_Widget730150_HyperLink1").send_keys(Keys.ENTER)
    
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(3) # 改成wait until
    driver.switch_to_alert().dismiss()
    # print(driver.current_url)
    wait.until(lambda driver: driver.find_elements_by_xpath("//li[@class='nav2']")[1])
    driver.find_elements_by_xpath("//li[@class='nav2']")[1].click()

    html = driver.page_source
    soup = BeautifulSoup(html)

    # 將資料存成array並且計算GPA
    global data 
    data = []
    total_score_4point3 = 0
    total_score_4 = 0
    total_credit = 0

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

    

@application.route('/status')
def thread_status():
    global finished
    global future
    if future.done():
        finished == "True"
    """ Return the status of the worker thread """
    return finished 

@application.route('/result', methods=["GET"])
def result():  
    global future
    global data
    data = future.result()
    return flask.render_template('page1.html', data_all = data)

            


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
