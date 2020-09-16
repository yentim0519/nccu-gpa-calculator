import flask
import os
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select 
from selenium.webdriver.common.keys import Keys
import time
from score_to_gpa import score_to_gpa

application = flask.Flask(__name__)

@application.route('/')
def index():
    return flask.render_template('index.html')


# try catch 還沒做好
@application.route('/result', methods=["POST"])
def result():
    username = flask.request.form['username']
    password = flask.request.form['password']

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

    # 將資料存成array並且計算GPA
    data = []
    total_score = 0
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
            
            total_credit += int(float(tr_data[5])) 
            total_score += float(tr_data[6]) * int(float(tr_data[5])) 
            
            table_data.append(tr_data)
        
        data.append(table_data)

    # 計算gpa
    gpa = total_score/total_credit
    
    return flask.render_template('page1.html', data_all = data, gpa = gpa)


if __name__ == '__main__':
    application.run(host='0.0.0.0')


# 1. 要有登入錯誤的介面
# 2.  