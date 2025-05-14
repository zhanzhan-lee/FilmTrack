
import time
import threading
import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GearUploadAndEditSystemTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')
        cls.app.config['WTF_CSRF_ENABLED'] = False
        cls.app.config['LIVESERVER_PORT'] = 5002

        def run_flask():
            cls.app.run(port=5002, debug=False, use_reloader=False)

        cls.server_thread = threading.Thread(target=run_flask)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(2)

        with cls.app.app_context():
            db.create_all()

        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_upload_and_edit_gear(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        # Register
        driver.get("http://localhost:5002/")
        driver.find_element(By.LINK_TEXT, "Sign Up").click()
        time.sleep(1)
        driver.find_element(By.NAME, "username").send_keys("testuser")
        driver.find_element(By.NAME, "password").send_keys("password")
        driver.find_element(By.NAME, "confirm_password").send_keys("password")
        checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
        checkboxes[0].click()
        checkboxes[1].click()
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(1)

        # Login
        driver.find_element(By.NAME, "username").send_keys("testuser")
        driver.find_element(By.NAME, "password").send_keys("password")
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(1)

        # gear page
        driver.get("http://localhost:5002/")
        time.sleep(1)
        driver.get("http://localhost:5002/gear")
        time.sleep(1)

        # Upload Lens
        driver.find_element(By.CSS_SELECTOR, "#lens-list .add-card").click()
        time.sleep(1)
        driver.find_element(By.ID, "lens-name").send_keys("Planar 50mm")
        driver.find_element(By.ID, "lens-brand").send_keys("Zeiss")
        driver.find_element(By.ID, "lens-mount-type").send_keys("M")
        driver.find_element(By.ID, "submit-lens").click()
        time.sleep(2)
        self.assertIn("Planar 50mm", driver.page_source)

        # Edit Lens
        lens_cards = driver.find_elements(By.CSS_SELECTOR, "#lens-list .gear-card")
        for card in lens_cards:
            if "Planar 50mm" in card.text:
                card.click()
                break

        time.sleep(1)
        brand_field = driver.find_element(By.ID, "edit-lens-brand")
        brand_field.clear()
        brand_field.send_keys("Updated Zeiss")
        driver.find_element(By.CSS_SELECTOR, "#lens-edit-form button[type='submit']").click()
        time.sleep(2)
        self.assertIn("Updated Zeiss", driver.page_source)



if __name__ == "__main__":
    unittest.main()
