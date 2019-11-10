import pathlib
import os
import time
import utility
import warnings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class whatsapp():
    def __init__(self):
        self.opts()
        warnings.filterwarnings("ignore", category=DeprecationWarning)  # ignoring DeprecationWarning

    def opts(self):
        self.options = Options()
        self.options.add_argument("--mute-audio") # Mute audio
        self.options.add_argument('--user-data-dir='+os.getcwd()+'\\profile') # User profile directory
        self.options.add_argument('window-size=0x0')

    def close(self):
        os.remove(os.getcwd()+'\\temporary\\session\\session.data')
        self.driver.close()

    def initialize(self, webdriverfile): # driver initializing
        try:
            pathlib.Path(os.getcwd()+'\\session\\').mkdir(parents=True, exist_ok=True)
            with open(os.getcwd()+'\\session\\session.data', 'r') as f:
                session_id, executor_url = f.read().split(';')
            opts = Options()
            capabilities = opts.to_capabilities()
            self.driver = webdriver.Remote(command_executor=executor_url, desired_capabilities=capabilities)
            self.driver.close()
            self.driver.session_id = session_id

        except:
            self.driver = webdriver.Chrome(executable_path = webdriverfile, options=self.options)
            self.driver.set_window_position(-10000,0)
            pathlib.Path(os.getcwd()+'\\session\\').mkdir(parents=True, exist_ok=True)
            with open(os.getcwd()+'\\session\\session.dat', 'w+') as f:
                data = self.driver.session_id+';'+self.driver.command_executor._url
                f.write(data)
        self.driver.get('https://web.whatsapp.com')
        return self.driver

    def check_auth(self):
        while True:
            try:
                self.driver.find_element_by_class_name("landing-wrapper")
                return False
            except:
                try:
                    self.driver.find_element_by_xpath('//div[@tabindex="-1"]')
                    return True
                except: pass

    def element_presence(self, by, xpath, time):  # element presence condition
        element_present = EC.presence_of_element_located((By.XPATH, xpath))
        WebDriverWait(self.driver, time).until(element_present)

    def element_absence(self, by, xpath, time): # element absence condition
        element_present = EC.presence_of_element_located((By.XPATH, xpath))
        WebDriverWait(self.driver, time).until_not(element_present)

    def get_qr_code(self):
        try: self.driver.find_element(By.XPATH, '//span[@data-icon="refresh-l-light"]').click()
        except: pass
        self.element_presence(By.XPATH,'/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div/img',30)
        return self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div/img').get_attribute("src")

    def logout(self): # logging out to whatsapp
        self.driver.get('https://web.whatsapp.com')
        while True:
            try:
                self.driver.find_element(By.XPATH , '/html/body/div[1]/div/div/div[3]/div/header/div[2]/div/span/div[3]/div/span').click()
                time.sleep(1)
                break
            except:
                pass
        while True:
            try:
                self.driver.find_element(By.XPATH , '/html/body/div[1]/div/div/div[3]/div/header/div[2]/div/span/div[3]/span/div/ul/li[7]/div').click()
                break
            except:
                pass
        return 1

    def send_text(self, phone, text):
        condition = text.replace('\n', '').replace(' ','')
        try:
            if condition != '':
                self.driver.get("https://web.whatsapp.com/send?phone="+format(phone))
                try:    self.driver.switch_to_alert().accept()
                except: pass
                texts = text.split('\n')
                for _text in texts:
                    __text = utility.decode(_text)
                    self.element_presence(By.XPATH,'/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2][@data-tab="1"]',30)
                    self.driver.find_element(By.XPATH , '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2][@data-tab="1"]').send_keys(__text)
                    self.driver.find_element(By.XPATH , '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2][@data-tab="1"]').send_keys(Keys.SHIFT+Keys.ENTER)
                self.element_presence(By.XPATH, '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2][@data-tab="1"]', 30)
                self.driver.find_element(By.XPATH , '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2][@data-tab="1"]').send_keys(Keys.ENTER)
                time.sleep(1)
                self.element_absence(By.XPATH,'//span[@data-icon="msg-time"]', 100)
                return True
            else:   return False
        except Exception as e:  return e

    def send_attach(self, phone, attachment):
        try:
            if os.path.exists(attachment) == True:
                self.driver.get("https://web.whatsapp.com/send?phone="+format(phone))
                try:    self.driver.switch_to_alert().accept()
                except: pass

                while True:
                    try:
                        self.driver.find_element(By.XPATH , '//div[@title="Attach"]').click()
                        break
                    except: pass
                while True:
                    try:
                        self.driver.find_element(By.XPATH , '//input[@accept="*"]').send_keys(attachment)
                        break
                    except: pass

                while True:
                    try:
                        self.driver.find_element(By.XPATH , '//span[@data-icon="send-light"]').click()
                        break
                    except: pass
                time.sleep(1)
                self.element_absence(By.XPATH,'//span[@data-icon="msg-time"]', 100)
                return True
            else:
                return False
        except Exception as e:  return e
