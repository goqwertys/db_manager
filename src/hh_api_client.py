import requests

from src.api_client import APIClient

class HHAPIClient(APIClient):
    """ Client for fetching data from hh.ru public API """
    BASE_URL = 'https://api.hh.ru/vacancies'

    def __init__(self, employer_id):
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {
            'employer_id': employer_id,
            'per_page': 100  # Number of vacancies on one page
        }

        self.vacancies = []

    def load_vacancies_by_emp_id(self, employer_id):
        """ Loads vacancies by employer_id """
        # TODO employer_id validation
        self.params['employer_id'] = employer_id
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

    def get_info(self):
        return self.vacancies
