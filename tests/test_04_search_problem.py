import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from config import BASE_URL, WAIT_TIMEOUT


class TestSearchProblem:

    def test_positive_search_keyword_valid(self, driver):
        driver.get(f"{BASE_URL}/problems/problemsets?name=arkavidia")
    
        visible_result_links = WebDriverWait(driver, WAIT_TIMEOUT).until(
            lambda d: [
                link for link in d.find_elements(
                    By.CSS_SELECTOR,
                    "a.content-card-link[href^='/problems/']"
                )
                if link.is_displayed()
                and link.text.strip()
                and "arkavidia" in link.text.lower()
            ]
        )
    
        body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
    
        assert "arkavidia" in body_text, (
            "Keyword valid 'arkavidia' seharusnya muncul pada hasil pencarian"
        )
    
        assert len(visible_result_links) > 0, (
            "Keyword valid seharusnya menampilkan minimal satu hasil problemset"
        )

    def test_negative_search_keyword_invalid(self, driver):
        driver.get(f"{BASE_URL}/problems/problemsets?name=ulmitfest")

        WebDriverWait(driver, WAIT_TIMEOUT).until(lambda d: d.title != "")
        time.sleep(2)

        body_text = driver.find_element(By.TAG_NAME, "body").text.lower()

        result_links = driver.find_elements(
            By.CSS_SELECTOR,
            "a[href*='/problems/problemsets/']"
        )

        visible_result_links = []
        for link in result_links:
            href = link.get_attribute("href") or ""
            text = link.text.strip()

            if (
                link.is_displayed()
                and text
                and "/problems/problemsets/" in href
                and "name=" not in href
            ):
                visible_result_links.append(link)

        no_result_message = any(
            keyword in body_text
            for keyword in [
                "no problemset",
                "no problem",
                "not found",
                "no result",
                "empty",
                "tidak ditemukan",
                "kosong",
            ]
        )

        assert no_result_message or len(visible_result_links) == 0, (
            "Keyword invalid 'ulmitfest' seharusnya tidak menampilkan hasil problemset"
        )