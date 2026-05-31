from config import BASE_URL, VALID_COURSE_SLUG, WAIT_TIMEOUT
from selenium.webdriver.support.ui import WebDriverWait
from conftest import is_safe_error_page


class TestDetailCourse:

    def test_positive_buka_course_public(self, driver):
        driver.get(f"{BASE_URL}/{VALID_COURSE_SLUG}")

        assert "/courses/" in driver.current_url, (
            "URL course public seharusnya berada pada route /courses/"
        )

        WebDriverWait(driver, WAIT_TIMEOUT).until(lambda d: d.title != "")

        assert driver.title != "", (
            "Halaman detail course public seharusnya memiliki title"
        )

    def test_negative_buka_course_slug_invalid(self, driver):
        invalid_course_slug = "course-slug-invalid-xxxxxxxxxxx-999"

        driver.get(f"{BASE_URL}/courses/{invalid_course_slug}")

        WebDriverWait(driver, WAIT_TIMEOUT).until(lambda d: d.title != "")

        assert is_safe_error_page(driver), (
            "Course dengan slug invalid seharusnya menampilkan halaman error yang aman"
        )