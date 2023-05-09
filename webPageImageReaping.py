from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set the number of times to click the button and the delay between each click
num_clicks = 493
delay_between_clicks = 5  # in seconds

# Initialize a new Chrome browser instance
browser = webdriver.Chrome()

# Navigate to the website you want to interact with
browser.get('https://www.pintradingdb.com/pinList.php?')

# Define a WebDriverWait object with a timeout of 10 seconds
wait = WebDriverWait(browser, 10)

# Wait for the "Load More" button element to become visible
load_more_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#moreButton')))

# Loop through and click the button multiple times with a delay in between
for i in range(num_clicks):
    # Click the "Load More" button
    load_more_button.click()
    
    # Wait for the specified delay
    time.sleep(delay_between_clicks)

# Close the browser when done
browser.quit()
