import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By


class QuillbotHandler:
    continue_xq = '//*[@id="loginContainer"]/div/div[5]/button'
    input_to_iq = "paraphraser-input-box"
    output_to_xq = "//*[@id='output-sentence-box~0']"
    submit_btn_xq = "//*[@id='controlledInputBoxContainer']/div[2]/div/div/div[2]/div/button"
    fluent_btn_xq = "//*[@id='Paraphraser - mode - tab - 1']"
    cookies_btn_iq = "onetrust-accept-btn-handler"
    result_xq = "//*[@id='paraphraser-output-box']"
    close_ad_xq = '//*[@id="max-width-dialog-title"]/button'
    close_ad2_xq = '/html/body/div[4]/div[3]/div/div[1]/button'
    close_ad3_xq = '/html/body/div[6]/div[3]/div/div[1]/button'
    close_ad4_xq = '//*[@class="css-1bvc4cc"]/button'

    def __init__(self, username: str, password: str, headless: bool = True):
        options = uc.ChromeOptions()
        options.add_argument("--incognito")
        options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

        if headless:
            options.add_argument("--headless=new")

        self.browser = uc.Chrome(options=options)
        self.browser.set_page_load_timeout(15)

        self.browser.get('https://quillbot.com/login')

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

    def interact(self, paragraph):
        """Function to get an responce to request"""
        # To avoid popup overflow
        self.avoid_popups()

        # Find input and change it content
        input_to = self.sleepy_find_element(By.ID, self.input_to_iq)
        input_to.clear()
        time.sleep(1)
        input_to.send_keys(paragraph)

        # Click submit
        submit_btn = self.browser.find_element(By.XPATH, self.submit_btn_xq)
        self.avoid_popups()
        submit_btn.click()
        time.sleep(6)

        # Find output and return result
        output_to = self.sleepy_find_element(
            By.XPATH, self.output_to_xq)
        if output_to:
            result = self.sleepy_find_element(By.XPATH, self.result_xq)
            return result.text

    def login(self, username: str, password: str):
        """To enter system"""
        # Find email textbox, enter e-mail
        email_box = self.browser.find_element(By.ID, 'mui-3')
        email_box.send_keys(username)
        time.sleep(1)

        # Find password textbox, enter password
        pass_box = self.sleepy_find_element(By.ID, 'mui-4')
        pass_box.send_keys(password)

        # Click continue
        continue_button = self.sleepy_find_element(By.XPATH, self.continue_xq)
        self.avoid_popups()
        continue_button.click()
        time.sleep(1)

        self.browser.get('https://quillbot.com')

    def avoid_popups(self):
        """To avoid popups"""
        try:
            self.browser.find_elements(By.XPATH, self.fluent_btn_xq)[0].click()
        except:
            pass
        try:
            self.browser.find_elements(By.XPATH, self.close_ad_xq)[0].click()
        except:
            pass

        try:
            self.browser.find_elements(By.ID, 'onetrust-accept-btn-handler')
        except:
            pass

        try:
            self.browser.find_elements(By.XPATH, self.close_ad2_xq)[0].click()
        except:
            pass

        try:
            self.browser.find_elements(By.XPATH, self.close_ad4_xq)[0].click()
        except:
            pass

        try:
            self.browser.find_elements(By.ID, self.cookies_btn_iq)[0].click()
        except:
            pass

        try:
            self.browser.find_elements(By.ID, 'close_ad3_xq')[0].click()
        except:
            pass

        try:
            self.browser.find_elements(
                By.XPATH, '/html/body/div[8]/div[3]/div/div[1]/button')[0].click()
        except:
            pass
        time.sleep(1)

    def quit(self):
        """To quit"""
        self.browser.quit()
        print('Ending quilBot session...')
