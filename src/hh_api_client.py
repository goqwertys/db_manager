import requests
import logging

from src.api_client import APIClient

from src.paths import root_join
from src.config import LOG_LEVEL

# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
log_path = root_join('logs', f'{__name__}.log')
fh = logging.FileHandler(log_path, mode='w')
formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

class HHAPIClient(APIClient):
    """ Client for fetching data from hh.ru public API """
    BASE_URL = 'https://api.hh.ru/vacancies'
    EMPLOYER_URL = 'https://api.hh.ru/employers'

    def __init__(self):
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {
            'per_page': 100,  # Number of vacancies on one page
            'page': 0  # Initial page
        }
        self.data = []

    def load_vacancy_by_emp_id(self, employer_id):
        """ Loads vacancies by a single employer_id """

        logger.info(f"Loading vacancies for employer ID: {employer_id}")

        # Validation
        employer_id = self.valid_id(employer_id)
        self.check_existence(employer_id)

        # Requesting data
        self.params['employer_id'] = employer_id
        self.params['page'] = 0  # Reset page to 0

        while True:
            try:
                logger.debug(f"Fetching page {self.params['page']} for employer ID: {employer_id}")

                response = requests.get(self.BASE_URL, headers=self.headers, params=self.params)
                response.raise_for_status()
                data = response.json()
                vacancies = data['items']
                self.data.extend(vacancies)

                logger.debug(f"Loaded {len(vacancies)} vacancies for employer ID: {employer_id}")

                if self.params['page'] >= data['pages'] - 1:
                    break
                self.params['page'] += 1
            except requests.RequestException as e:
                logger.error(f'An error has occurred: {e}')
                break

        logger.info(f"Finished loading vacancies for employer ID: {employer_id}")


    def load_vacancies_by_emp_ids(self, emp_ids: list[int]):
        """ Loads vacancies by a list of employer_ids """

        logger.info(f"Loading vacancies for employer IDs: {emp_ids}")

        for employer_id in emp_ids:
            self.load_vacancy_by_emp_id(employer_id)

        logger.info(f"Finished loading vacancies for employer IDs: {emp_ids}")

    @staticmethod
    def valid_id(employer_id):
        """ Validates employer id """
        logger.debug(f"Validating employer ID: {employer_id}")
        if isinstance(employer_id, int) and employer_id > 0:
            return employer_id
        raise ValueError('Invalid employer ID')

    @staticmethod
    def check_existence(employer_id):
        """ Checks if employer_id exists on hh.ru """
        logger.debug(f"Checking existence of employer ID: {employer_id}")
        url = f"{HHAPIClient.EMPLOYER_URL}/{employer_id}"
        response = requests.get(url)
        if response.status_code == 200:
            logger.debug(f"Employer ID {employer_id} exists")
            return True
        elif response.status_code == 404:
            logger.error(f"Employer ID {employer_id} does not exist")
            raise ValueError("Employer ID does not exist")
        else:
            logger.error(f"Failed to check employer ID {employer_id}")
            raise ValueError("Failed to check employer ID")


    def get_info(self):
        logger.info("Getting loaded vacancies")
        return self.data

    def get_areas(self):
        """ Returns a dict of areas in fetched data """
        areas = {}
        for vacancy in self.data:
            area = vacancy.get('area')
            area_id = area.get('id')
            if area_id not in areas:
                areas[area_id] = {
                    'name': area.get('name'),
                    'url': area.get('url')
                }
        return areas

    def get_employers(self):
        """ Returns a dict of employers in fetched data """
        employers = {}
        for vacancy in self.data:
            employer = vacancy.get('employer')
            employer_id = employer.get('id')
            if employer_id not in employers:
                employers[employer_id] = {
                    'name': employer.get('name'),
                    'area_id': int(employer.get('area').get('id')),
                    'url': employer.get('url'),
                    'open_vacancies': 0
                }
        return employers

    def get_vacancies(self):
        """ Returns a list of employers in fetched data """
        vacancies_list = []
        for vacancy in self.data:
            vacancies_list.append(
                {
                    'id': int(vacancy.get('id')),
                    'name': vacancy.get('name'),
                    'area_id': int(vacancy.get('area').get('id')),
                    'salary': vacancy.get('salary').get('from'),
                    'employer_id': id(vacancy.get('employer').get('id')),
                    'url': vacancy.get('url')
                }
            )
        return vacancies_list
