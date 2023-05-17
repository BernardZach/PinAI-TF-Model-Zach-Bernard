from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import urllib.request
from progressbar import ProgressBar
import subprocess

# Set the number of times to click the button and the delay between each click
num_clicks = 493
delay_between_clicks = 5  # in seconds
image_loading = 60          #in seconds

options = webdriver.ChromeOptions()
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
options.add_argument('--ignore-certificate-errors')


browser = webdriver.Chrome(options=options)
browser.get('https://www.pintradingdb.com/pinList.php?')


# Define a WebDriverWait object with a timeout of 10 seconds
wait = WebDriverWait(browser, 10)

# Wait for the "Load More" button element to become visible
load_more_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#moreButton')))

subprocess.run(["clear"])
print("\n\n\n\n--Currently Loading WebPage--")

# Create a progress bar object
progress_bar = ProgressBar(max_value=num_clicks)

# Loop through and click the button multiple times with a delay in between
for i in range(num_clicks):
    # Click the "Load More" button
    load_more_button.click()
    
    #Update the progress bar
    progress_bar.update(i)

    # Wait for the specified delay
    time.sleep(delay_between_clicks)


#pause after loading all pages in order to allow all images to laod
progress_bar = ProgressBar(max_value=image_loading)
print("\n\n\n\n--Awaiting Image Loading--")
for i in range(image_loading):
    progress_bar.update(i)
    time.sleep(1)


# Create the 'images' directory if it doesn't exist
if not os.path.exists('images'):
    os.mkdir('images')

# Find all the image elements on the page
image_elements = browser.find_elements(by='tag name', value='img')

print("\n\n\n\n--Currently Loading Images--")

# Create a progress bar object
progress_bar = ProgressBar(max_value=len(image_elements))

startIndex = 30445      #use in the case the initial image downloads did not complete

# Loop through the image elements and save each image to a file
for i, image_element in enumerate(image_elements):
    # Get the source URL and filename of the image
    image_url = image_element.get_attribute('src')
    filename = image_element.get_attribute('title')

    # Replace any invalid characters in the filename
    filename = filename.replace('/', '-').replace('\\', '-').replace(':', '-').replace('*', '-').replace('?', '-').replace('"', '').replace('<', '').replace('>', '').replace('|', '').replace('\t', '_')

    # Generate a unique filename for the image
    filename = f'{i+1:03d} - {filename}.jpg'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

    # Save the image to a file in the 'images' folder
    req = urllib.request.Request(image_url, headers=headers)
    response = urllib.request.urlopen(req)
    data = response.read()

    with open(os.path.join('images', filename), 'wb') as f:
        f.write(data)

    # Update the progress bar
    progress_bar.update(i)

    # Add a delay between each image download
    time.sleep(.1)

startIndex = input("Did all the images get sucessfully scraped? if so type Y. if not type the last image that was successfully saved.\n")

while startIndex != "Y":
    if not isinstance(startIndex, int):
        print("Invalid Input recieved.")
    
    else:
        # Loop through the image elements and save each image to a file
        for i, image_element in enumerate(image_elements[startIndex:], startIndex):

            # Get the source URL and filename of the image
            image_url = image_element.get_attribute('src')
            filename = image_element.get_attribute('title')

            # Replace any invalid characters in the filename
            filename = filename.replace('/', '-').replace('\\', '-').replace(':', '-').replace('*', '-').replace('?', '-').replace('"', '').replace('<', '').replace('>', '').replace('|', '').replace('\t', '_')

            # Generate a unique filename for the image
            filename = f'{i+1:03d} - {filename}.jpg'

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

            # Save the image to a file in the 'images' folder
            req = urllib.request.Request(image_url, headers=headers)
            response = urllib.request.urlopen(req)
            data = response.read()

            with open(os.path.join('images', filename), 'wb') as f:
                f.write(data)

            # Update the progress bar
            progress_bar.update(i)

            # Add a delay between each image download
            time.sleep(.1)

    startIndex = input("Did all the images get sucessfully scraped? if so type Y. if not type the last image that was successfully saved.\n")

browser.quit()