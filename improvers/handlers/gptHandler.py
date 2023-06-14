"""Хандлить запити на chat.openai.io"""
import sys
import time
import random
import pyperclip as pc
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions as Exceptions
from global_context import C_GREEN, C_RED


class ChatGPTHandler:
    login_xq = '//button[//div[text()="Log in"]]'
    continue_xq = '//button[text()="Continue"]'
    stop_xq = '//button[text()="Stop generating"]'

    next_cq = "prose"
    button_tq = "button"
    done_xq = '//button[//div[text()="Done"]]'
    chatbox_cq = "text-base"
    wait_cq = "text-2xl"
    reset_xq = '//a[text()="New chat"]'
    continue_gen_xq = (
        '//*[@id="__next"]/div[2]/div[2]/div/main/div[3]/form/div/div[1]/div/button[2]'
    )
    gpt4_btn_xq = '//*[@id="__next"]/div[2]/div[2]/div/main/div[2]/div/div/div[1]/div/div/ul/li[2]/button'
    gpt_version_div = (
        "/html/body/div[1]/div[2]/div[2]/div/main/div[2]/div/div/div/div[1]"
    )

    def __init__(
        self,
        username: str,
        password: str,
        headless: bool = False,
        cold_start: bool = False,
        gpt4=False,
        should_start_with=False,
    ):
        self.gpt4 = gpt4
        self.should_start_with = should_start_with
        options = uc.ChromeOptions()
        options.add_argument("--incognito")

        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--blink-settings=imagesEnabled=false")

        self.browser = uc.Chrome(options=options)
        self.browser.set_page_load_timeout(15)

        self.browser.get("https://chat.openai.com/auth/login?next=/chat")
        if not cold_start:
            self.pass_verification()
            self.login(username, password)

    def pass_verification(self):
        while self.check_login_page():
            verify_button = self.browser.find_elements(
                By.ID, "challenge-stage")
            if len(verify_button):
                try:
                    verify_button[0].click()
                except Exceptions.ElementNotInteractableException:
                    pass
            time.sleep(1)
        return

    def check_login_page(self):
        login_button = self.browser.find_elements(By.XPATH, self.login_xq)
        return len(login_button) == 0

    def login(self, username: str, password: str):
        """To enter system"""

        # Find login button, click it
        login_button = self.sleepy_find_element(By.XPATH, self.login_xq)
        login_button.click()
        time.sleep(1)

        # Find email textbox, enter e-mail
        email_box = self.sleepy_find_element(By.ID, "username")
        email_box.send_keys(username)

        # Click continue
        continue_button = self.sleepy_find_element(By.XPATH, self.continue_xq)
        continue_button.click()
        time.sleep(1)

        # Find password textbox, enter password
        pass_box = self.sleepy_find_element(By.ID, "password")
        if type(pass_box) == list and len(pass_box):
            pass_box[0].send_keys(password)
        else:
            pass_box.send_keys(password)
        # Click continue
        continue_button = self.sleepy_find_element(By.XPATH, self.continue_xq)
        continue_button.click()
        time.sleep(3)

        # Pass introduction
        next_button = self.browser.find_element(By.CLASS_NAME, self.next_cq)
        next_button = next_button.find_elements(By.TAG_NAME, self.button_tq)[0]
        next_button.click()
        time.sleep(1)
        next_button = self.browser.find_element(By.CLASS_NAME, self.next_cq)
        next_button = next_button.find_elements(By.TAG_NAME, self.button_tq)[1]
        next_button.click()
        time.sleep(1)
        next_button = self.browser.find_element(By.CLASS_NAME, self.next_cq)
        done_button = next_button.find_elements(By.TAG_NAME, self.button_tq)[1]
        done_button.click()

    def sleepy_find_element(
        self, by, query, attempt_count: int = 30, sleep_duration: int = 1
    ):
        """If the loading time is a concern, this function helps"""
        for _ in range(attempt_count):
            item = self.browser.find_elements(by, query)
            if len(item) > 0:
                item = item[0]
                break
            time.sleep(sleep_duration)
        return item

    def wait_to_disappear(self, by, query, sleep_duration=1):
        """Wait until the item disappear, then return"""
        while True:
            thinking = self.browser.find_elements(by, query)
            if len(thinking) == 0:
                break
            time.sleep(sleep_duration)
        return

    def interact(self, question: str, isForced=False):
        """Function to get an answer for a question"""

        # Set GPT-4 if enabled.
        if self.gpt4 and not question == "keep going":
            time.sleep(1)
            print("-" * 90 + "\nGPT-4 Version Enabled.\n" + "-" * 90)
            btn_set_gpt4 = self.sleepy_find_element(By.XPATH, self.gpt4_btn_xq)

            while not btn_set_gpt4:
                time.sleep(0.5)
                btn_set_gpt4 = self.sleepy_find_element(
                    By.XPATH, self.gpt4_btn_xq)
                print("Try to find btn gpt-4", btn_set_gpt4)

            btn_set_gpt4.click()
            time.sleep(0.2)
            btn_set_gpt4.click()
            time.sleep(0.2)
            btn_set_gpt4.click()
            time.sleep(0.5)

            gpt_version = self.sleepy_find_element(
                By.XPATH, self.gpt_version_div)
            if gpt_version and gpt_version.text and "GPT-4" in gpt_version.text:
                print(f"{C_GREEN}Finded GPT-4 btn.{C_GREEN.OFF}")
            else:
                print(f"{C_RED}Not a GPT-4. Skipping...{C_RED.OFF}")
                return "not a GPT-4"

                # перевірка на запит keep going, якщо є кнопка Continue generating генерни продовження, інакше скіп
        if question == "keep going" and not isForced:
            return self.continue_generating()

        else:
            text_area = self.sleepy_find_element(
                By.TAG_NAME, "textarea", 40, 1)
            # оновлена версія для швидшого вставлення question в text_area
            print(
                "-" * 90 +
                f"\n{C_GREEN}Request:{C_GREEN.OFF} {question}\n" + "-" * 90
            )
            pc.copy(question.strip())
            cmd_ctrl = Keys.COMMAND if sys.platform == "darwin" else Keys.CONTROL
            text_area.send_keys(cmd_ctrl + "v м")
            # фікс кириллиці
            if text_area.get_attribute("value").endswith("м"):
                text_area.send_keys(Keys.BACKSPACE)
            text_area.send_keys(Keys.RETURN)

            # перевірка на should_start_with
            if (self.should_start_with) and question != "keep going":
                time.sleep(2)
                still_generating = self.browser.find_elements(
                    By.CLASS_NAME, self.wait_cq
                )
                if still_generating and len(still_generating):
                    check_answer = self.browser.find_elements(
                        By.CLASS_NAME, self.chatbox_cq
                    )[-1]
                    # перевірка на ліміт в реалтаймі
                    self.check_limit_timeout(response=check_answer.text)
                    stripped = "".join(check_answer.text.strip().split(" "))
                    if (
                        len(check_answer.text.strip()) > 4
                        and not stripped.startswith(self.should_start_with)
                        or not stripped.startswith(
                            "html\nCopy code" + self.should_start_with
                        )
                        or not stripped.startswith(
                            "html\nCopy code\n" + self.should_start_with
                        )
                    ):
                        print(
                            f"{C_RED}should_start_with exeption...{C_RED.OFF}\n{check_answer.text}"
                        )
                        # Click stop
                        stop_button = self.browser.find_elements(
                            By.XPATH, self.stop_xq)
                        if len(stop_button):
                            stop_button[0].click()
                        return ""

            self.wait_to_disappear(By.CLASS_NAME, self.wait_cq)
            answer = self.browser.find_elements(
                By.CLASS_NAME, self.chatbox_cq)[-1]

            # перевірка на ліміт по відповіді і повернення якщо ні
            self.check_limit_timeout(response=answer.text)
            return answer.text

    def continue_generating(self):
        # пошук кнопки keep generating, якщо найдеш за 30 спроб - натисни, інакше форс ітерактшн з текстовим keep going
        btn_continue_gen = self.sleepy_find_element(
            By.XPATH, self.continue_gen_xq, 30, 0.3
        )
        if btn_continue_gen:
            btn_continue_gen.click()
            try:
                btn_continue_gen.click()
                time.sleep(1)
                btn_continue_gen.click()
            except:
                pass

            print(f"{C_RED}Continue generating click{C_RED.OFF}")
            fin_answer = self.get_last_generated()
            # перевірка на ліміт по відповіді і повернення якщо ні
            if fin_answer:
                self.check_limit_timeout(response=fin_answer)
                return fin_answer if fin_answer else " "
            else:
                return " "

        # перевірка чи генерує, якщо ні і закінчується на артікл - повернути, інакше в залежності від того чи є кнопка
        else:
            fin_answer = self.get_last_generated()
            btn_continue_gen = self.sleepy_find_element(
                By.XPATH, self.continue_gen_xq, 30, 0.3
            )
            if fin_answer.strip().endswith("</article>"):
                return fin_answer
            elif not btn_continue_gen:
                self.interact("keep going", isForced=True)
                print(f"{C_RED}Forced keep going{C_RED.OFF}")
            elif btn_continue_gen:
                self.continue_generating()

    def quit(self):
        self.browser.quit()
        return

    def get_last_generated(self):
        DELAY_FIRST_GENERATION = 4
        DELAY_BETWEEN_CHECKS = 4
        # Затримка в 4 сек, далі перевірка чи новий стемп відповідний старому з затримкою в 4 сек. Якщо рівні - повернення відповіді.
        isAnswerNotEqual = True
        answer = ""
        time.sleep(DELAY_FIRST_GENERATION)
        while isAnswerNotEqual:
            ans_block = self.browser.find_elements(
                By.CLASS_NAME, self.chatbox_cq)[-1]
            newAnswer = ans_block.text
            if newAnswer and newAnswer.strip().lower().endswith("</article>"):
                return newAnswer
            elif newAnswer and not answer == newAnswer:
                answer = newAnswer
            elif newAnswer:
                isAnswerNotEqual = False
            time.sleep(DELAY_BETWEEN_CHECKS)
        self.wait_to_disappear(By.CLASS_NAME, self.wait_cq)
        return self.browser.find_elements(By.CLASS_NAME, self.chatbox_cq)[-1].text

    def reset_thread(self):
        """the conversation is refreshed"""
        self.browser.find_element(By.XPATH, self.reset_xq).click()

    def check_limit_timeout(self, response: str):
        if (
            self.gpt4 == True
            and "You've reached the current usage cap for GPT-4" in response.strip()
        ):
            print(
                f"{C_RED}ChatGPT-4 limit reached. Setting sleep to 1 hour...{C_RED.OFF}"
            )
            time.sleep(3600)
        if (
            "".join(response.strip().split(" ")).lower().startswith("!")
            and "reached our limit of messages per 24 hours." in response.strip()
        ):
            requests_delay = random.randint(2, 16)
            print(
                f"{C_RED}ChatGPT 24h limit reached. Setting sleep to 1h {requests_delay} minutes...{C_RED.OFF}"
            )
            time.sleep(3600 + (requests_delay * 60))
        if (
            "".join(response.strip().split(" ")).lower().startswith("!")
            and "limit reached" in response.strip()
        ):
            requests_delay = random.randint(8, 20)
            print(
                f"{C_RED}ChatGPT limit reached. Setting sleep to {requests_delay} minutes...{C_RED.OFF}"
            )
            time.sleep(requests_delay * 60)
        if (
            "".join(response.strip().split(" ")).lower().startswith("!")
            and "ne minute." in response.strip().lower()
        ):
            print(f"{C_RED}ne minute....{C_RED.OFF}")
            return ""
        if (
            "".join(response.strip().split(" ")).lower().startswith("!")
            and "Only one message at a time" in response.strip().lower()
        ):
            print(f"{C_RED}at a time....{C_RED.OFF}")
            return " "
