from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

from utils.WebDriverManager import WebDriverManager


class DomestikaScraper:
    def scrape(self, category):
        driver = WebDriverManager.get_driver()
        url = f"https://www.domestika.org/es/courses/search/{category}"

        driver.get(url)
        try:
            # Utiliza 'presence_of_element_located' que puede ser más rápido que 'visibility_of_element_located'
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-testid='coursecard']"))
            )
        finally:
            html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')
        course_cards = soup.find_all('div', {'data-testid': 'coursecard'})
        courses = [self.extract_course_data(card) for card in course_cards]

        return courses

    @staticmethod
    def extract_course_data(card):
        title_element = card.find('h3')
        title = title_element.text.strip() if title_element else ""

        link_element = card.find('a', href=True)
        course_url = 'https://www.domestika.org' + link_element['href'] if link_element else ""

        description_element = card.find('h4', class_='ContanierCard-DescriptionClass')
        description = description_element.text.strip() if description_element else ""

        rating_element = card.select_one('.m-course-stats__stat--inline .a-icon-thumbs-up')
        if rating_element:
            rating_text = rating_element.parent.get_text(strip=True)
            rating = rating_text.split('(')[0].strip() if '(' in rating_text else rating_text.strip()
        else:
            rating = ""

        image_element = card.find('img')
        image_url = image_element['src'] if image_element else ""

        return {
            "Image": image_url,
            "Title": title,
            "Description": description,
            "Score": rating,
            "CourseLink": course_url
        }
