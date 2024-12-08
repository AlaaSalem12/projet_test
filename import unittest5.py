import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create a screenshots directory if it doesn't exist
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

class SaucedemoCheckoutTest(unittest.TestCase):
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
        self.take_screenshot("after_login_inventory_page")

    def test_complete_checkout_process(self):
        # Add items to cart
        add_to_cart_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Add to cart')]")
        
        # Add first two items to cart
        add_to_cart_buttons[0].click()
        add_to_cart_buttons[1].click()
        
        # Take screenshot after adding items
        self.take_screenshot("items_added_to_cart")
        
        # Open shopping cart
        cart_link = self.driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_link.click()
        
        # Take screenshot of cart page
        self.take_screenshot("cart_page")
        
        # Proceed to checkout
        checkout_button = self.driver.find_element(By.ID, "checkout")
        checkout_button.click()
        
        # Take screenshot of checkout information page
        self.take_screenshot("checkout_info_page")
        
        # Fill out checkout information
        first_name = self.driver.find_element(By.ID, "first-name")
        last_name = self.driver.find_element(By.ID, "last-name")
        postal_code = self.driver.find_element(By.ID, "postal-code")
        
        first_name.send_keys("John")
        last_name.send_keys("Doe")
        postal_code.send_keys("12345")
        
        # Take screenshot after filling out information
        self.take_screenshot("checkout_info_filled")
        
        # Continue to overview
        continue_button = self.driver.find_element(By.ID, "continue")
        continue_button.click()
        
        # Take screenshot of checkout overview
        self.take_screenshot("checkout_overview")
        
        # Verify total price
        total_price_element = self.driver.find_element(By.CLASS_NAME, "total_price")
        total_price = total_price_element.text
        
        # Verify item count
        inventory_items = self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        self.assertEqual(len(inventory_items), 2, "Should have 2 items in checkout")
        
        # Finish checkout
        finish_button = self.driver.find_element(By.ID, "finish")
        finish_button.click()
        
        # Wait for confirmation page
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
        )
        
        # Take screenshot of order complete page
        self.take_screenshot("order_complete")
        
        # Verify completion message
        complete_message = self.driver.find_element(By.CLASS_NAME, "complete-header")
        self.assertEqual(complete_message.text, "Thank you for your order!", "Order completion message should match")

    def tearDown(self):
        # Take a final screenshot before closing the browser
        self.take_screenshot("test_end")
        self.driver.quit()

if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit:
        pass