from selenium import webdriver

data_spm = {
    "女装": "nvzhuang",
    "男装": "nanzhuang",
    "手机数码": "shuma",
    "鞋靴": "xie",
    "食品": "shipin",
    "百货": "baihuo",
    "家电": "jiadian",
    "美妆洗护": "meizhuang",
    "内衣配饰": "peishi",
    "运动户外": "yundong",
    "母婴": "muying",
    "箱包": "xiangbao",
    "生活服务": "shenghuo",
    "家装": "jiazhuang",
    "整车车品": "qiche",
    "家居家纺": "jiafang",
    "珠宝配饰": "zhubao",
    "鲜花宠物": "huaniao",
    "生鲜": "shengxian",
    "图书乐器": "tushu",
    "现代农业": "nongye"
}


def getDriver():
    mobile_emulation = {"deviceName": "Nexus 5"}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    return chrome_options
