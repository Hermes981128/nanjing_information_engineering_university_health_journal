from selenium import webdriver
from health_journal_1 import send_email
import threading
class health_journal(threading.Thread):
    def __init__(self, username, password, email):
        threading.Thread.__init__(self)
        self.username = username
        self.password = password
        self.email = email
    def run(self):
        fil_in_health_journal(self.username,self.password,self.email)


def fil_in_health_journal(username, password, email):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")#无头浏览器
        options.add_argument('--disable-gpu') #gpu不渲染
        driver = webdriver.Chrome("D:\Crawler\chromedriver.exe", options=options)
        driver.implicitly_wait(10)  # 隐性等待，最长等30秒
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
        driver.find_element_by_xpath("/html/body/div[7]/div/div[2]/button").click()
        driver.quit()
        # print(time.ctime() + "==" + username + ":健康日报已完成")
        send_email.QQ_send_email(username + "您今日健康日报已填写提交成功，请前往信息门户查看。", email)
    except:
        send_email.QQ_send_email(username+"==="+password+"==="+email+"===填写健康日报出现错误","1993702790@qq.com")