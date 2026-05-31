from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from config import BASE_URL, WAIT_TIMEOUT
from conftest import is_safe_error_page


INVALID_PROFILE_PATH = "/profile"


def wait_page_loaded(driver):
    WebDriverWait(driver, WAIT_TIMEOUT).until(
        lambda d: d.find_element(By.TAG_NAME, "body").text.strip() != ""
    )


def clear_session(driver):
    """Bersihkan cookie, localStorage, dan sessionStorage."""
    driver.get(BASE_URL)
    driver.delete_all_cookies()
    driver.execute_script(
        "window.localStorage.clear(); window.sessionStorage.clear();"
    )
    driver.get(BASE_URL)
    wait_page_loaded(driver)


def is_not_found_or_safe_error(driver):
    """Cek apakah halaman menampilkan 404/not found/error aman."""
    url = driver.current_url.lower()
    page = driver.page_source.lower()

    shows_not_found = any(kw in url or kw in page for kw in [
        "404",
        "not found",
        "page not found",
        "tidak ditemukan",
    ])

    return shows_not_found or is_safe_error_page(driver)


def get_visible_profile_candidates(driver):
    """
    Ambil kandidat link profil user setelah login.

    Tidak memakai teks 'profile' saja, karena bisa false positive.
    Di TLX, halaman user biasanya lebih mungkin berupa link user/avatar/menu,
    bukan route hardcoded /profile.
    """
    candidates = driver.find_elements(
        By.XPATH,
        """
        //a[
            contains(translate(@href, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '/users/')
            or contains(translate(@href, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '/profile')
        ]
        |
        //button[
            contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'profile')
            or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'profil')
        ]
        """
    )

    return [
        el for el in candidates
        if el.is_displayed()
    ]


class TestProtectedPage:

    def test_positive_user_login_melihat_akses_profil(self, logged_in_driver):
        """
        TC-20P: User login harus memiliki akses/menu profil.
        Jangan hardcode /profile karena route tersebut memang Not Found di TLX.
        """
        logged_in_driver.get(BASE_URL)
        wait_page_loaded(logged_in_driver)

        profile_candidates = get_visible_profile_candidates(logged_in_driver)

        print("Jumlah kandidat profil:", len(profile_candidates))
        for el in profile_candidates[:5]:
            print("TAG:", el.tag_name)
            print("TEXT:", el.text)
            print("HREF:", el.get_attribute("href"))
            print("CLASS:", el.get_attribute("class"))
            print("---")

        assert len(profile_candidates) > 0, (
            "User yang sudah login seharusnya memiliki link/menu menuju profil atau halaman user"
        )

    def test_negative_user_belum_login_akses_profile_url_invalid(self, driver):
        """
        TC-20N: User belum login memaksa akses /profile.
        Pada TLX, route ini memang tidak tersedia dan harus menghasilkan 404/error aman.
        """
        clear_session(driver)

        driver.get(f"{BASE_URL}{INVALID_PROFILE_PATH}")
        wait_page_loaded(driver)

        assert is_not_found_or_safe_error(driver), (
            f"User belum login yang memaksa akses /profile seharusnya mendapat 404/error aman.\n"
            f"URL saat ini: {driver.current_url}"
        )