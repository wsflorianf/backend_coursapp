import urllib

import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from utils.WebDriverManager import WebDriverManager


class UdacityScraper:
    def scrape(self, query, level, duration, price):
        driver = WebDriverManager.get_driver()

        level_map = {
            'beginner': 'beginner',
            'intermediate': 'intermediate',
            'advanced': 'advanced'
        }

        duration_map = {
            'hours': 'hours',
            'days': 'days',
            'weeks': 'weeks',
            'months': 'months'
        }

        price_map = {
            'free': 'free',
            'paid': 'paid'
        }

        encoded_query = urllib.parse.quote(query)
        level_param = level_map.get(level, 'any-difficulty')
        duration_param = duration_map.get(duration, 'any-duration')
        price_param = price_map.get(price, 'any-price')

        url = f'https://www.udacity.com/catalog/all/{price_param}/any-school/any-skill/{level_param}/{duration_param}/any-type/relevance/page-1?searchValue={encoded_query}'
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".css-15q7znr, .css-1mbed0a"))
        )

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        no_results_card = soup.find('div', class_='css-1mbed0a')
        if no_results_card and no_results_card.find('h2', class_='chakra-heading').text.strip() == "No Results Found":
            return []

        course_cards = soup.findAll('div', class_='css-15q7znr')

        # Extraer los datos de cada tarjeta de curso
        courses = [self.extract_course_data(card) for card in course_cards]
        return courses

    @staticmethod
    def extract_course_data(card):
        image_element = card.find('img')
        image_url = image_element['src'] if image_element else 'No image found'
        title_element = card.find('a', class_='chakra-heading css-1rsglaw')
        title = title_element.text.strip() if title_element else 'No title found'
        course_url = f"https://www.udacity.com{title_element['href']}" if title_element else ''
        description_element = card.select_one('div.css-k008qs > p.chakra-text')
        description = description_element.text.strip() if description_element else ''
        rating_element = card.find('div', class_='css-nbgxi6')
        rating = rating_element['aria-label'] if rating_element and 'aria-label' in rating_element.attrs else ''
        return {
            "Image": image_url,
            "Title": title,
            "Description": description,
            "Score": rating,
            "CourseLink": course_url
        }
