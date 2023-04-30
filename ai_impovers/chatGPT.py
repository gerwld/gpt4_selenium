from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Start a webdriver instance and open ChatGPT
driver = webdriver.Chrome()
driver.get('https://chatgpt.openai.com/')

# Find the input field and send a question
input_field = driver.find_element_by_class_name('c-text-input')
input_field.send_keys('What is the capital of France?')
input_field.send_keys(Keys.RETURN)

# Wait for ChatGPT to respond
driver.implicitly_wait(10)

# Find the response and save it to a file
response = driver.find_element_by_class_name('c-message__body').text
with open('response.txt', 'w') as f:
    f.write(response)

# Close the webdriver instance
driver.quit()
