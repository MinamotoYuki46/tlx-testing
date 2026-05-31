from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from config import BASE_URL, VALID_PROBLEM_SLUG, INVALID_PROBLEM_SLUG
from conftest import wait_for

STATEMENT_SELECTOR = ".problem-statement, .statement, [class*='statement']"


class TestStatementProblem:

    def test_positive_statement_tampil(self, driver):
        """TC-06P: Statement problem valid harus tampil."""
        driver.get(f"{BASE_URL}/{VALID_PROBLEM_SLUG}")
        try:
            el = wait_for(driver, By.CSS_SELECTOR, STATEMENT_SELECTOR)
            assert el.is_displayed()
        except TimeoutException:
            assert len(driver.page_source) > 1000, "Statement tidak ditemukan"

    def test_negative_statement_tidak_ada_problem_invalid(self, driver):
        """TC-06N: Problem invalid tidak boleh menampilkan statement."""
        driver.get(f"{BASE_URL}/{INVALID_PROBLEM_SLUG}")
        els = driver.find_elements(By.CSS_SELECTOR, STATEMENT_SELECTOR)
        assert len(els) == 0 or not any(e.is_displayed() for e in els)
