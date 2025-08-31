# imported libraries
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Configure Brave Browser(I use Brave on fedora 42 workstation)
brave_path = "/usr/bin/brave-browser"
chromedriver_path = "/home/mehedihassan/Documents/Mastercourse/chromedriver"

options = Options()
options.binary_location = brave_path
options.add_argument("--start-maximized")  # Remove this to run without opening a new window in the browser

service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

# I created an empty list to keep all of my scraped data
all_data = []

# here I did the most works. Each page had 20 entries and I scraped 60 pages. 
# So in total there are 1200 rows are scraped.
# first I found out the links to the products, then clicked on them, then scraped the data
# then came back and did the same until the page is finished
# I read the selenium python documentation for building this scraper. Link: https://selenium-python.readthedocs.io/
# also I saw the videos of Tech with Tim, a famous youtuber for pyhton. His playlist helped a lot. 
for i in range(60):
    print(f"Scraping page {i+1}/60")
    url_entry = f"https://www.mobiledokan.co/filter/page/{i+1}/?g-type=phones&g-availability=available"
    driver.get(url_entry)
    time.sleep(4)
    
    phone_elements = driver.find_elements(By.CLASS_NAME, "aps-product-title")
    
    for j in range(len(phone_elements)):
        try:
            print(f"Processing phone {j+1}/20 on page {i+1}")
            
            current_phone_elements = driver.find_elements(By.CLASS_NAME, "aps-product-title")
            h2_element = current_phone_elements[j]
            a_tag = h2_element.find_element(By.TAG_NAME, "a")
            driver.execute_script("arguments[0].click();", a_tag)
            time.sleep(4)
            phone_data = {}
            
            phone_data['name'] = driver.find_element(By.CLASS_NAME, "aps-main-title").text
            phone_data['brand'] = driver.find_elements(By.CSS_SELECTOR, "span[itemprop='name']")[1].text
            phone_data['rating'] = driver.find_element(By.CLASS_NAME, "aps-rating-total").text
            phone_data['price'] = driver.find_elements(By.CLASS_NAME, "aps-price-value")[0].text
            
            features = [feature.text for feature in driver.find_elements(By.CLASS_NAME, "aps-feature-vl")]
            
            # Assign features to specific fields (adjust indices based on your page structure)
            phone_data['release_year'] = features[0] if len(features) > 0 else "N/A"
            phone_data['os'] = features[1] if len(features) > 1 else "N/A"
            phone_data['display'] = features[2] if len(features) > 2 else "N/A"
            phone_data['camera'] = features[3] if len(features) > 3 else "N/A"
            phone_data['ram'] = features[4] if len(features) > 4 else "N/A"
            phone_data['battery'] = features[5] if len(features) > 5 else "N/A"
            # page_number & phone_position helped me in being updated 
            # about which page and which phone is being scraped in the moment
            phone_data['page_number'] = i + 1
            phone_data['phone_position'] = j + 1
            
            all_data.append(phone_data)
            print(f"Scraped: {phone_data['name']}")
            
        except Exception as e:
            print(f"Error scraping phone {j+1}: {e}")
        
        driver.back()
        time.sleep(4)
driver.quit()

# Create DataFrame and save to CSV
df = pd.DataFrame(all_data)
df.to_csv('smartphone_data.csv', index=False)
