'''
*************************************************************************** DISCLAIMER ****************************************************************************

CODE IS STILL BEING WORKED ON, ISN'T READY FOR DISTRIBUTION/USE AND THEREFORE ISN'T OPTIMIZED

You can test the send_dm, auto_reply and cycle_stories functions, any feedback is appreciated.

'''
import datetime
import os
import apscheduler
import time
from json import dump, load
from selenium import webdriver
from time import sleep
from os.path import exists
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from apscheduler.schedulers.background import BackgroundScheduler
from selenium.webdriver.support import expected_conditions as EC


class Botstagram:
    '''Set driverpath to Chromedriver executable path to be able to use Chrome'''

    def __init__(self, driverpath):
        self.driver = webdriver.Chrome(executable_path=driverpath)

    def login(self, username, password):
        '''To reset cookies, delete the "ig.json" file and run the script again.'''
        self.driver.get("https://instagram.com/")
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
                not_now_button = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Not now']")))
                not_now_button.click()
                notifications_button = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Not now"]')))
                notifications_button.click()

                cookie = self.driver.get_cookies()
                with open("Cookies/ig.json", "w") as file:
                    dump(cookie, file)
                print("Cookies saved!")

                self.driver.refresh()

            except:
                raise KeyError("Error! Login failed.")

        else:
            with open("./Cookies/ig.json", "r") as _file:
                for i in load(_file):
                    self.driver.add_cookie(i)

                sleep(1)

                try:
                    username_input = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']")))
                    password_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='password']")
                    username_input.send_keys(username)
                    password_input.send_keys(password)

                    login_button = WebDriverWait(self.driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
                    login_button.click()
                    not_now_button = WebDriverWait(self.driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[text()='Not now']")))
                    not_now_button.click()
                    notifications_button = WebDriverWait(self.driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, '//button[text()="Not Now"]')))
                    notifications_button.click()

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
                    NextStory = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[contains(@class, 'FhutL')]")))
                    NextStory.click()
                    sleep(0.03)
                except:
                    break
        except:
            print("Did not click on next")
        print("Done. ")

    def send_dm(self, recipient, text):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//*[name()='svg' and @aria-label='Messenger']"))).click()
            conversations_text = self.driver.find_element(
                By.XPATH, "//div[text()='{}']".format(recipient)
            )
            conversations_text.click()
            text_field = self.driver.find_element(By.CSS_SELECTOR, "textarea")
            text_field.send_keys(text)
            sendit = self.driver.find_element(By.XPATH, "//button[text()='Send']")
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(sendit)).click()
        except:
            raise Exception("Could not send DM...")

        print("DM successfully sent to", recipient + ".")

    def schedule_dm(self, time_, function):
        while True:
            time_ = datetime.datetime(time_).timestamp()
            if time_ == time.time():
                pass
            sleep(3000)

        scheduler = BackgroundScheduler()
        scheduler.add_job(function, 'interval', minutes=2)
        scheduler.start()

    def auto_reply(self, text):
        while True:
            if len(self.driver.find_elements( By.XPATH, "//div[@class='KdEwV']/div[@class='J_0ip  Vpz-1  TKi86 ']/div[@class='bqXJH']" )) != 0:
                print("It's there! ")
                try:
                    WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[name()='svg' and @aria-label='Messenger']"))).click()

                    to = self.driver.find_element(By.XPATH, "//div[@class='             qF0y9          Igw0E     IwRSH      eGOV_          ui_ht                                                                          i0EQd                                   ']/div[@class='_7UhW9   xLCgt        qyrsm KV-D4              fDxYl     ']").text
                    self.send_dm(to, text)
                    back_button = self.driver.find_element(By.XPATH, "//*[name()='svg' and @aria-label='Home' and @class='_8-yf5 ']")
                    back_button.click() 
                except:
                    print("Not found...")
                # placeholder

            else:
                print("Not found...")
            sleep(5.5)


test = Botstagram("/Users/kerim/PycharmProjects/APIs/venv/bin/chromedriver")

test.login("your_username", "password")
#test.send_dm("User", "This message was sent using a bot :)")
test.auto_reply("I'm currently busy. ")
# test.cycle_stories()
# test.schedule_dm()

