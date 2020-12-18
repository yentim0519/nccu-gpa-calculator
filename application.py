import flask
from flask import request, jsonify,session
from flask_session import Session
import os
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select 
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
import time
from rq import Queue
from rq.job import Job
from rq.registry import StartedJobRegistry
from worker import conn
import json 


application = flask.Flask(__name__)
q = Queue(connection=conn)

# 一定要加這行，幫session簽名 
application.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



@application.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']
        # grad_or_not = flask.request.form['password']

        task = q.enqueue(generate_data_thread, args=(username,password))
        task_id = task.get_id()

        return flask.render_template('loading_page.html', task_id=task_id)

    return flask.render_template('index.html')




# get data
def generate_data_thread(username, password):

    target_url = 'https://i.nccu.edu.tw/Home.aspx'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--no-sandbox") # 這個放前面才不會crash (尚未證實
    chrome_options.add_argument("--headless") #無頭模式
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    
    try:
        driver.get(target_url)

        wait = ui.WebDriverWait(driver,100) # 100秒內，每500毫秒掃描一次
        wait.until(lambda driver: driver.find_element_by_id("captcha_Login1_UserName"))

        
        # # 這邊要try catch一下
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
        print(soup)

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
    except selenium.common.exceptions.WebDriverException:
        driver.close()
        return flask.render_template('error_page.html')

    return json.dumps(data) # 這邊要轉成json檔，result才能decode回來

    

    

@application.route('/thread_status/', methods=["POST"])
def thread_status():
    if request.method == 'POST':
        task_id = flask.request.form['task_id']
        print(task_id)
        task = Job.fetch(task_id, connection=conn)
        print(task.get_status())
        print(task.is_finished)
        registry = StartedJobRegistry('default', connection=conn)
        running_job_ids = registry.get_job_ids() 
        print(running_job_ids)

        if(task.get_status() == "failed"):
            return flask.render_template('error_page.html')
        
        if task.is_finished:
            return "true"
        else:
            return "false"
    
        
    



@application.route('/result', methods=["POST", "GET"]) 
def result():  
    
    task_id = flask.request.form['task_id']
    print("result", task_id)
    task = Job.fetch(task_id, connection=conn)
    # print(task.result)
    result_list = json.loads(task.result) 
    # print(result_list)

    return flask.render_template('page1.html', data_all = result_list)
    

            


if __name__ == '__main__':
    # application.debug=True
    application.run(host='0.0.0.0',threaded=True)


# Must:
# 密碼會加密（不會讓人看到
# handle result要按很多次才能跑出來
# 手機版的可以把不重要的資訊拿掉，讓table變小


# Nice to have:
# handle 一個學期全選
# handle 在generate時refresh
# handle 晚上學校系統維修的狀況
# 符合各平台版本 --> 在手機上要大一點
# 紀錄使用人次
# 給延畢生
# 中間弄個進度條，讓人知道等待時間
