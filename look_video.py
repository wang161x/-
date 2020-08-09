from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
import requests
from bs4 import BeautifulSoup
import re
import time
from lxml import etree
import logger
session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36 FS',
    'X-Requested-With': 'XMLHttpRequest',
}


def login():
    params = {
        'username': '41132919960525161x',
        'password': 'bj123465',
    }
    # r = session.post("https://www.bjjnts.cn/login", params=params, headers = headers)
    driver.get(url='https://www.bjjnts.cn/login')
    username = driver.find_element_by_name("username")
    password = driver.find_element_by_name("password")
    username.send_keys('41132919960525161x')
    password.send_keys("bj123465")
    sbm = driver.find_element_by_class_name("login_btn")
    time.sleep(1)
    sbm.click()

    # 点击个人中心
    try:
        driver.get(url='https://www.bjjnts.cn/userCourse')
        personal_center = driver.find_element_by_xpath('/html/body/div[4]/div/ul/li[2]/div/a/span')
        personal_center.click()
    except Exception:
        pass

    # 点击我的课程
    driver.get(url='https://www.bjjnts.cn/userCourse')
    my_learn_course = driver.find_element_by_xpath('/html/body/div[3]/div/div/ul/li[1]/a/span')
    my_learn_course.click()
    time.sleep(2)

    # 点击具体某一课程
    learning_course = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/ul/li[4]/div[1]/img')
    learning_course.click()

    # 手动点击使用摄像头
    a = input("请在您点击使用摄像头后按下回车！！！")


def play_video(i):
    global warning
    # 选择某一节课
    try:
        learning_class = driver.find_element_by_xpath(f'/html/body/div[3]/div/div/div/div[1]/div[2]/ul/li[{i}]/div/a/div/h4')
        learning_class.click()
        time.sleep(3)
    except Exception:
        return 1

    # 点击播放
    try:
        play_start = driver.find_element_by_xpath('//*[@id="studymovie"]')
        play_start.click()
    except ElementClickInterceptedException:
        input('请在人脸验证完毕之后点击回车键！！！')

    """
    探测下一节课是否已经解锁，未解锁，则循环找是否继续按钮，隔3s查找，若找不到则pass，找到点击按钮
    若下一节已经解锁，则播放下一节
    """
    while True:
        try:
            # //*[@id="layui-layer6"]/div[3]/a
            # //*[@id="layui-layer6"]/div[3]/a
            # //*[@id="layui-layer2"]/div[3]/a
            # //*[@id="layui-layer4"]/div[3]/a
            # //*[@id="layui-layer2"]/div[3]/a
            # //*[@id="layui-layer62"]/div[3]/a
            # //*[@id="layui-layer14"]/div[3]/a
            # //*[@id="layui-layer12"]/div[3]/a
            # //*[@id="layui-layer10"]/div[3]/a
            # //*[@id="layui-layer8"]/div[3]/a
            # //*[@id="layui-layer6"]/div[3]/a
            driver.find_element_by_xpath(f'//*[@id="layui-layer{warning}"]/div[3]/a')
            play_contiue = driver.find_element_by_xpath(f'//*[@id="layui-layer{warning}"]/div[3]/a')
            play_contiue.click()
            print(f'waring: {warning}')
            warning += 2
            print('出现提示！！')
        except Exception:
            print('未出现提示！！！')
        finally:
            # # 点击播放
            # play_start = driver.find_element_by_xpath('//*[@id="studymovie"]')
            # play_start.click()
            video = driver.find_element_by_xpath('//*[@id="studymovie"]')
            driver.execute_script("return arguments[0].play()", video)
            time.sleep(10)
        print(re.findall(r'已完成\n(.*)', driver.find_elements_by_partial_link_text(u'已完成')[i-1].text))
        if re.findall(r'已完成\n(.*)', driver.find_elements_by_partial_link_text(u'已完成')[i-1].text)[0] == '100%':
            print('已经看完了！！！')
            # learning_class = driver.find_element_by_xpath(
            #     '/html/body/div[3]/div/div/div/div[1]/div[2]/ul/li[]/div/a/div/h4')
            # learning_class.click()
            break
        else:
            print('还没有看完！！！！')


if __name__ == '__main__':
    driver = webdriver.Chrome()
    login()
    warning = 2
    for i in range(56, 60):
        print(i)
        play_video(i)
