import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select


class MMUEDigitalTwins:

    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.login_url = "/login"
        self.username = username
        self.password = password
        self.driver = None

    def close_browser(self):
        self.driver.close()

    def open_browser(self):
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        options = webdriver.ChromeOptions()
        options.add_argument('user-agent=' + ua)
        driver = webdriver.Chrome(options=options)
        driver.get(self.base_url + self.login_url)
        driver.implicitly_wait(60)
        driver.maximize_window()
        self.driver = driver

    def login_user(self):
        self.driver.find_element_by_css_selector("#form_item_username").send_keys(self.username)
        self.driver.find_element_by_css_selector("#form_item_pwd").send_keys(self.password)
        self.driver.find_element_by_css_selector("#main > div > form > div:nth-child(4) > "
                                                 "div > div > div > button").click()

    def change_navi_bar(self):
        self.driver.find_element_by_xpath('//*[@id="leftMenus"]/li[7]/div/span[2]').click()
        self.driver.find_element_by_xpath('//*[@id="sub_menu_6_$$_duomotaidabao-popup"]/li[9]/span').click()

    def click_cloud_model_button(self):
        self.driver.find_element_by_css_selector("#app > div > div.el-dialog__wrapper.modeswitch > "
                                                 "div > div.el-dialog__body > span > "
                                                 "div:nth-child(1) > p.ms_btn").click()

    def check_in_digital_twins_iframe(self):
        """change iframe to digital"""
        iframe_ele = self.driver.find_element_by_css_selector("#app > div > iframe")
        self.driver.switch_to.frame(iframe_ele)

    def check_out_digital_twins_iframe(self):
        """change iframe to default"""
        self.driver.switch_to.parent_frame()

    def click_start_serve(self):
        try:
            self.driver.find_element_by_css_selector("#playButton").click()
            return 0
        except Exception as e:
            print("not find playButton 1", e)

        try:
            WebDriverWait(self.driver, 30).until(ec.visibility_of_element_located((By.CSS_SELECTOR,
                                                                                   "#playButton"))).click()
        except Exception as e:
            print("not find playButton 2", e)

    def click_setting_button(self):
        self.driver.find_element_by_css_selector(
            "#app > div > button.el-button.confbtn.el-button--default.el-button--mini.is-plain > span").click()

    @staticmethod
    def setting_select_option(element, text):
        return Select(element).select_by_visible_text(text)

    def setting_select_twins_type(self, twins_type):
        self.driver.find_element_by_css_selector("#app > div > div:nth-child(7) > div > div > section > div > div > div:nth-child(2) > div").click()
        ele = self.driver.find_element_by_css_selector("body > div:nth-child(8) > div.el-scrollbar > div.el-select-dropdown__wrap.el-scrollbar__wrap > ul")
        self.setting_select_option(ele, twins_type)

    def setting_select_twins_dress(self, twins_dress):
        self.driver.find_element_by_css_selector("#app > div > div:nth-child(7) > div > div > section > div > div > div:nth-child(3) > div").click()
        ele = self.driver.find_element_by_css_selector("body > div:nth-child(8) > div.el-scrollbar > div.el-select-dropdown__wrap.el-scrollbar__wrap > ul")
        self.setting_select_option(ele, twins_dress)

    def setting_select_twins_background_pic(self, background_pic):
        self.driver.find_element_by_css_selector("#app > div > div:nth-child(7) > div > div > section > div > div > div:nth-child(4) > div").click()
        ele = self.driver.find_element_by_css_selector("body > div:nth-child(8) > div.el-scrollbar > div.el-select-dropdown__wrap.el-scrollbar__wrap > ul")
        self.setting_select_option(ele, background_pic)

    def setting_select_twins_background_color(self, background_color):
        ele = self.driver.find_element_by_css_selector("#app > div > div:nth-child(7) > div > div > section > div > div > div:nth-child(5) > div > div")

    def setting_save_button(self):
        self.driver.find_element_by_css_selector("#app > div > div:nth-child(7) > div > div > section > div > div > div.btnbox > button > span").click()

    def on_start(self):
        self.open_browser()
        self.login_user()
        self.change_navi_bar()
        self.click_cloud_model_button()

        self.check_in_digital_twins_iframe()
        self.click_start_serve()
        self.check_out_digital_twins_iframe()

        time.sleep(5)
        self.click_setting_button()
        self.setting_select_twins_type("SchoolGirl")
        self.setting_select_twins_dress("SchoolGirl_White")
        self.setting_select_twins_background_pic("3DRoom")
        self.setting_save_button()

    def on_stop(self):
        self.close_browser()


if __name__ == '__main__':
    test_url = "http://10.11.35.104:4000"
    user_1 = "admin"
    pwd_1 = "123456"
    instance_1 = MMUEDigitalTwins(test_url, user_1, pwd_1)
    instance_1.on_start()
    time.sleep(10)
    instance_1.on_stop()
