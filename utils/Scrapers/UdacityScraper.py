import urllib

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

from utils.WebDriverManager import WebDriverManager


class UdacityScraper:
    def scrape(self, query):
        driver = WebDriverManager.get_driver()

        # Codificar la consulta y construir la URL
        encoded_query = urllib.parse.quote(query)
        url = f'https://www.udacity.com/catalog/all/any-price/any-school/any-skill/any-difficulty/any-duration/any-type/relevance/page-1?searchValue={encoded_query}'
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".css-15q7znr"))
        )

        # Extraer el HTML y analizarlo con BeautifulSoup
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        course_cards = soup.findAll('div', class_='css-15q7znr')

        # Extraer los datos de cada tarjeta de curso
        courses = [self.extract_course_data(card) for card in course_cards]
        return courses

    @staticmethod
    def extract_course_data(card):
        image_element = card.find('img')
        image_url = image_element['src'] if image_element else 'No image found'
        title_element = card.find('div', class_='chakra-heading css-1rsglaw')
        title = title_element.text.strip() if title_element else 'No title found'
        description_element = card.select_one('div.css-k008qs > p.chakra-text')
        description = description_element.text.strip() if description_element else ''
        rating_element = card.find('div', class_='css-nbgxi6')
        rating = rating_element[
            'aria-label'] if rating_element and 'aria-label' in rating_element.attrs else ''

        link_element = card.find('a', class_='css-752atj')
        course_url = f'https://www.udacity.com{link_element["href"]}' if link_element else ''

        return {
            "Image": image_url,
            "Title": title,
            "Description": description,
            "Score": rating,
            "CourseLink": course_url
        }
