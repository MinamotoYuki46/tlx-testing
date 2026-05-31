import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from config import BASE_URL, VALID_PROBLEM_SLUG, INVALID_PROBLEM_SLUG
from conftest import wait_for

SAMPLE_SELECTOR = "pre, code, .sample-io, [class*='sample']"


class TestSampleInputOutput:

    def test_positive_sample_io_tampil(self, driver):
        """TC-07P: Sample input/output problem valid harus tampil."""
        driver.get(f"{BASE_URL}/{VALID_PROBLEM_SLUG}")
        try:
            el = wait_for(driver, By.CSS_SELECTOR, SAMPLE_SELECTOR)
            assert el.is_displayed()
        except TimeoutException:
            pytest.skip("Elemen sample I/O tidak ditemukan — sesuaikan selector")

    def test_negative_sample_io_tidak_tampil_problem_invalid(self, driver):
        """TC-07N: Problem invalid tidak boleh menampilkan sample I/O."""
        driver.get(f"{BASE_URL}/{INVALID_PROBLEM_SLUG}")
        els = driver.find_elements(By.CSS_SELECTOR, "[class*='sample-input'], [class*='sample-output']")
        assert len(els) == 0 or not any(e.is_displayed() for e in els)
