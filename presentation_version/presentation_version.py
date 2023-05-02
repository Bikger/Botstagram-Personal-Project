import os
from json import dump, load
from selenium import webdriver
from time import sleep
from datetime import datetime
from os.path import exists
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from apscheduler.schedulers.background import BackgroundScheduler
from selenium.webdriver.support import expected_conditions as EC

class Botstagram:

    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def login(self, username, password):
        '''To reset cookies, delete the "ig.json" file in your directory and run the script again.'''
        self.driver.get("https://www.instagram.com/accounts/login/")
        self.driver.implicitly_wait(7)

        if not exists("./Cookies/ig.json"):
            try:
                os.makedirs('Cookies')
            except:
                print("File 'Cookies' exists. ")
            try:
                username_input = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']")))
                password_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='password']")
                username_input.send_keys(username)
                password_input.send_keys(password)

                login_button = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
                login_button.click()

                self.driver.get("https://www.instagram.com")
                self.driver.implicitly_wait(7)

                cookie = self.driver.get_cookies()
                with open("Cookies/ig.json", "w") as file:
                    dump(cookie, file)
                print("Cookies saved!")


            except:
                raise Exception("Error! Login failed.")
        else:
            with open("./Cookies/ig.json", "r") as _file:
                for i in load(_file):
                    self.driver.add_cookie(i)

                sleep(1)

                try:
                    username_input = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']")))
                    password_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='password']")
                    username_input.send_keys(username)
                    password_input.send_keys(password)

                    login_button = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
                    login_button.click()

                    sleep(6)

                    self.driver.get("https://www.instagram.com/direct/inbox")
                    self.driver.implicitly_wait(7)

                    not_now_button = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='_a9-- _a9_1']")))
                    not_now_button.click()

                except:
                    raise Exception("Login failed! ")

                print("Login successful. ")

    def cycle_stories(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Story')]"))).click()
        try:
            print("Cycling through stories...")
            while True:
                try:
                    next_story = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[contains(@class, 'FhutL')]")))
                    next_story.click()
                    sleep(0.03)
                except:
                    break
        except:
            print("Did not click on next")
        print("Done. ")

    def send_dm(self, recipient, text):
        try:
            '''
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//*[name()='svg' and @aria-label='Messenger']"))).click()
            '''
            message_thread = self.driver.find_element(
                By.CSS_SELECTOR, "[aria-label='Unread']".format(recipient))
            message_thread.click()

            sleep(1)

            text_field = self.driver.find_element(By.CSS_SELECTOR, "textarea")
            text_field.send_keys(text)
            sendit = self.driver.find_element(By.XPATH, "//div[text()='Send']")
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(sendit)).click()
        except:
            raise Exception("Could not send DM...")

        print("DM successfully sent to", recipient + ".")

        chat_button = self.driver.find_element(By.CSS_SELECTOR, "[aria-label='Messenger']")
        chat_button.click()

    def schedule(self, time_, function):
        print("The time is: '{}'".format(datetime.now()))
        scheduler = BackgroundScheduler()
        scheduler.add_job(function, 'interval', minutes=1)
        scheduler.start()

    def auto_reply(self, text):
        while True:
            if len(self.driver.find_elements(By.CSS_SELECTOR, "[aria-label='Unread']")) > 0:
                print("It's there! ")
                try:

                    to = self.driver.find_element(By.XPATH, "//span[@style='line-height: 18px;']").text
                    self.send_dm(to, text)
                    sleep(3)

                except:
                    print("DM not sent!")

            else:
                print("Not found...")
            sleep(3)


test = Botstagram()

test.login("username", "pass")
test.auto_reply("Pozdrav svima! Ja sam Botstagram. Ova poruka je poslana automatski.")
# test.send_dm("Luka", "This message was sent using a bot :)")r
# test.auto_reply("I'm currently busy. ")
# test.cycle_stories()
# test.schedule()


