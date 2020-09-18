def generate_data_thread(username, password):
    try:
        if request.method == 'POST':
            
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

            將資料存成array並且計算GPA
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
                    
                    if tr_data[6] == "棄修":
                        continue
                    elif tr_data[6] == "通過":
                        continue
                    else:
                        total_credit += int(float(tr_data[5])) 
                        total_score_4point3 += score_to_gpa_4point3(float(tr_data[6])) * int(float(tr_data[5])) 
                        total_score_4 += score_to_gpa_4(float(tr_data[6])) * int(float(tr_data[5])) 

                    table_data.append(tr_data)
                
                data.append(table_data)

            driver.close()
        # return flask.render_template('page1.html')
            return flask.render_template('page1.html', data_all = data)
            global finished
            time.sleep(5)
            finished = True
        else:
            return flask.render_template('index.html')

    except Exception:
        driver.close()
        return flask.render_template('error_page.html')