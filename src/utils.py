from configparser import ConfigParser, NoSectionError, NoOptionError, MissingSectionHeaderError

import psycopg2
import logging

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

def create_database(database_name: str, params: dict):
    """ Creates a new database and tables within it """

    try:
        logger.info(f"Starting creation of database '{database_name}'")

        # Connect to the default 'postgres' database to create the new database
        with psycopg2.connect(dbname='postgres', **params) as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                # Drop the database if it already exists
                logger.info(f"Dropping database '{database_name}' if it exists")

                cur.execute(f'DROP DATABASE IF EXISTS {database_name};')
                # Create the new database
                logger.info(f"Creating database '{database_name}'")

                cur.execute(f'CREATE DATABASE {database_name};')

        # Connect to the newly created database
        with psycopg2.connect(dbname=database_name, **params) as conn:
            with conn.cursor() as cur:
                # Create table areas
                logger.info("Creating table 'areas'")

                cur.execute(
                    """
                    CREATE TABLE areas (
                        area_id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        url TEXT
                    );
                    """
                )

                # Create table employers
                logger.info("Creating table 'employers'")

                cur.execute(
                    """
                    CREATE TABLE employers (
                        employer_id INTEGER PRIMARY KEY,
                        employer_name TEXT NOT NULL,
                        employer_area INTEGER REFERENCES areas(area_id),
                        url TEXT,
                        open_vacancies INTEGER
                    );
                    """
                )

                # Create table vacancies
                logger.info("Creating table 'vacancies'")

                cur.execute(
                    """
                    CREATE TABLE vacancies (
                        vacancy_id INTEGER PRIMARY KEY,
                        vacancy_name VARCHAR,
                        vacancy_area INTEGER REFERENCES areas(area_id),
                        salary INTEGER,
                        employer_id INTEGER REFERENCES employers(employer_id),
                        vacancy_url VARCHAR
                    );
                    """
                )

            # Commit the transaction
            conn.commit()

        logger.info(f"Database '{database_name}' and tables created successfully")

    except psycopg2.Error as e:
        logger.error(f"Error creating database '{database_name}': {e}")
        return False

    return True

def save_to_database():
    """ Save data to database """
    pass


def read_db_config(config_file: str) -> dict[str, str]:
    """ Reads config file and returns params for connection to DB """
    config = ConfigParser()
    try:
        logger.info(f"Reading config file: {config_file}")
        config.read(config_file)

        if 'postgres' not in config:
            raise NoSectionError('postgres')

        db_config = {
            'host': config['postgres'].get('host', ''),
            'port': config['postgres'].get('port', ''),
            'user': config['postgres'].get('user', ''),
            'password': config['postgres'].get('password', '')
        }

        if not all(db_config.values()):
            raise NoOptionError('postgres', 'One or more required options are missing')

        logger.info(f"Successfully read config file: {config_file}")
        return db_config

    except (FileNotFoundError, NoSectionError, NoOptionError, MissingSectionHeaderError) as e:
        logger.error(f'Error reading config file: {e}')
        return {}