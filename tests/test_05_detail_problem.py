from config import BASE_URL, VALID_PROBLEM_SLUG, INVALID_PROBLEM_SLUG, WAIT_TIMEOUT
from selenium.webdriver.support.ui import WebDriverWait
from conftest import is_safe_error_page


class TestDetailProblem:

    def test_positive_buka_problem_valid(self, driver):
        driver.get(f"{BASE_URL}/{VALID_PROBLEM_SLUG}")
        assert "/problems/" in driver.current_url
        WebDriverWait(driver, WAIT_TIMEOUT).until(lambda d: d.title != "")
        assert driver.title != ""

    def test_negative_buka_problem_slug_invalid(self, driver):
        driver.get(f"{BASE_URL}/{INVALID_PROBLEM_SLUG}")
        assert is_safe_error_page(driver)