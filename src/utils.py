import psycopg2

def create_database(database_name: str, params: dict):
    """ Creates a new database and tables within it """

    try:
        # Connect to the default 'postgres' database to create the new database
        with psycopg2.connect(dbname='postgres', **params) as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                # Drop the database if it already exists
                cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
                # Create the new database
                cur.execute(f'CREATE DATABASE {database_name}')

        # Connect to the newly created database
        with psycopg2.connect(dbname=database_name, **params) as conn:
            with conn.cursor() as cur:
                # Create table areas
                cur.execute(
                    """
                    CREATE TABLE areas (
                        area_id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        url TEXT
                    )
                    """
                )

                # Create table employers
                cur.execute(
                    """
                    CREATE TABLE employers (
                        employer_id INTEGER PRIMARY KEY,
                        employer_name TEXT NOT NULL,
                        employer_area INTEGER REFERENCES areas(area_id),
                        url TEXT,
                        open_vacancies INTEGER
                    )
                    """
                )

                # Create table vacancies
                cur.execute(
                    """
                    CREATE TABLE vacancies (
                        vacancy_id INTEGER PRIMARY KEY,
                        vacancy_name VARCHAR,
                        vacancy_area INTEGER REFERENCES areas(area_id),
                        salary INTEGER,
                        employer_id INTEGER REFERENCES employers(employer_id),
                        vacancy_url VARCHAR
                    )
                    """
                )

            # Commit the transaction
            conn.commit()

    except psycopg2.Error as e:
        print(f"Error: {e}")
        return False

    return True

def save_to_database():
    """ Save data to database """
    pass
