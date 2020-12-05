# ePortal-Web-Ruijie
使用python定义post报文实现校园网登录.

---

# 依赖
> pip install requests

---

# 语法

> python ruijielogin.py -n <用户名> -p <密码> -id <运营商id>
``` bash


       -h    显示帮助


       -u    后面加用户名(必填)


       -p    后面加密码(必填)
            1)可以直接填写密码
            #暴力破解注意事项# 跑密码建议请选择可以登录"校园网络"的接入点测试,或者请选择正确的运营商.
            2)file:文件路径 可以实现跑弱口令,逐行读取.
            3)run:数字1-数字2 从 数字1 跑到 数字2 结束,
                (身份证后六位范围010000-319999).


       -v   显示完整输出


       -id   0-3 默认0,[
            0="校园网络",
            1="中国移动ChinaMobile",
            2="中国电信ChinaTelecom",
            3="中国联通ChinaUnicom"]
```
> 如果你的认证有不同的运营商服务选项,请修改start函数中的id数组,用记得URLencode.

---

# 说明
参考了原项目RuijiePortalLoginTool的python的报文格式（不过现在源项目已经被删除）
