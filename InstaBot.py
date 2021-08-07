import os
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.dirpath = os.path.dirname(__file__)
        self.driver = webdriver.Chrome(os.path.join(self.dirpath, 'chromedriver'))
        self.base_url = 'https://www.instagram.com/'
        self.wait = WebDriverWait(self.driver, 30)
        self.posts = 0

    def login(self):
        driver = self.driver
        driver.get(self.base_url)
        wait = self.wait
        input_field = wait.until(ec.visibility_of_all_elements_located((By.CLASS_NAME, "f0n8F")))
        driver.implicitly_wait(1)
        username = input_field[0]
        username.send_keys(self.username)
        password = input_field[1]
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(5)
        print('-------checking save login-------')
        try:
            not_now = driver.find_element_by_class_name('yWX7d')
            not_now.click()
        except UnexpectedAlertPresentException as ex:
            print(ex)
            pass
        print('-------check notifications option-------')
        wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "piCib")))
        no_button = driver.find_element_by_class_name('HoLwm')
        no_button.click()

    def get_details_of_account(self, account):
        wait = self.wait
        driver = self.driver
        print('-------redirect to friend profile-------')
        driver.get(self.base_url + account)
        wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'g47SY ')))
        spans = driver.find_elements_by_class_name("g47SY ")
        user_details = {
            'number_of_posts': spans[0].text,
            'followers': spans[1].get_attribute("title"),
            "following": spans[2].text
        }
        print(user_details)
        self.posts = int(spans[0].text)
        driver.close()

    def like_photos_of_friend(self, friend):
        wait = self.wait
        driver = self.driver
        print('-------redirect to friend profile-------')
        driver.get(self.base_url + friend)

        time.sleep(2)
        try:
            driver.find_element_by_class_name("rkEop")
        except NoSuchElementException:
            pass

        wait.until(ec.visibility_of_all_elements_located((By.CLASS_NAME, "v1Nh3")))
        img_divs = driver.find_elements_by_class_name('v1Nh3')
        img_divs[0].find_element_by_tag_name('a').click()
        count = 0
        while True:
            like_button = wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "fr66n")))
            aria_label = like_button.find_element_by_css_selector('svg').get_attribute("aria-label")
            if aria_label == 'Unlike':
                count = count + 1
                like_button.click()
            time.sleep(1)
            try:
                next_btn = driver.find_element_by_class_name('coreSpriteRightPaginationArrow')
                next_btn.click()
            except NoSuchElementException:
                print("next not found")
                break
        print("You liked " + str(count) + " posts of" + friend)
        driver.find_element_by_xpath('/html/body/div[6]/div[3]/button').click()
        driver.close()
