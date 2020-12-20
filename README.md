# ePortal-Web-Ruijie
使用python定义post报文实现校园网登录.

---

# 依赖
> pip install requests

---

# 语法
> 基本**必选**项
> python ruijielogin.py **-n** *<用户名>* **-p** *<密码>* **-id** *<运营商id>*

> 1.跑密码字典(file)
> python ruijielogin.py **-n** *<用户名>* **-p** file:文件路径 **-id** *0*
> *逐行读取,自动去除回车,登录成功后停止.

> python ruijielogin.py -n** *2021* **-p** file:/home/pi/rklin.txt **-id** *0*
> > **/home/pi/rklin.txt内容**
> > 123456
> > abcdefg

> 2.跑数字密码(run)
> python ruijielogin.py **-n** *<用户名>* **-p** run:数字1-数字2 **-id** *<运营商id>*
> 从数字1到数字2依次作为密码,如果范围内有数字小于6位,自动在前面补够0,登录成功后停止.

> python ruijielogin.py -n** *2021* **-p** run:10000-3199999 **-id** *0*
> 10000因为不足6位被识别为010000
> 同理 10=>000010

> 循环登录(设置执行间隔,会持续登录)
> python ruijielogin.py **-n** *<用户名>* **-p** *<密码>* **-id** *<运营商id>* **-t** *<延迟时间秒>*
> python ruijielogin.py -n** *2021* **-p** *123456* **-id** *0* **-t** *30*
> 每30s发送一次登录请求

``` bash
       -h    显示帮助,输入此项后只输出提示.

       -v    显示完整输出.

       -u [字符串 user]    *后面加用户名(必填).

       -p [字符串 password]   *后面加密码(必填).
             1)可以直接填写密码
             #暴力破解注意事项# 跑密码建议请选择可以登录"校园网络"的接入点测试,或者请选择正确的运营商.
             2)file:文件路径 可以实现跑弱口令,逐行读取.
             3)run:数字1-数字2 从 数字1 跑到 数字2 结束,如果范围内有数字小于6位,自动在前面补够0
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
```
> 如果你的认证有不同的运营商服务选项,请修改start函数中的id数组,用记得URLencode.

---

# 更新
v1.0 实现基础的登录;
v1.1 完善部分功能;
v1.2 新增加密码测试;
v1.3 新增加循环登录功能;

---

# 说明
参考了原项目RuijiePortalLoginTool的python的报文格式（不过现在源项目已经被删除）
