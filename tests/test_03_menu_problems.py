from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import BASE_URL, WAIT_TIMEOUT
from conftest import wait_for, is_safe_error_page


class TestMenuProblems:

    def test_positive_halaman_problems_tampil(self, driver):
        driver.get(BASE_URL)
        menu = wait_for(driver, By.XPATH, "//a[contains(@href, '/problems')]")
        menu.click()
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.url_contains("/problems"))
        assert "/problems" in driver.current_url

    def test_negative_route_problem_invalid(self, driver):
        driver.get(f"{BASE_URL}/problems-halaman-salah")
        assert is_safe_error_page(driver)
