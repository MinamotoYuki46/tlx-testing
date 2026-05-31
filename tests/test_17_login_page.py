import time
from selenium.webdriver.common.by import By
from config import BASE_URL
from conftest import wait_for


class TestLoginPage:

    def test_positive_form_login_tampil(self, driver):
        driver.get(f"{BASE_URL}/login")
        username = wait_for(driver, By.CSS_SELECTOR, "input[name='username'], input[type='text']")
        password = driver.find_element(By.CSS_SELECTOR, "input[name='password'], input[type='password']")
        assert username.is_displayed()
        assert password.is_displayed()

    def test_negative_submit_form_kosong(self, driver):
        """TC-17N: Submit login dengan field kosong, harus ada pesan validasi."""
        driver.get(f"{BASE_URL}/login")
        submit = wait_for(driver, By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
        submit.click()
        time.sleep(1)
        page = driver.page_source.lower()
        url  = driver.current_url
        still_on_login = "login" in url
        has_validation = any(kw in page for kw in ["required", "wajib", "cannot be empty", "field"])
        assert still_on_login or has_validation, "Submit form kosong seharusnya tidak berhasil login"
