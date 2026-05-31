from config import BASE_URL, VALID_CONTEST_SLUG, INVALID_CONTEST_SLUG
from conftest import is_safe_error_page


class TestAnnouncementsContest:

    def test_positive_announcements_contest_public(self, driver):
        driver.get(f"{BASE_URL}/{VALID_CONTEST_SLUG}/announcements")
        assert "announcements" in driver.current_url

    def test_negative_announcements_route_invalid(self, driver):
        driver.get(f"{BASE_URL}/{INVALID_CONTEST_SLUG}/announcements")
        assert is_safe_error_page(driver)
