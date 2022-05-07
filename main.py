from selenium import webdriver
from datetime import date
import os
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

today = str(date.today().strftime('%Y-%m-%d'))
url = f"https://api.composer.nprstations.org/v1/widget/50ef24ebe1c8a1369593d032/day?date={today}&format=html&hide_amazon=false&hide_itunes=false&hide_arkiv=false"

driver.get(url)
print(driver.page_source)
print("Finished!")