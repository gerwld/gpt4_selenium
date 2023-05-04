from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService

import os
import time

# Ініціалізація сервісу, опшинів хедлес бравзеру
chromedriver = '/usr/local/bin/chromedriver'
options = webdriver.ChromeOptions()
options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
# options.add_argument('headless')  # для открытия headless-браузера
service = ChromeService(executable_path=chromedriver)
driver = webdriver.Chrome(service=service, options=options)


driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[0])
driver.get("http://www.quillbot.com")

wait = WebDriverWait(driver, 80, poll_frequency=1,
                     ignored_exceptions=[NoSuchElementException,
                                         ElementNotVisibleException,
                                         ElementNotSelectableException])

accept_cookies_btn = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
print("accept_cookies_btn clicked")


fluent_btn = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id='Paraphraser - mode - tab - 1']"))).click()
print("Fluent clicked")


while True:
    input_to = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "paraphraser-input-box"))).clear()
    print("input_to cleared")

    input_to = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "paraphraser-input-box"))).send_keys("One of the important data structures in Bash, the most popular shell in Linux, is the associative array. This type \
                                                                                of array enables you to store key-value pairs. In this article, we will explain how associative arrays work in Bash \
                                                                                and how to use them effectively.")

    # нажимає на баттон з делаєм
    time.sleep(1)
    driver.find_element(
        By.XPATH, "//*[@id='controlledInputBoxContainer']/div[2]/div/div/div[2]/div/button").click()
    print("input_to sended")

    # driver.switch_to.window(driver.window_handles[0])

    Element = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//*[@id='output-sentence-box~0']")))
    time.sleep(8)

    quilled = driver.find_element(
        By.XPATH, "//*[@id='paraphraser-output-box']")
    print('text:', quilled.text)
    time.sleep(4)
