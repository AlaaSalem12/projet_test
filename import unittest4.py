import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

class SauceDemoProductSortTest(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.saucedemo.com/")
        # Login with standard user
        username_field = self.driver.find_element(By.ID, "user-name")
        password_field = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "login-button")
        
        username_field.send_keys("standard_user")
        password_field.send_keys("secret_sauce")
        login_button.click()
        
        # Wait for inventory to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
        )
    
    def test_product_sorting(self):
        """
        Test Case: Verify product sorting functionality
        This test checks if the sorting dropdown works correctly
        """
        # Find the sort dropdown
        sort_dropdown = self.driver.find_element(By.CLASS_NAME, "product_sort_container")
        
        # Sort by Name (A to Z)
        sort_dropdown.find_element(By.XPATH, "//option[@value='az']").click()
        
        # Get product names after A to Z sorting
        product_names_az = [name.text for name in self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
        self.assertEqual(product_names_az, sorted(product_names_az), 
                         "Products are not sorted alphabetically (A to Z)")
        
        # Sort by Name (Z to A)
        sort_dropdown.find_element(By.XPATH, "//option[@value='za']").click()
        product_names_za = [name.text for name in self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
        self.assertEqual(product_names_za, sorted(product_names_za, reverse=True), 
                         "Products are not sorted alphabetically (Z to A)")
        
        # Take screenshot
        self.driver.save_screenshot("product_sorting_test_screenshot.png")
    
    def tearDown(self):
        # Close the browser
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()