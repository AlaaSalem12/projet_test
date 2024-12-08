import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# Create a screenshots directory if it doesn't exist
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

class SaucedemoProductFilterTest(unittest.TestCase):
    def take_screenshot(self, name):
        """
        Take a screenshot and save it with a specific name.
        
        :param name: Name of the screenshot file (without extension)
        """
        screenshot_path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
        self.driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved: {screenshot_path}")

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()  # Maximize window for better screenshots
        self.driver.get("https://www.saucedemo.com/")
        
        # Take screenshot of login page
        self.take_screenshot("login_page")
        
        username = self.driver.find_element(By.ID, "user-name")
        password = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "login-button")
        
        username.send_keys("standard_user")
        password.send_keys("secret_sauce")
        
        # Take screenshot before login
        self.take_screenshot("before_login")
        
        login_button.click()
        
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )
        
        # Take screenshot after successful login
        self.take_screenshot("after_login")

    def test_price_low_to_high_filter(self):
        # Take initial screenshot of product page
        self.take_screenshot("product_page_initial")
        
        # Find and interact with sort dropdown
        sort_dropdown = Select(self.driver.find_element(By.CLASS_NAME, "product_sort_container"))
        
        # Take screenshot before sorting
        self.take_screenshot("before_sorting")
        
        # Select low to high price sorting
        sort_dropdown.select_by_visible_text("Price (low to high)")
        
        # Take screenshot after sorting
        self.take_screenshot("after_sorting")
        
        # Wait for products to be sorted
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item_price"))
        )
        
        # Retrieve and verify price sorting
        prices = self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        price_values = [float(price.text.replace('$', '')) for price in prices]
        
        # Take screenshot of prices
        self.take_screenshot("price_list")
        
        # Assert that prices are sorted from low to high
        self.assertEqual(price_values, sorted(price_values), 
                         "Prices are not sorted from low to high")
        
        # Final screenshot of the sorted page
        self.take_screenshot("product_sorting_final")

    def tearDown(self):
        # Take a final screenshot before closing the browser
        self.take_screenshot("test_end")
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()