from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import json
import sqlite3
import somedata


def networktest():
    # 蓉蓉(chrome)的手机模拟器设置
    # 由于PhantomJS解析有点奇怪，这里就只能调用firefox或者chrome
    mobile_emulation = {"deviceName": "Nexus 5"}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    sq = sqlite3.connect('./db.sqlite')
    c = sq.cursor()

    driver = webdriver.Chrome(desired_capabilities=chrome_options.to_capabilities())
    # driver = webdriver.PhantomJS()
    driver.implicitly_wait(10)
    ## 以正常方式进入首页
    driver.get("https://h5.m.taobao.com/")
    # print(driver.page_source)
    driver.find_elements_by_xpath("//div[@aria-label='分类']")[0].click()
    # print(driver.title)
    selectpage_url = driver.current_url

    selector = driver.find_element_by_xpath("//div[@axisdirection=\'vertical\']").find_elements_by_tag_name('span')
    vk = {}
    vb = {}
    vdata = {}

    for i in range(0, len(selector)):
        stet = selector[i].text
        if stet == '为您推荐' or stet == '人群偏爱' or stet == '花呗分期' or stet == '淘宝租赁' or stet == '飞猪旅行':
            continue
        selector[i].click()
        # 等待0.5秒避免错误数据
        tittle = selector[i].text
        WebDriverWait(driver=driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-spm=\'' + somedata.data_spm[tittle] + '\']')))
        panel = driver.find_element_by_xpath('//div[@data-spm]')
        vb[tittle] = panel.get_attribute('data-spm')
        vk[tittle] = {}
        elelist = panel.find_elements_by_tag_name('span')
        data = []
        try:
            for k in range(0, len(elelist)):
                locationtittle = elelist[k].text
                if locationtittle != '' and locationtittle != '' and locationtittle != '到底啦':
                    vk[tittle][str(k)] = locationtittle
                    # th = threading.Thread(target=openPage, args=(i, k, locationtittle, somedata.data_spm[tittle]))
                    # th.start()
                    node = driver.find_element_by_xpath('//div[@data-spm]').find_elements_by_tag_name('span')[k]
                    print(node.text)
                    node.click()
                    if driver.title != '商品分类':
                        print('-' + driver.title)
                        if driver.title == '搜索宝贝':
                            for item in driver.find_elements_by_xpath('//a/h3'):
                                print(item.text)
                                curs = c.execute('SELECT count(*) FROM datas WHERE name = :name', {'name': item.text})
                                if curs.fetchone()[0] == 0:
                                    c.execute('INSERT INTO datas(name ,tag ,type ) VALUES(:name , :tag , :type)',
                                              {'name': item.text, 'tag': locationtittle, 'type': tittle})
                        else:
                            spanlist = driver.find_elements_by_xpath(
                                '//span[contains(@style,\'color: rgb(51, 51, 51)\')]')
                            # print(int(len(spanlist) / 4))
                            for item in spanlist:
                                if len(item.text) > 6:
                                    print(item.text)
                                    curs = c.execute('SELECT count(*) FROM datas WHERE name = :name',
                                                     {'name': item.text})
                                    if curs.fetchone()[0] == 0:
                                        c.execute('INSERT INTO datas(name ,tag ,type ) VALUES(:name , :tag , :type)',
                                                  {'name': item.text, 'tag': locationtittle, 'type': tittle})
                    driver.get(selectpage_url)
                    sq.commit()
                    driver.find_element_by_xpath("//div[@axisdirection=\'vertical\']").find_elements_by_tag_name(
                        'span')[
                        i].click()
                    # 等待
                    WebDriverWait(driver=driver, timeout=10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//div[@data-spm=\'' + somedata.data_spm[tittle] + '\']')))
                    elelist = driver.find_element_by_xpath('//div[@data-spm]').find_elements_by_tag_name('span')
            selector = driver.find_element_by_xpath("//div[@axisdirection=\'vertical\']").find_elements_by_tag_name(
                'span')
        except Exception:
            driver.get(selectpage_url)
            sq.commit()
            driver.find_element_by_xpath("//div[@axisdirection=\'vertical\']").find_elements_by_tag_name(
                'span')[
                i].click()
            # 等待
            WebDriverWait(driver=driver, timeout=10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@data-spm=\'' + somedata.data_spm[tittle] + '\']')))
            selector = driver.find_element_by_xpath("//div[@axisdirection=\'vertical\']").find_elements_by_tag_name(
                'span')
        print(data)

    driver.close()

    print(json.dumps(vk))
    print(json.dumps(vb))
