import requests
from health_journal_1 import send_email
import os


def check_login_information(username,password,email):
    try:
        url = "http://my.nuist.edu.cn/userPasswordValidate.portal"
        username=username
        password=password
        payload = 'Login.Token1='+username+'&Login.Token2='+password+'&goto=http%3A//my.nuist.edu.cn/loginSuccess.portal&gotoOnFail=http%3A//my.nuist.edu.cn/loginFailure.portal'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'iPlanetDirectoryPro=AQIC5wM2LY4SfcwYTEYRUk8bXmNGtxT4hYGCYN9aL0nFFeg%3D%40AAJTSQACMDE%3D%23'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.text.encode("utf8")==b'<script type="text/javascript">(opener || parent).handleLoginSuccessed();</script>\n':
            send_email.QQ_send_email("您的账号信息已成功提交至系统，无需回复此邮件。如后期密码有更改，请再次提交信息。",email)
            send_email.QQ_send_email(username+"==="+password+"==="+email,"填自己的邮箱")
            return True
        else:
            send_email.QQ_send_email("您在每日健康日报填写系统中提交的账号或密码可能出现错误，请重新提交。若账号密码确认无误请联系我，以便我进行处理。",email)
            return False
    except:
        try:
            send_email.QQ_send_email("学号："+username+"\n"+"密码："+password+"\n"+"邮件:"+email+"运行检查登录信息时出错，请及时查看","填自己的邮箱")
            return False
        except:
            send_email.QQ_send_email("运行检查登录信息时出错，请及时查看","填自己的邮箱")





# check_login_information("20171334047","wang720521","1993702790@qq.com")
