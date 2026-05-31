from config import BASE_URL, VALID_CONTEST_SLUG, INVALID_CONTEST_SLUG, WAIT_TIMEOUT
from selenium.webdriver.support.ui import WebDriverWait
from conftest import is_safe_error_page


class TestDetailContest:

    def test_positive_buka_contest_public(self, driver):
        driver.get(f"{BASE_URL}/{VALID_CONTEST_SLUG}")
        assert "/contests/" in driver.current_url
        WebDriverWait(driver, WAIT_TIMEOUT).until(lambda d: d.title != "")
        assert driver.title != ""

    def test_negative_buka_contest_slug_salah(self, driver):
        driver.get(f"{BASE_URL}/{INVALID_CONTEST_SLUG}")
        assert is_safe_error_page(driver)