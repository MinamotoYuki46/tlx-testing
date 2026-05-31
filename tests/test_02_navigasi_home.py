from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from config import BASE_URL, WAIT_TIMEOUT
from conftest import wait_for, is_safe_error_page


class TestNavigasiHome:

    def test_positive_logo_kembali_ke_home(self, driver):
        driver.get(f"{BASE_URL}/problems")
        logo = wait_for(driver, By.CSS_SELECTOR, "a[href='/']")
        logo.click()
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            lambda d: d.current_url.rstrip("/") == BASE_URL.rstrip("/")
        )
        assert driver.current_url.rstrip("/") == BASE_URL.rstrip("/")

    def test_negative_route_typo_aman(self, driver):
        driver.get(f"{BASE_URL}/homee")
        assert is_safe_error_page(driver)
