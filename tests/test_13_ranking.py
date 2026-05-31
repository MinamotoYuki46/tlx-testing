from config import BASE_URL, WAIT_TIMEOUT
from selenium.webdriver.support.ui import WebDriverWait
from conftest import is_safe_error_page


class TestRanking:

    def test_positive_halaman_ranking_tampil(self, driver):
        driver.get(f"{BASE_URL}/ranking")
        assert "/ranking" in driver.current_url
        WebDriverWait(driver, WAIT_TIMEOUT).until(lambda d: d.title != "")
        assert driver.title != ""

    def test_negative_route_ranking_invalid(self, driver):
        driver.get(f"{BASE_URL}/ranking/xxxxxxxxxxx-invalid")
        assert is_safe_error_page(driver)