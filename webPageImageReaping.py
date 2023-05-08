from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Set the number of times to press Enter and the delay between each press
num_presses = 5
delay_between_presses = 1  # in seconds

# Initialize a new Chrome browser instance
browser = webdriver.Chrome()

# Navigate to the website you want to interact with
browser.get('https://www.example.com')

# Loop through and press Enter multiple times with a delay in between
for i in range(num_presses):
    # Press the Enter key
    elem = browser.find_element_by_tag_name('body')
    elem.send_keys(Keys.RETURN)
    
    # Wait for the specified delay
    time.sleep(delay_between_presses)

# Close the browser when done
browser.quit()