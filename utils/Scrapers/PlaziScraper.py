from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from utils.WebDriverManager import WebDriverManager


class PlatziScraper:
    def scrape(self, category):
        driver = WebDriverManager.get_driver()
        url = f"https://platzi.com/buscar/?search={category}&objecttype=course"

        driver.get(url)
        try:
            WebDriverWait(driver, 10).until(  # Increased timeout to 20 seconds
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'CourseCard'))  # Changed to presence_of_all_elements_located
            )
        except TimeoutException:
            print("Timed out waiting for page to load")
            return []
        finally:
            html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')
        course_cards = soup.find_all('div', class_='CourseCard')
        courses = [self.extract_course_data(card) for card in course_cards]

        return courses

    @staticmethod
    def extract_course_data(card):
        # Extract the title and link to the course
        title_link_element = card.select_one("a.CourseCard-maintitle-copy")
        title = title_link_element.text.strip() if title_link_element else "No title found"
        course_url = 'https://platzi.com' + title_link_element['href'] if title_link_element and 'href' in title_link_element.attrs else "No link found"

        # Extract the course image URL
        image_element = card.select_one('.CourseCard-preview-image img')
        image_url = image_element['src'] if image_element else "No image found"

        # Extract the course description
        description_element = card.select_one(".CourseCard-description")
        description = description_element.text.strip() if description_element else "No description found"

        # Platzi does not typically display ratings in the same way, so this might not be applicable
        rating = "Not Available"

        return {
            "Image": image_url,
            "Title": title,
            "Description": description,
            "Score": rating,
            "CourseLink": course_url
        }