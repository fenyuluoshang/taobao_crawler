from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import sqlite3
import somedata
import time


## 针对手机淘宝的爬虫
def networktest():
    # 蓉蓉(chrome)的手机模拟器设置
    # 由于PhantomJS解析有点奇怪，这里就只能调用firefox或者chrome
    mobile_emulation = {"deviceName": "Nexus 5"}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    # 初始化数据库连接
    sq = sqlite3.connect('./db.sqlite')
    c = sq.cursor()

    driver = webdriver.Chrome(desired_capabilities=chrome_options.to_capabilities())
    #### 超时时间 ####
    driver.implicitly_wait(5)
    # 以正常方式进入首页
    driver.get("https://h5.m.taobao.com/")
    # 点击按钮跳转分类页
    driver.find_elements_by_xpath("//div[@aria-label='分类']")[0].click()
    selectpage_url = driver.current_url

    # 大分类的列表
    selector = driver.find_element_by_xpath("//div[@axisdirection=\'vertical\']").find_elements_by_tag_name('span')

    for i in range(3, len(selector)):
        stet = selector[i].text
        if stet == '为您推荐' or stet == '人群偏爱' or stet == '花呗分期' or stet == '淘宝租赁' or stet == '飞猪旅行':
            continue
        selector[i].click()
        # 等待加载具体分类后进行后续操作
        tittle = selector[i].text
        WebDriverWait(driver=driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-spm=\'' + somedata.data_spm[tittle] + '\']')))
        panel = driver.find_element_by_xpath('//div[@data-spm]')
        elelist = panel.find_elements_by_tag_name('span')
        try:
            for k in range(0, len(elelist)):
                locationtittle = elelist[k].text

                if locationtittle != '' and locationtittle != '' and locationtittle != '到底啦':
                    # 呼吸延时
                    time.sleep(5)
                    node = driver.find_element_by_xpath('//div[@data-spm]').find_elements_by_tag_name('span')[k]
                    node.click()
                    if driver.title != '商品分类':
                        print('-' + driver.title)
                        if driver.title == '搜索宝贝':
                            for item in driver.find_elements_by_xpath('//a/h3'):
                                curs = c.execute(
                                    'SELECT count(*) FROM data WHERE name = :name AND tag = :tag AND type = :type ',
                                    {'name': item.text, 'tag': locationtittle, 'type': tittle})
                                if curs.fetchone()[0] == 0:
                                    c.execute('INSERT INTO data(name ,tag ,type ) VALUES(:name , :tag , :type)',
                                              {'name': item.text, 'tag': locationtittle, 'type': tittle})
                                    print(item.text + '  ' + locationtittle + '  ' + tittle)
                        else:
                            ## 尝试滚动
                            for ls in range(0, 40):
                                slit = driver.find_elements_by_tag_name('a')
                                ActionChains(driver).move_to_element(slit[len(slit) - 1]).perform()
                                # time.sleep(0.1)
                            spanlist = driver.find_elements_by_xpath(
                                '//span[contains(@style,\'color: rgb(51, 51, 51)\')]')
                            # print(int(len(spanlist) / 4))
                            for item in spanlist:
                                if len(item.text) > 6:
                                    curs = c.execute(
                                        'SELECT count(*) FROM data WHERE name = :name AND tag = :tag AND type = :type ',
                                        {'name': item.text, 'tag': locationtittle, 'type': tittle})
                                    if curs.fetchone()[0] == 0:
                                        c.execute('INSERT INTO data(name ,tag ,type ) VALUES(:name , :tag , :type)',
                                                  {'name': item.text, 'tag': locationtittle, 'type': tittle})
                                        print(item.text + '  ' + locationtittle + '  ' + tittle)
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
        except Exception as e:
            # 捕捉到异常恢复状态，并为后续操作提供准备
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
    sq.close()
    driver.close()
