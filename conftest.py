"""
conftest.py
Fixture dan helper bersama untuk seluruh test.
Dibaca otomatis oleh pytest dari semua file test dalam folder tests/.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from config import BASE_URL, WAIT_TIMEOUT, HEADLESS, VALID_USERNAME, VALID_PASSWORD


# =============================================================================
# FIXTURE: WebDriver
# =============================================================================

@pytest.fixture(scope="function")
def driver():
    """Inisialisasi dan teardown Chrome WebDriver untuk setiap test function."""
    options = Options()
    if HEADLESS:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,900")

    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(3)
    yield drv
    drv.quit()


@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """
    Fixture driver yang sudah dalam kondisi login.
    Digunakan untuk test yang memerlukan sesi autentikasi.
    """
    driver.get(f"{BASE_URL}/login")
    wait_for(driver, By.CSS_SELECTOR, "input[name='username'], input[type='text']").send_keys(VALID_USERNAME)
    driver.find_element(By.CSS_SELECTOR, "input[name='password'], input[type='password']").send_keys(VALID_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']").click()
    WebDriverWait(driver, WAIT_TIMEOUT).until(
        lambda d: "login" not in d.current_url
    )
    yield driver


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def wait_for(driver, by, locator, timeout=None):
    """Tunggu hingga elemen visible, lalu kembalikan elemennya."""
    t = timeout or WAIT_TIMEOUT
    return WebDriverWait(driver, t).until(
        EC.visibility_of_element_located((by, locator))
    )


def is_safe_error_page(driver):
    """
    Cek apakah halaman menampilkan error yang aman (404/not found/redirect),
    bukan crash atau stack trace berbahaya.
    """
    page = driver.page_source.lower()
    url  = driver.current_url.lower()

    has_safe_message = any(kw in page for kw in [
        "not found", "404", "halaman tidak ditemukan",
        "page not found", "doesn't exist", "no longer available",
    ])
    redirected_safely = (
        url.startswith(BASE_URL.lower()) and
        "exception" not in url
    )
    no_crash = not any(kw in page for kw in [
        "traceback", "syntaxerror", "uncaught exception",
        "internal server error", "500",
    ])

    return (has_safe_message or redirected_safely) and no_crash
