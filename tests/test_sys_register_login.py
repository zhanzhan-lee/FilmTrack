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

class SystemRegisterLoginTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')
        cls.app.config['WTF_CSRF_ENABLED'] = False
        cls.app.config['LIVESERVER_PORT'] = 5001

        def run_flask():
            cls.app.run(port=5001, debug=False, use_reloader=False)

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

    def test_register_and_login_flow(self):
        driver = self.driver

        # 1. 打开首页，点击 Sign Up
        driver.get("http://localhost:5001/")
        driver.find_element(By.LINK_TEXT, "Sign Up").click()
        time.sleep(1)

        # 2. 填写注册表单
        driver.find_element(By.NAME, "username").send_keys("testuser")
        driver.find_element(By.NAME, "password").send_keys("password")
        checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
        checkboxes[0].click()
        checkboxes[1].click()
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(1)

        # ✅ 现在已经跳转到了 login 页面，无需点击 “Sign in”
        driver.find_element(By.NAME, "username").send_keys("testuser")
        driver.find_element(By.NAME, "password").send_keys("password")
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(1)

        # 4. 验证已成功登录并进入 Gear 页
        driver.get("http://localhost:5001/gear")
        time.sleep(1)
        self.assertIn("Upload Camera", driver.page_source)  # or check .add-card presence


if __name__ == "__main__":
    unittest.main()
