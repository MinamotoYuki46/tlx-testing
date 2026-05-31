from config import BASE_URL, VALID_CONTEST_SLUG, INVALID_CONTEST_SLUG
from conftest import is_safe_error_page


class TestScoreboardContest:

    def test_positive_scoreboard_contest_public(self, driver):
        driver.get(f"{BASE_URL}/{VALID_CONTEST_SLUG}/scoreboard")
        assert "scoreboard" in driver.current_url
        assert not is_safe_error_page(driver) or "scoreboard" in driver.page_source.lower()

    def test_negative_scoreboard_contest_invalid(self, driver):
        driver.get(f"{BASE_URL}/{INVALID_CONTEST_SLUG}/scoreboard")
        assert is_safe_error_page(driver)
