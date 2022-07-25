from time import sleep

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy


def driver_init():
    desired_caps = {
        'platformName': 'Android',  # 被测手机是安卓
        'platformVersion': '6.0',  # 手机安卓版本
        'deviceName': 'xxx',  # 设备名，安卓手机可以随意填写
        'appPackage': 'cn.xuexi.android',  # 启动APP Package名称
        'appActivity': 'com.alibaba.android.rimet.biz.SplashActivity',  # 启动Activity名称
        'unicodeKeyboard': True,  # 使用自带输入法，输入中文时填True
        'resetKeyboard': True,  # 执行完程序恢复原来输入法
        'noReset': True,  # 不要重置App
        # 'newCommandTimeout': 12000,
        'automationName': 'UiAutomator2'
    }
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    return driver


# 向上滑动
def swipe_up(driver):
    x1 = int(driver.get_window_size()['width'] * 0.5)
    y1 = int(driver.get_window_size()['height'] * 0.7)
    y2 = int(driver.get_window_size()['height'] * 0.1)
    driver.swipe(x1, y1, x1, y2, 1000)


# 返回
def back(driver):
    driver.tap([(0, 36), (84, 112)], 100)


# 退出app自动化
def esc(driver):
    driver.quit()


# 任务一：选读文章
def read_article(driver):
    driver.implicitly_wait(40)
    print("--------> 开始执行任务一：选读文章 <--------")
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("要闻")').click()
    # 获取6条要闻头条
    click_number = 1
    while click_number < 7:
        eles = driver.find_elements(AppiumBy.ID, 'cn.xuexi.android:id/general_card_title_id')
        if eles:
            # eles = driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("“学习强国”学习平台")')
            for ele in eles:
                ele.click()
                sleep(60)
                print("选读文章完成{}篇, 累计{}分钟".format(click_number, click_number))
                back(driver)
                # driver.find_element(AppiumBy.CLASS_NAME, 'android.widget.ImageView').click()
                click_number = click_number + 1
                if click_number == 7:
                    break
            swipe_up(driver)
        else:
            swipe_up(driver)
    print("完成任务一：选读文章")


# 任务二：发表观点
def post_views(driver):
    sleep(1)
    print("--------> 开始执行任务二：发表观点 <--------")
    ele = driver.find_element(AppiumBy.ID, 'cn.xuexi.android:id/general_card_title_id')
    print("进入发布观点文章")
    if ele:
        ele.click()
        ele_text_view = driver.find_element(AppiumBy.CLASS_NAME, 'android.widget.TextView')
        ele_text_view.click()
        ele_text = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("好观点将会被优先展示")')
        ele_text.click()
        print("输入观点：祖国越来越好")
        ele_input = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("好观点将会被优先展示")')
        ele_input.send_keys('祖国越来越好')
        print("发布")
        ele_post = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("发布")')
        ele_post.click()
        back(driver)
    else:
        swipe_up(driver)
    print("完成任务二：发表观点")


# 任务三：本地频道
def read_channel(driver):
    print("--------> 开始执行任务三：本地频道 <--------")
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("广东")').click()
    print("使用频道内容")
    ele = driver.find_element(AppiumBy.XPATH,
                              '//androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[1]')
    ele.click()
    sleep(1)
    driver.tap([(0, 36), (84, 112)], 100)
    print("完成任务三：本地频道")


# 任务四：视听学习
def read_tv(driver):
    print("--------> 开始执行任务四：视听学习 <--------")
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, '电视台').click()
    i = 1
    while i < 7:
        # eles = driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("中央广播电视总台")')
        eles = driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR,
                                    'new UiSelector().className("android.widget.TextView").textContains("01:")')
        if eles:
            for ele in eles:
                ele.click()
                sleep(60)
                print("视听学习完成{}次, 累计{}分钟".format(i, i))
                i = i + 1
                # 返回
                # driver.tap([(0, 36), (84, 112)], 100)
                back(driver)
            # driver.swipe(500, 1100, 500, 100, 1000)
        else:
            swipe_up(driver)
    print("完成任务四：视听学习")


def star():
    driver = driver_init()
    read_article(driver)
    post_views(driver)
    read_channel(driver)
    read_tv(driver)
    print(" 共得 26 积分 ")
    print("3秒后自动退出程序")
    sleep(3)
    esc(driver)


if __name__ == '__main__':
    star()
