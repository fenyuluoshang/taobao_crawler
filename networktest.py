from selenium import webdriver
import json

# 蓉蓉(chrome)的手机模拟器设置
# 由于PhantomJS解析有点奇怪，这里就只能调用firefox或者chrome

mobile_emulation = {"deviceName": "Nexus 5"}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
driver = webdriver.Chrome(desired_capabilities=chrome_options.to_capabilities())
driver.implicitly_wait(1000)
## 以正常方式进入首页
driver.get("https://h5.m.taobao.com/")

driver.find_elements_by_xpath("//div[@aria-label='分类']")[0].click()
selectpage_url = driver.current_url
selector = driver.find_element_by_xpath("//div[@axisdirection=\'vertical\']").find_elements_by_tag_name('span')

vk = {}
for i in range(0, len(selector)):
    selector[i].click()
    print('-' + selector[i].text)
    tittle = selector[i].text
    panel = driver.find_element_by_xpath('//div[@data-spm]')
    panel.find_elements_by_tag_name('span')
    vk[tittle] = {}
    try:
        elelist = panel.find_elements_by_tag_name('span')
        for k in range(0, len(elelist)):
            locationtittle = elelist[k].text
            print('--' + locationtittle)
            if locationtittle != ''and locationtittle != '' and locationtittle != '到底啦':
                vk[tittle][str(k)] = locationtittle
    except Exception:
        vk[tittle] = {}
        elelist = panel.find_elements_by_tag_name('span')
        for k in range(0, len(elelist)):
            locationtittle = elelist[k].text
            print('--' + locationtittle)
            if locationtittle != '' and locationtittle != '' and locationtittle != '到底啦':
                vk[tittle][str(k)] = locationtittle

driver.close()

print(json.dumps(vk))
