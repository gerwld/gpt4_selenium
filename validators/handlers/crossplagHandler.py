import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By


class CrossplagHandler:
    signin_btn_xq = '//button[text()=" Sign In "]'
    input_to_iq = "/html/body/app-root/app-navbar/section/app-text-detector/main/div[2]/div[1]/textarea"
    submit_btn_xq = "/html/body/app-root/app-navbar/section/app-text-detector/main/div[2]/div[1]/div/button"

    def __init__(self, username: str, password: str, headless: bool = False):
        options = uc.ChromeOptions()
        options.add_argument("--incognito")
        options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

        if headless:
            options.add_argument("--headless=new")

        self.browser = uc.Chrome(options=options)
        self.browser.set_page_load_timeout(15)

        self.browser.get('https://app.crossplag.com/login')

        self.login(username, password)

    def sleepy_find_element(self, by, query, attempt_count: int = 20, sleep_duration: int = 1):
        """If the loading time is a concern, this function helps"""
        for _ in range(attempt_count):
            item = self.browser.find_elements(by, query)
            if len(item) > 0:
                item = item[0]
                break
            time.sleep(sleep_duration)
        return item

    def interact(self, post):
        """Function to get an responce to request"""
        # Find input and change it content
        input_to = self.sleepy_find_element(By.XPATH, self.input_to_iq)
        input_to.clear()
        time.sleep(1)
        input_to.send_keys(post)

        # Click submit
        submit_btn = self.browser.find_element(By.XPATH, self.submit_btn_xq)
        submit_btn.click()

        # Find answer on loader dissapear and return it
        self.wait_to_disappear(By.CLASS_NAME, 'processing')
        answer = self.sleepy_find_element(
            By.XPATH, '/html/body/app-root/app-navbar/section/app-text-detector/main/div[2]/div[2]/div/div[1]/div[1]/div/span')

        # Return result or 101, depends of does answer contain % in it
        return int(answer.text.split('%')[0]) if '%' in answer.text else 101

    def login(self, username: str, password: str):
        """To enter system"""
        # Find email textbox, enter e-mail
        email_box = self.browser.find_elements(
            By.XPATH, "//input[@type='email']")
        email_box[0].send_keys(username)

        # Find password textbox, enter password
        pass_box = self.browser.find_elements(
            By.XPATH,  "//input[@type='password']")
        pass_box[0].send_keys(password)

        # Click continue
        continue_button = self.sleepy_find_element(
            By.XPATH, self.signin_btn_xq)
        continue_button.click()
        time.sleep(2)

        self.browser.get('https://app.crossplag.com/individual/detector')

    def wait_to_disappear(self, by, query, sleep_duration=1):
        """Wait until the item disappear, then return"""
        while True:
            thinking = self.browser.find_elements(by, query)
            if len(thinking) == 0:
                break
            time.sleep(sleep_duration)
        return

    def quit(self):
        """To quit"""
        self.browser.quit()
        print('Ending quilBot session...')
