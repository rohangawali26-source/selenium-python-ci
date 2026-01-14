import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

CHANNEL_URL = "https://www.youtube.com/@google/videos"
VIDEO_FILE = "last_video.txt"


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        ChromeDriverManager().install(),
        options=options
    )
    yield driver
    driver.quit()


def test_latest_youtube_video(driver):
    wait = WebDriverWait(driver, 30)
    driver.get(CHANNEL_URL)

    try:
        consent = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button//span[text()='Accept all']")
            )
        )
        consent.click()
    except:
        pass

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    latest_video = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "a#video-title-link")
        )
    )

    latest_video_url = latest_video.get_attribute("href")
    assert latest_video_url is not None

    with open(VIDEO_FILE, "w") as f:
        f.write(latest_video_url)
