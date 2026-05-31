import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from config import BASE_URL, WAIT_TIMEOUT, VALID_USERNAME, VALID_PASSWORD
from conftest import wait_for


class TestLoginCredential:

    def test_positive_login_akun_valid(self, driver):
        driver.get(f"{BASE_URL}/login")
        wait_for(driver, By.CSS_SELECTOR, "input[name='username'], input[type='text']").send_keys(VALID_USERNAME)
        driver.find_element(By.CSS_SELECTOR, "input[name='password'], input[type='password']").send_keys(VALID_PASSWORD)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']").click()
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            lambda d: "login" not in d.current_url
        )
        assert "login" not in driver.current_url, "Login gagal, masih di halaman login"

    def test_negative_login_credential_salah(self, driver):
        driver.get(f"{BASE_URL}/login")
        wait_for(driver, By.CSS_SELECTOR, "input[name='username'], input[type='text']").send_keys(VALID_USERNAME)
        driver.find_element(By.CSS_SELECTOR, "input[name='password'], input[type='password']").send_keys("password_salah_123!")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']").click()
        time.sleep(2)
        page = driver.page_source.lower()
        url  = driver.current_url
        login_failed = (
            "login" in url or
            any(kw in page for kw in ["invalid", "incorrect", "salah", "failed", "gagal", "wrong"])
        )
        assert login_failed, "Login dengan credential salah seharusnya gagal"
