import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create a screenshots directory if it doesn't exist
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

class SaucedemoShoppingCartTest(unittest.TestCase):
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

    def test_add_remove_items(self):
        # Take initial screenshot of product page
        self.take_screenshot("product_page_initial")
        
        # Find add to cart buttons
        add_to_cart_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Add to cart')]")
        
        # Add first two items to cart
        add_to_cart_buttons[0].click()
        self.take_screenshot("after_first_item_added")
        
        add_to_cart_buttons[1].click()
        self.take_screenshot("after_second_item_added")
        
        # Verify cart badge shows correct number of items
        cart_badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        self.assertEqual(cart_badge.text, "2", "Cart badge should show 2 items")
        
        # Take screenshot of cart badge
        self.take_screenshot("cart_badge_with_two_items")
        
        # Open shopping cart
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        
        # Take screenshot of cart page
        self.take_screenshot("cart_page_with_two_items")
        
        # Find and click remove button for first item
        remove_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Remove')]")
        remove_buttons[0].click()
        
        # Take screenshot after removing an item
        self.take_screenshot("cart_page_after_removing_item")
        
        # Verify only one item remains in cart
        cart_items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
        self.assertEqual(len(cart_items), 1, "Only one item should remain in the cart")
        
        # Final screenshot of cart
        self.take_screenshot("cart_page_final")

    def tearDown(self):
        # Take a final screenshot before closing the browser
        self.take_screenshot("test_end")
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()