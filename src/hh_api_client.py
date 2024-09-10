import requests

from src.api_client import APIClient

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
        # Validation
        employer_id = self.valid_id(employer_id)
        self.check_existence(employer_id)

        # Requesting data
        self.params['employer_id'] = employer_id
        self.params['page'] = 0  # Reset page to 0

        while True:
            try:
                response = requests.get(self.BASE_URL, headers=self.headers, params=self.params)
                response.raise_for_status()
                data = response.json()
                vacancies = data['items']
                self.vacancies.extend(vacancies)
                if self.params['page'] >= data['pages'] - 1:
                    break
                self.params['page'] += 1
            except requests.RequestException as e:
                print(f'An error has occurred: {e}')
                break

    def load_vacancies_by_emp_ids(self, emp_ids: list[int]):
        """ Loads vacancies by a list of employer_ids """
        for employer_id in emp_ids:
            self.load_vacancy_by_emp_id(employer_id)

    @staticmethod
    def valid_id(employer_id):
        """ Validates employer id """
        if isinstance(employer_id, int) and employer_id > 0:
            return employer_id
        raise ValueError('Invalid employer ID')

    @staticmethod
    def check_existence(employer_id):
        """ Checks if employer_id exists on hh.ru """
        url = f"{HHAPIClient.EMPLOYER_URL}/{employer_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            raise ValueError("Employer ID does not exist")
        else:
            raise ValueError("Failed to check employer ID")


    def get_info(self):
        return self.vacancies
