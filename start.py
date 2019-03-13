import requests
from requests.exceptions import RequestException
import urllib.parse
import time
import json
import sys


def taobao_getpage():
    param = {
        "upnid": 0, "token": "a4dac375acb05b2a8b1cc35660b37c2f9b4e1ae4", "upbcat": 21140462, "is_industry_shoal": "yes",
        "industry": 0, "maxn": 200, "needTab": "true", "page_s": "0", "page_n": "10"
    }
    par = json.dumps(param)
    data = {
        'appId': '3489',
        'params': par,
        'needTab': 'true',
    }
    # json.dumps(data)
    query = {
        'jsv': '2.4.5',
        'appKey': 12574478,
        't': int(round(time.time() * 1000)),
        'sign': '387d830bb184a0829c85101f496e8575',
        'api': 'mtop.relationrecommend.WirelessRecommend.recommend',
        'v': '2.0',
        'preventFallback': 'true',
        'type': 'jsonp',
        'dataType': 'jsonp',
        'callback': 'mtopjsonp1',
        'data': urllib.parse.quote(json.dumps(data))

    }
    header = {
        'cookie': 'cookie2=513a56afb0efabdf584f0f1be41b80f8; t=e83e226271d411d32c64cf2b99613876; _tb_token_=358967e9b83a; cna=R08OFXsJ/TgCAXxdxAj0EM5z; _m_h5_tk=a9ba60896007b84b01b46eb2c7209543_1552467193948; _m_h5_tk_enc=6960be6291e5f2c51d484fc2e606c152; isg=BNXVADGAJZxdwAEQIvm0s00p5NEjwUMcZR3bBFd6kcybrvWgHyKZtON8fvS9taGc'
    }
    mainurl = 'https://h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/'
    testquery = '?jsv=2.4.5&appKey=12574478&t=1552457356420&sign=387d830bb184a0829c85101f496e8575&api=mtop.relationrecommend.WirelessRecommend.recommend&v=2.0&preventFallback=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7b%22appId%22%3a%223489%22%2c%22params%22%3a%22%7b%5c%22upnid%5c%22%3a0%2c%5c%22token%5c%22%3a%5c%22a4dac375acb05b2a8b1cc35660b37c2f9b4e1ae4%5c%22%2c%5c%22upbcat%5c%22%3a21140462%2c%5c%22is_industry_shoal%5c%22%3a%5c%22yes%5c%22%2c%5c%22industry%5c%22%3a0%2c%5c%22maxn%5c%22%3a200%2c%5c%22needTab%5c%22%3a%5c%22true%5c%22%2c%5c%22page_s%5c%22%3a%5c%220%5c%22%2c%5c%22page_n%5c%22%3a%5c%2210%5c%22%7d%22%2c%22needTab%22%3a%22true%22%7d'
    try:
        print(query)
        response2 = requests.get(url=mainurl + testquery, headers=header)
        print(response2.text)
        response = requests.get(url=mainurl, headers=header, params=query)
        print(response2.url)
        print(response.url)
        return response.text
    except RequestException as e:
        print('request is error!', e)


def main():
    html = taobao_getpage()
    print(html)


if __name__ == '__main__':
    print(sys.getdefaultencoding())
    main()
