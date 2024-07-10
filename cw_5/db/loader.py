from tqdm import tqdm
from cw_5.api_clients import HeadHunterAPIClient
from cw_5.config import settings
from cw_5.db.managers import PostgresDBManager

api_client = HeadHunterAPIClient()


def load_employers():
    """
    Загрузка работаателей
    :return:
    """
    employer_ids = settings.get_employer_ids()
    sql = """
        INSERT INTO employers(id, name, url, site_url, region)
        VALUES(%s, %s, %s, %s, %s);
    """
    db_manager = PostgresDBManager()
    db_manager.connect()

    try:
        with db_manager.connection.cursor() as cursor:
            for employer_id in tqdm(employer_ids, desc='Загрузка работадателей...'):
                emp = api_client.get_employer_info(employer_id)
                cursor.execute(sql, (emp.id, emp.name, emp.url, emp.site_url, emp.region))

            db_manager.commit()
    finally:
        db_manager.disconnect()


def load_vacancies():
    """
    Загрузка вакансий
    :return:
    """
    employer_ids = settings.get_employer_ids()
    sql = """
        INSERT INTO vacancies(id, name, url,  salary_from, salary_to, employer_id)
        VALUES(%s, %s, %s, %s,%s, %s);
        """
    db_manager = PostgresDBManager()
    db_manager.connect()

    try:
        with db_manager.connection.cursor() as cursor:
            for employer_id in tqdm(employer_ids, desc='Загрузка вакансий...'):
                vacancies = api_client.get_employer_vacancies(employer_id)
                data = (
                    (vac.id, vac.name, vac.url, vac.salary_from, vac.salary_to, employer_id)
                    for vac in vacancies
                )
                cursor.executemany(sql, data)

            db_manager.commit()
    finally:
        db_manager.disconnect()


