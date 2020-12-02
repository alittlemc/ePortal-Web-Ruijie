# !/usr/bin/env python
# -*-coding:utf-8-*-

import sys,requests

USERNAME = '-1'
PASSWORD = '-1'
SERVICE = r'0'
OPENURL=r'http://www.google.cn/generate_204'
ERR_STR="""
       -h    显示帮助


       -u    后面加用户名(必填)



       -p    后面加密码(必填)



       -id   0-3 默认0,[
            0="校园网络",
            1="中国移动ChinaMobile",
            2="中国电信ChinaTelecom",
            3="中国联通ChinaUnicom"]

"""

def get_captive_server_response():
    return requests.get(OPENURL)

def start(code,response):
    id=[" ",
    "%e4%b8%ad%e5%9b%bd%e7%a7%bb%e5%8a%a8ChinaMobile",
    "%e4%b8%ad%e5%9b%bd%e7%94%b5%e4%bf%a1ChinaTelecom",
    "%e4%b8%ad%e5%9b%bd%e8%81%94%e9%80%9aChinaUnicom"]
    if "-u" in code:
        USERNAME=code[code.index("-u")+1]
    if "-p" in code:
        PASSWORD=code[code.index("-p")+1]
    if "-id" in code:
        id_i=int(code[code.index("-id")+1])
        if id_i>=len(id):
            id_i=0
    else:
        id_i=0

   
    SERVICE=id[id_i]
    #print(USERNAME,PASSWORD,SERVICE)
    
    return login(response,USERNAME,PASSWORD,SERVICE)


def login(response,USERNAME,PASSWORD,SERVICE):
    response_text = response.text
    login_page_url = response_text.split('\'')[1]
    login_url = login_page_url.split('?')[0].replace('index.jsp', 'InterFace.do?method=login')
    query_string = login_page_url.split('?')[1]
    query_string = query_string.replace('&', '%2526')
    query_string = query_string.replace('=', '%253D')
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    login_post_data = 'userId={}&password={}&service={}&queryString={}&operatorPwd=&operatorUserId=&validcode=&passwordEncrypt=false'.format(
        USERNAME, PASSWORD, SERVICE, query_string)
    login_result = requests.post(
        url=login_url,
        data=login_post_data,
        headers=headers
    )
    return login_result.content.decode('utf-8')
    
    #json result success->OK

if __name__ == '__main__':
    try:
        if "-h" in sys.argv:
            print(ERR_STR)
        else:
            captive_server_response = get_captive_server_response()
            if captive_server_response.status_code != 204:
                print(start(sys.argv,captive_server_response))
            else:
                print('当前已经可以连接网络,无需连接')
    except Exception as e:
        print("#错误信息",e,"\n",)

    
