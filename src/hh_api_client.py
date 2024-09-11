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
        self.vacancies = []

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
                self.vacancies.extend(vacancies)

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
        return self.vacancies
