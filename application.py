import flask
import os
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select 
from selenium.webdriver.common.keys import Keys
import time
 
application = flask.Flask(__name__)
# engine = sqlalchemy.create_engine("mysql+pymysql://yentim0519:helloyen@database-1.crc98fdcbodi.us-east-2.rds.amazonaws.com/innodb")
# db = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker(bind=engine))  # 這行出問題
# Config MySQL


@application.route('/')
def index():
    return flask.render_template('index.html')
    
@application.route('/result', methods=["POST"])
def result():
    username = flask.request.form['username']
    password = flask.request.form['password']
    return username

    # target_url = 'https://i.nccu.edu.tw/Home.aspx'
    # driver = webdriver.Chrome('/Users/owner/Desktop/Github/Self_practice/Selenium_動態爬蟲/chromedriver')
    # driver.get(target_url)
    # # print(driver.current_url)
    

    # driver.find_element_by_id("captcha_Login1_UserName").send_keys(username)
    # driver.find_element_by_id("captcha_Login1_Password").send_keys(password)
    # driver.find_element_by_id("captcha_Login1_ckbLogin").send_keys(Keys.ENTER)
    # time.sleep(4) #讓javasciprt的東西跑出來，才能進入全人系統 # 這邊應該改得更彈性
    # driver.find_element_by_id("WidgetContainer730150_Widget730150_HyperLink1").send_keys(Keys.ENTER)
    # driver.switch_to.window(driver.window_handles[-1])
    # # print(driver.current_url) # 不知道為什麼一定要print才行
    # time.sleep(3)
    # driver.switch_to_alert().dismiss()
    # # print(driver.current_url)
    # time.sleep(2)
    # driver.find_elements_by_xpath("//li[@class='nav2']")[1].click()

    # # html = driver.page_source
    # # soup = BeautifulSoup(html)
    # data = []
    # all_table = soup.find_all("table")
    # for table in all_table[5:]:
    #     all_tr = table.find_all("tr")
    #     for tr in all_tr[2:]:
    #         all_td = tr.find_all("td")
    #         for td in all_td:
    #             print(td.string)
        
    return flask.render_template('page1.html', tables = username)

@application.route('/result1', methods=["POST"])
def result1():
    top_notes = flask.request.form['top_notes']
    middle_notes = flask.request.form['middle_notes']
    base_notes = flask.request.form['base_notes']

    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM perfume_data WHERE top_notes LIKE '%{top_notes}%' and middle_notes LIKE '%{middle_notes}%' and base_notes LIKE '%{base_notes}%' '''.format(top_notes = top_notes, middle_notes = middle_notes, base_notes = base_notes))
    brand_datas = cur.fetchall()
    return flask.render_template('page2.html', brand_datas = brand_datas)



if __name__ == '__main__':
    application.run(host='0.0.0.0')
