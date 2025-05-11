
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

class GearUploadAndEditSystemTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')
        cls.app.config['WTF_CSRF_ENABLED'] = False
        cls.app.config['LIVESERVER_PORT'] = 5003

        def run_flask():
            cls.app.run(port=5003, debug=False, use_reloader=False)

        cls.server_thread = threading.Thread(target=run_flask)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(2)

        with cls.app.app_context():
            db.create_all()

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_upload_and_edit_camera(self):
        driver = self.driver

        # 注册
        driver.get("http://localhost:5003/")
        driver.find_element(By.LINK_TEXT, "Sign Up").click()
        time.sleep(1)
        driver.find_element(By.NAME, "username").send_keys("testuser")
        driver.find_element(By.NAME, "password").send_keys("password")
        checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
        checkboxes[0].click()
        checkboxes[1].click()
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(1)

        # 登录
        driver.find_element(By.NAME, "username").send_keys("testuser")
        driver.find_element(By.NAME, "password").send_keys("password")
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(1)

        # 进入 gear 页面
        driver.get("http://localhost:5003/gear")
        time.sleep(1)

        # 上传相机
        driver.find_element(By.CSS_SELECTOR, "#camera-list .add-card").click()
        time.sleep(1)
        driver.find_element(By.NAME, "name").send_keys("M6")
        driver.find_element(By.NAME, "brand").send_keys("Leica")
        driver.find_element(By.NAME, "type").send_keys("Rangefinder")
        driver.find_element(By.NAME, "format").send_keys("35mm")
        driver.find_element(By.NAME, "is_public").click()
        driver.find_element(By.ID, "submit").click()
        time.sleep(2)
        self.assertIn("M6", driver.page_source)

        # 编辑相机（点击卡片弹窗 → 修改品牌 → 保存）
        camera_cards = driver.find_elements(By.CSS_SELECTOR, "#camera-list .gear-card")
        for card in camera_cards:
            if "M6" in card.text:
                card.click()
                break

        time.sleep(1)
        brand_field = driver.find_element(By.ID, "edit-brand")
        brand_field.clear()
        brand_field.send_keys("Updated Leica")
        driver.find_element(By.CSS_SELECTOR, "#camera-edit-form button[type='submit']").click()
        time.sleep(2)
        self.assertIn("Updated Leica", driver.page_source)

if __name__ == "__main__":
    unittest.main()
