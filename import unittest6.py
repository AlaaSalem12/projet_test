import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SaucedemoResetTest(unittest.TestCase):
    def setUp(self):
        # Create a screenshots directory if it doesn't exist
        self.screenshot_dir = 'screenshots'
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
        
        # Setup Chrome WebDriver
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.saucedemo.com/")
        
        # Take initial screenshot
        self._take_screenshot('initial_page')

    def _take_screenshot(self, name):
        """
        Take a screenshot and save it with a unique name
        
        :param name: Base name for the screenshot file
        """
        try:
            screenshot_path = os.path.join(self.screenshot_dir, f'{name}_screenshot.png')
            self.driver.save_screenshot(screenshot_path)
            print(f'Screenshot saved: {screenshot_path}')
        except Exception as e:
            print(f'Failed to take screenshot: {e}')

    def test_reset_functionality(self):
        # Login with standard user
        username = self.driver.find_element(By.ID, "user-name")
        password = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "login-button")
        username.send_keys("standard_user")
        password.send_keys("secret_sauce")
        login_button.click()
        
        # Take screenshot after login
        self._take_screenshot('after_login')

        # Wait for the inventory page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )

        # Add an item to the cart
        add_to_cart_button = self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
        add_to_cart_button.click()
        
        # Take screenshot after adding item to cart
        self._take_screenshot('after_add_to_cart')

        # Verify the cart badge shows 1 item
        cart_badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        self.assertEqual(cart_badge.text, "1")

        # Open the sidebar menu
        menu_button = self.driver.find_element(By.ID, "react-burger-menu-btn")
        menu_button.click()
        
        # Take screenshot of opened sidebar
        self._take_screenshot('sidebar_opened')

        # Wait for reset button to be clickable
        reset_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "reset_sidebar_link"))
        )
        reset_button.click()
        
        # Take screenshot after reset
        self._take_screenshot('after_reset')

        # Verify the cart badge is no longer displayed
        cart_badge_displayed = self.driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        self.assertEqual(len(cart_badge_displayed), 0, "Cart badge should not be displayed after reset")

    def tearDown(self):
        # Take a final screenshot before closing the browser
        self._take_screenshot('test_completed')
        self.driver.quit()

if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit:
        pass