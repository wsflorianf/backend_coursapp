import requests
from bs4 import BeautifulSoup


class CourseraScraper:
    def __init__(self):
        self.base_url = "https://www.coursera.org"
        self.search_url = f"{self.base_url}/search"

    def scrape(self, query, language, level, duration):
        params = {'query': query, 'sortBy': 'BEST_MATCH'}

        # Mapa de niveles a la URL de dificultad de Coursera
        level_map = {
            'beginner': 'Beginner',
            'intermediate': 'Intermediate',
            'advanced': 'Advanced'
        }

        # Mapa de duraciones a los parámetros de Coursera
        duration_map = {
            'hours': 'Less%20Than%202%20Hours',
            'days': '1-4%20Weeks',
            'weeks': '1-4%20Weeks',
            'months': '1-3%20Months%2C3-6%20Months%2C6-12%20Months%2C1-4%20Years'
        }

        if language:
            params['language'] = language.capitalize()

        if level:
            params['productDifficultyLevel'] = level_map.get(level, '')

        if duration:
            params['duration'] = duration_map.get(duration, '')

        response = requests.get(self.search_url, params=params)
        soup = BeautifulSoup(response.content, "html.parser")

        cards = soup.find_all("div", {"data-testid": "product-card-cds"})
        courses = []

        for card in cards:
            title_link = card.find("a", {"data-track": "true"})
            title = title_link.find("h3", class_="cds-CommonCard-title").text.strip() if title_link else ""
            course_url = self.base_url + title_link["href"] if title_link else ""

            description_tag = card.find("p", class_="cds-CommonCard-bodyContent")
            description = description_tag.text.strip() if description_tag else ""

            rating_tag = card.find("div", class_="cds-CommonCard-ratings")
            rating = rating_tag.text.strip() if rating_tag else ""

            image_tag = card.find("img")
            image_url = image_tag["src"] if image_tag else ""

            courses.append({
                "Image": image_url,
                "Title": title,
                "Description": description,
                "Score": rating,
                "CourseLink": course_url
            })

        return courses
