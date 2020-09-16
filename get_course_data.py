def get_course_data(username, password):
    target_url = 'https://i.nccu.edu.tw/Home.aspx'

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # chrome_options.add_argument("--headless") #無頭模式
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")

    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    # driver.get(target_url)
    
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

    # html = driver.page_source
    # soup = BeautifulSoup(html)

    # data = []
    # all_table = soup.find_all("table")
    # for table in all_table[5:]:
    #     table_data = []
    #     all_tr = table.find_all("tr")
    #     for tr in all_tr[2:]:
    #         tr_data = []
    #         all_td = tr.find_all("td")
    #         for td in all_td:
    #             tr_data.append(td)
    #         table_data.append(tr_data)
    #     data.append(table_data)

    return target_url