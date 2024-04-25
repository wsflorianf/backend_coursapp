from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class WebDriverManager:
    _driver = None

    @classmethod
    def get_driver(cls):
        if cls._driver is None:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--blink-settings=imagesEnabled=false")  # Desactivar imágenes
            options.add_experimental_option("prefs", {
                "profile.default_content_setting_values": {
                    "images": 2,  # No cargar imágenes
                    "stylesheet": 2  # No cargar CSS
                }
            })
            options.page_load_strategy = 'eager'
            options.add_argument("--disable-javascript")
            options.add_argument("--disable-gpu")
            cls._driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return cls._driver

    @classmethod
    def close_driver(cls):
        if cls._driver:
            cls._driver.quit()
            cls._driver = None
