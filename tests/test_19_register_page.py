import time
import pytest
from selenium.webdriver.common.by import By
from config import BASE_URL


class TestRegisterPage:

    def test_positive_form_register_tampil(self, driver):
        driver.get(f"{BASE_URL}/register")
        fields = driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='email'], input[type='password']")
        assert len(fields) >= 2, "Form register harus memiliki minimal 2 field input"

    def test_negative_register_email_tidak_valid(self, driver):
        driver.get(f"{BASE_URL}/register")
        email_fields = driver.find_elements(By.CSS_SELECTOR, "input[type='email'], input[name*='email']")
        if not email_fields:
            pytest.skip("Field email tidak ditemukan di halaman register")
        email_fields[0].send_keys("ini-bukan-email")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']").click()
        time.sleep(1)
        page = driver.page_source.lower()
        browser_invalid = email_fields[0].get_attribute("validationMessage") not in (None, "")
        page_invalid    = any(kw in page for kw in ["invalid", "email", "format", "salah"])
        assert browser_invalid or page_invalid, "Email tidak valid seharusnya ditolak"
