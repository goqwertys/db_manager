# DB VACANCY MANAGER
## Instalation:
1. Clone repo:
    ```
    git clone https://github.com/goqwertys/db_manager.git
    ```
2. Start the virtual environment:
    ```
    poetry install
    ```
## Usage
1. Check and adjust the `/data/config.ini` as needed
    ```
    [postgres]
    host = localhost
    port = 5432
    user = postgres
    password = your_password
    ```
2. Check `data/employer_ids.json` file for companies you are interested in:
    ```
    [
      4344489,
      597423,
      851716,
      9510458,
      2015058,
      9574451,
      3672566,
      6098532,
      4602050,
      3244995
    ]
    ```
3. Run `main.py` or enter the following in the terminal:
    ```commandline
    python main.py
    ```
<p>The program will download vacancies of the companies you are interested in and insert them into the database.</p>
<p>You will then be presented with several options for what data you can see.</p>
