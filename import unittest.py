import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

# Create a screenshots directory if it doesn't exist
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

class SaucedemoLoginTest(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.saucedemo.com/")
        self.driver.maximize_window()  # Maximize window for better screenshots

    def take_screenshot(self, name):
        """
        Take a screenshot and save it with a specific name.
        
        :param name: Name of the screenshot file (without extension)
        """
        screenshot_path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
        self.driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved: {screenshot_path}")

    def test_valid_login(self):
        # Take initial screenshot of login page
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
        self.take_screenshot("after_successful_login")
        
        self.assertTrue(self.driver.current_url.endswith("/inventory.html"))

    def test_invalid_login(self):
        # Take initial screenshot of login page
        self.take_screenshot("login_page")

        username = self.driver.find_element(By.ID, "user-name")
        password = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "login-button")

        username.send_keys("locked_out_user")
        password.send_keys("secret_sauce")
        
        # Take screenshot before login attempt
        self.take_screenshot("before_invalid_login")
        
        login_button.click()

        error_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "error-message-container"))
        )
        
        # Take screenshot of error message
        self.take_screenshot("invalid_login_error")
        
        self.assertIn("Epic sadface", error_message.text)

    def tearDown(self):
        # Take a final screenshot before closing the browser
        self.take_screenshot("test_end")
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()