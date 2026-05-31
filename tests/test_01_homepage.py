from config import BASE_URL, WAIT_TIMEOUT
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from conftest import is_safe_error_page


class TestHomepage:

    def test_positive_homepage_loads(self, driver):
        driver.get(BASE_URL)

        try:
            WebDriverWait(driver, WAIT_TIMEOUT).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )

            WebDriverWait(driver, WAIT_TIMEOUT).until(
                lambda d: d.find_element(By.TAG_NAME, "body").text.strip() != ""
            )

        except TimeoutException:
            body_text = (
                driver.find_element(By.TAG_NAME, "body").text
                if driver.find_elements(By.TAG_NAME, "body")
                else ""
            )

            assert False, (
                "Homepage tidak selesai dimuat dalam batas waktu.\n"
                f"URL saat ini    : {driver.current_url}\n"
                f"Title saat ini  : {driver.title!r}\n"
                f"Body length     : {len(body_text)}\n"
                f"Body preview    : {body_text[:300]!r}"
            )

        body_text = driver.find_element(By.TAG_NAME, "body").text.lower()

        assert BASE_URL.lower().rstrip("/") in driver.current_url.lower().rstrip("/"), (
            f"Homepage tidak berada pada BASE_URL.\n"
            f"Expected base : {BASE_URL}\n"
            f"Actual URL    : {driver.current_url}"
        )

        assert "tlx" in body_text, (
            "Homepage seharusnya menampilkan identitas TLX"
        )

        assert "competitive programming training gate" in body_text, (
            "Homepage seharusnya menampilkan teks utama TLX"
        )

        assert "home" in body_text, (
            "Homepage seharusnya menampilkan menu Home"
        )

        assert "contests" in body_text, (
            "Homepage seharusnya menampilkan menu Contests"
        )

        assert "problems" in body_text, (
            "Homepage seharusnya menampilkan menu Problems"
        )

    def test_negative_typo_tlx_toki_no_crash(self, driver):
        typo_paths = [
            "tlxx",
            "tokii",
            "tlx-tokii",
            "tlx-toki-invalid",
        ]
    
        for path in typo_paths:
            driver.get(f"{BASE_URL}/{path}")
    
            assert is_safe_error_page(driver), (
                f"Halaman typo seharusnya menampilkan error aman.\n"
                f"Path: /{path}\n"
                f"URL saat ini: {driver.current_url}"
            )