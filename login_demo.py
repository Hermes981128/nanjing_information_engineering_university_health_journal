from flask import Flask, render_template, request
from health_journal_1 import check_login_information
import time
from selenium import webdriver
# from health_journal_1 import fill_in_health_journal
from health_journal_1 import send_email

options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # 无头浏览器
# options.add_argument('--disable-gpu')  # gpu不渲染
driver = webdriver.Chrome("D:\Crawler\chromedriver.exe", options=options)
driver.implicitly_wait(10)  # 隐性等待，最长等30秒
def fil_in_health_journal(username, password, email):
    try:
        driver.delete_all_cookies()
        driver.get("http://my.nuist.edu.cn/login.portal", )  # 进入登录页面
        username_input_box = driver.find_element_by_id("username")  # 寻找用户名输入框
        username_input_box.send_keys(username)  # 填入用户名
        password_input_box = driver.find_element_by_id("password")  # 寻找密码输入框
        password_input_box.send_keys(password)  # 填入密码
        driver.find_element_by_name("btn").click()  # 点击登录
        driver.find_element_by_class_name("portletFrame")  # 等待页面加载
        driver.get("http://e-office2.nuist.edu.cn/infoplus/form/XNYQSB/start")  # 进入健康日报页面
        driver.find_element_by_name("fieldSTQKfrtw").send_keys("37.0")  # 填写温度
        driver.find_element_by_name("fieldCNS").click()  # 寻找承诺选框并点击
        driver.find_element_by_class_name("command_button_content").click()  # 点击确认填报
        driver.find_element_by_xpath("/html/body/div[7]/div/div[2]/button[1]").click()
        driver.find_element_by_class_name("dialog_footer").find_element_by_tag_name("button").click()

        # driver.quit()
        # print(time.ctime() + "==" + username + ":健康日报已完成")
        send_email.QQ_send_email(username + "您今日健康日报已填写提交成功，请前往信息门户查看。", email)
    except:
        send_email.QQ_send_email(username+"==="+password+"==="+email+"===填写健康日报出现错误","填自己的邮箱")




app = Flask(__name__)
app.secret_key = "yun"


@app.route("/")
def index():
    # if int(time.time()) % 86400 > 82800:
    #     return render_template("pause_to_submit.html")
    # elif int(time.time()) % 86400 < 3600:
    #     return render_template("pause_to_submit.html")
    #
    # else:
        return render_template("login.html")


@app.route('/submitted_successful', methods=["POST", "GET"])
def successful():
    if request.method == "POST":
        username = request.form.get("student_id")
        password = request.form.get("password")
        email = request.form.get("email")
        print(username, password, email)
        if username=="" and username:
            return render_template("failure_to_submit.html")
        elif password=="":
            return render_template("failure_to_submit.html")
        elif password=="":
            return render_template("failure_to_submit.html")
        result = check_login_information.check_login_information(username, password, email)
        if result == True:
            informatin = ""
            with open("account_password_record.txt", "r+", encoding="UTF-8") as f:
                for i in f.readlines():
                    if username in i:
                        continue
                    informatin = informatin + i
            with open("account_password_record.txt", "w", encoding="UTF-8") as f:
                f.writelines(informatin)
                informatin = ""
            with open("account_password_record.txt", "r+", encoding="UTF-8") as f:
                for i in f.readlines():
                    informatin = informatin + i

                if username in informatin:
                    pass
                else:
                    f.writelines(username + "=" + password + "=" + email + "\n")
            # fill_in_health_journal.health_journal(username, password, email).run()
            fil_in_health_journal(username,password,email)
            return render_template("submitted_successful.html")
        else:
            return render_template("failure_to_submit.html")

    else:
        return render_template("failure_to_submit.html")

if __name__ == "__main__":
    app.run()
    # host = "0.0.0.0", port = 8090
