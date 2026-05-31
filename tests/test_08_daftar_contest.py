from selenium.webdriver.support.ui import WebDriverWait
from config import BASE_URL, WAIT_TIMEOUT, INVALID_CONTEST_SLUG
from conftest import is_safe_error_page


class TestDaftarContest:

    def test_positive_halaman_contests_tampil(self, driver):
        driver.get(f"{BASE_URL}/contests")
        assert "/contests" in driver.current_url
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            lambda d: "contest" in d.page_source.lower()
        )

    def test_negative_contest_tidak_ada(self, driver):
        driver.get(f"{BASE_URL}/{INVALID_CONTEST_SLUG}")
        assert is_safe_error_page(driver)
