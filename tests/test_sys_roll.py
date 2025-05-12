
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


        # Upload Film
        driver.find_element(By.CSS_SELECTOR, "#film-list .add-card").click()
        time.sleep(1)
        driver.find_element(By.ID, "film-name").send_keys("Portra 400")
        driver.find_element(By.ID, "film-brand").send_keys("Kodak")
        driver.find_element(By.ID, "film-iso").send_keys("400")
        driver.find_element(By.ID, "film-format").send_keys("35mm")

        driver.find_element(By.ID, "submit-film").click()
        time.sleep(2)
        self.assertIn("Portra 400", driver.page_source)

        # Go to shooting/rolls page
        driver.get("http://localhost:5002/shooting")
        wait.until(EC.presence_of_element_located((By.ID, "add-roll-btn")))

        # Upload Roll
        driver.find_element(By.ID, "add-roll-btn").click()
        wait.until(EC.element_to_be_clickable((By.ID, "roll-film-select")))
        driver.find_element(By.ID, "roll-film-select").click()
        driver.find_element(By.ID, "roll-film-select").find_elements(By.TAG_NAME, "option")[0].click()

        driver.find_element(By.NAME, "roll_name").send_keys("Test Roll 1")
        
        driver.find_element(By.NAME, "notes").send_keys("First test roll")

        driver.find_element(By.ID, "submit-rolls").click()
        time.sleep(2)
        self.assertIn("Test Roll 1", driver.page_source)

        #Edit Roll
        cards = driver.find_elements(By.CSS_SELECTOR, "#roll-list .gear-card")
        for card in cards:
            if "Test Roll 1" in card.text:
                card.find_element(By.CLASS_NAME, "film-logo-container").click()
                break

        wait.until(EC.element_to_be_clickable((By.ID, "edit-roll-name-use"))).clear()
        driver.find_element(By.ID, "edit-roll-name-use").send_keys("Updated Roll 1")
        driver.find_element(By.ID, "edit-roll-notes-use").clear()
        driver.find_element(By.ID, "edit-roll-notes-use").send_keys("Updated notes")

        driver.find_element(By.CSS_SELECTOR, "#edit-roll-form-use button[type='submit']").click()
        time.sleep(2)
        self.assertIn("Updated Roll 1", driver.page_source)


if __name__ == "__main__":
    unittest.main()
