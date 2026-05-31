from config import BASE_URL, VALID_CONTEST_SLUG, INVALID_CONTEST_SLUG
from conftest import is_safe_error_page


class TestProblemContest:

    def test_positive_buka_tab_problem_contest(self, driver):
        driver.get(f"{BASE_URL}/{VALID_CONTEST_SLUG}/problems")
        assert "problems" in driver.current_url
        assert not is_safe_error_page(driver) or "problems" in driver.page_source.lower()

    def test_negative_problem_contest_kode_invalid(self, driver):
        driver.get(f"{BASE_URL}/{INVALID_CONTEST_SLUG}/problems")
        assert is_safe_error_page(driver)
