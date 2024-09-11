import logging

from src.config import LOG_LEVEL
from src.hh_api_client import HHAPIClient
from src.paths import root_join
from src.utils import read_employers_list, read_db_config

# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
log_path = root_join('logs', f'{__name__}.log')
fh = logging.FileHandler(log_path, mode='w')
formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

def main() -> bool:
    """ Main function """
    logger.info('The program has been launched')
    try:
        config_path = root_join('data', 'config.ini')
        params = read_db_config(config_path)

        logger.info('Params successfully received')

        # Get a list of saved employers to work with

        emp_ids_path = root_join('data', 'employer_ids.json')
        logger.info(f'Reading employers ids from {emp_ids_path}')
        employers_list = read_employers_list(emp_ids_path)

        logger.info(f'IDs is {employers_list}')

        # Creating HH API Client
        logger.info('Creating hh.ru API Client')
        hh_client = HHAPIClient()

        logger.info('Loading vacancies from employers')
        hh_client.load_vacancy_by_emp_id(employers_list)

        #


    except Exception as e:
        logger.error(f'An error has occured: {e}')
        return False

    while True:
        print("""Please enter the following characters to:
        'EXT' : Exit the program
        'CVCOUNT' : Get a list of all companies and the number of vacancies for each company
        'GETALL' : Get a list of all vacancies with the company name, job title and salary and a link to the vacancy
        'AVGSAL' : Get average salary for vacancies
        'HIAVG' : Get a list of all vacancies where the salary is higher than the average for all vacancies
        'KEYW' : Get a list of all vacancies whose titles contain the words passed to the method, for example python
        """)
        user_input = input()

        if user_input.lower() == 'ext':
            return True

        elif user_input.lower() == 'cvcount':
            pass

        elif user_input.lower() == 'getall':
            pass

        elif user_input.lower() == 'avgsal':
            pass

        elif user_input.lower() == 'hiavg':
            pass

        elif user_input.lower() == 'keyw':
            pass
        else:
            print('Your request is not provided, please enter another request')


if __name__ == '__main__':
    main()
