import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By


class QuillbotHandler:
    input_to_iq = "paraphraser-input-box"
    output_to_xq = "//*[@id='output-sentence-box~0']"
    submit_btn_xq = "//*[@id='controlledInputBoxContainer']/div[2]/div/div/div[2]/div/button"
    fluent_btn_xq = "//*[@id='Paraphraser - mode - tab - 1']"
    cookies_btn_iq = "onetrust-accept-btn-handler"
    result_xq = "//*[@id='paraphraser-output-box']"

    def __init__(self, headless: bool = False):
        options = uc.ChromeOptions()
        options.add_argument("--incognito")
        options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

        if headless:
            options.add_argument("--headless=new")

        self.browser = uc.Chrome(options=options)
        self.browser.set_page_load_timeout(15)

        self.browser.get("http://www.quillbot.com")

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
        accept_cookies_btn = self.browser.find_elements(
            By.ID, self.cookies_btn_iq)
        try:
            accept_cookies_btn[0].click()
        except:
            print('No accept cookies button found.')

        fluent_btn = self.sleepy_find_element(By.XPATH, self.fluent_btn_xq)
        fluent_btn.click()

        input_to = self.sleepy_find_element(By.ID, self.input_to_iq)
        input_to.clear()
        input_to.send_keys(paragraph)

        time.sleep(1)
        submit_btn = self.browser.find_element(By.XPATH, self.submit_btn_xq)
        submit_btn.click()

        output_to = self.sleepy_find_element(
            By.XPATH, self.output_to_xq)
        time.sleep(8)

        if output_to:
            result = self.sleepy_find_element(By.XPATH, self.result_xq)
            return result.text
