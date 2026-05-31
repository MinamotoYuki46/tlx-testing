from config import BASE_URL, INVALID_COURSE_SLUG, WAIT_TIMEOUT
from selenium.webdriver.support.ui import WebDriverWait
from conftest import is_safe_error_page


class TestCourses:

    def test_positive_halaman_courses_tampil(self, driver):
        driver.get(f"{BASE_URL}/courses")
        assert "/courses" in driver.current_url
        WebDriverWait(driver, WAIT_TIMEOUT).until(lambda d: d.title != "")
        assert driver.title != ""

    def test_negative_course_slug_invalid(self, driver):
        driver.get(f"{BASE_URL}/{INVALID_COURSE_SLUG}")
        assert is_safe_error_page(driver)