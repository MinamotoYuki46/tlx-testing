from config import BASE_URL, WAIT_TIMEOUT
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from conftest import is_safe_error_page


VALID_SUBMISSION_ID = "5463281"
INVALID_SUBMISSION_ID = "999999999999999999"


class TestViewSubmission:

    def test_positive_view_submission_belum_login(self, driver):
        driver.get(f"{BASE_URL}/submissions/{VALID_SUBMISSION_ID}")

        WebDriverWait(driver, WAIT_TIMEOUT).until(lambda d: d.title != "")

        WebDriverWait(driver, WAIT_TIMEOUT).until(
            lambda d: d.find_element(By.TAG_NAME, "body").text.strip() != ""
        )

        body_text = driver.find_element(By.TAG_NAME, "body").text.lower()

        login_required_keywords = [
            "login",
            "log in",
            "masuk",
            "sign in",
            "unauthorized",
            "forbidden",
            "permission",
            "access",
            "not allowed",
            "tidak diizinkan",
            "harus masuk",
            "harus login",
        ]

        assert "/submissions/" in driver.current_url or "/login" in driver.current_url, (
            "Halaman view submission seharusnya tetap berada di route submission "
            "atau diarahkan ke halaman login"
        )

        assert any(keyword in body_text for keyword in login_required_keywords), (
            "Submission valid yang dibuka tanpa login seharusnya menampilkan pesan "
            "bahwa user harus login atau tidak memiliki akses"
        )

    def test_negative_view_submission_id_salah(self, driver):
        driver.get(f"{BASE_URL}/submissions/{INVALID_SUBMISSION_ID}")

        WebDriverWait(driver, WAIT_TIMEOUT).until(lambda d: d.title != "")

        assert is_safe_error_page(driver)