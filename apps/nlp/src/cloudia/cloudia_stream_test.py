import os
import time
from selenium import webdriver


class MyTestCase:

    def __init__(self):
        self.stop_path = None
        self.start_path = None
        self.stop = None
        self.start = None
        self.driver = None

    def on_start(self):
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        options = webdriver.ChromeOptions()
        options.add_argument('user-agent=' + ua)
        driver = webdriver.Chrome(options=options)
        self.driver = driver
        driver.get("http://39.100.122.115:8090/rdk-0523/")
        driver.maximize_window()

        driver.find_element_by_css_selector("#tenantId").send_keys("gingerlite87")
        driver.find_element_by_css_selector("#accountId").send_keys("355929090035651")
        driver.find_element_by_css_selector("#robotId").send_keys("355929090035651")
        driver.find_element_by_css_selector("#vadAddress").send_keys(
            "wss://psc-rdk-dit87.harix.iamidata.com/ps-controller")

        start = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[1]/div/button[1]")
        stop = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[1]/div/button[2]")
        self.start = start
        self.stop = stop

        start_execute_time = time.strftime("%Y-%m-%d-%H-%M-%S")
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        now_path = os.path.join(path, start_execute_time)
        start_path = os.path.join(now_path, "start")
        stop_path = os.path.join(now_path, "stop")
        if not os.path.exists(now_path):
            os.makedirs(now_path)
            os.makedirs(start_path)
            os.makedirs(stop_path)

        self.start_path = start_path
        self.stop_path = stop_path

    def on_stop(self):
        self.driver.close()

    def testing(self):
        for i in range(100):
            self.start.click()
            time.sleep(7)
            self.driver.save_screenshot(os.path.join(self.start_path, str(i) + ".png"))
            self.stop.click()
            time.sleep(3)
            self.driver.save_screenshot(os.path.join(self.stop_path, str(i) + ".png"))


def runner():
    t = MyTestCase()
    t.on_start()
    t.testing()
    t.on_stop()


if __name__ == '__main__':
    runner()
