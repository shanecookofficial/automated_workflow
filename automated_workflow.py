from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import Driver
from dotenv import load_dotenv
import os
import time
import random

load_dotenv()

# Go to tcgplayer.com
driver = Driver(uc=True)
driver.get("https://www.tcgplayer.com/")
driver.maximize_window()

# Click 'Sell With Us' button
sell_with_us_button_locator = "//a/span[contains(text(),'Sell With Us')]"
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, sell_with_us_button_locator)))
driver.find_element(By.XPATH, sell_with_us_button_locator).click()

# Click 'Sign into Your Seller Account' button
sign_into_your_seller_account_button_locator = "//a[contains(text(),'Sign into Your Seller Account')]"
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,sign_into_your_seller_account_button_locator)))
driver.find_element(By.XPATH, sign_into_your_seller_account_button_locator).click()

# Sign in
email_input_locator = "//input[@name='Email']"
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,email_input_locator)))
email = os.getenv('EMAIL')
"""
Individually sending characters at randomized timing helps with being undetected
by web scrapping prevention software.
"""
for i in email:
    time.sleep(random.random())
    driver.find_element(By.XPATH,email_input_locator).send_keys(i)

password_input_locator = "//input[@name='Password']"
password = os.getenv('PASSWORD')
for i in password:
    time.sleep(random.random())
    driver.find_element(By.XPATH,password_input_locator).send_keys(i)

sign_in_button_locator = "//button/span[contains(text(),'Sign In')]"
driver.find_element(By.XPATH, sign_in_button_locator).click()

# Navigate to Orders tab
driver.get("https://store.tcgplayer.com/admin/orders/orderlist")

# Select all 'Ready To Ship' orders
WebDriverWait(driver,10).until(EC.text_to_be_present_in_element((By.XPATH,"//tbody/tr[1]/td[2]"), ''))
ready_to_ship = True
i = 1
while ready_to_ship:
    orderRowLocator = driver.find_element(By.XPATH,f"//tbody/tr[{i}]")
    if "ready-to-ship" in orderRowLocator.get_attribute("class"):
        orderRowCheckboxLocator = driver.find_element(By.XPATH,f"//tbody/tr[{i}]/td/label")
        orderRowCheckboxLocator.click()
        i += 1
    else:
        ready_to_ship = False

driver.quit()