import psycopg2

from cw_5.db.managers.base import DBManager


class PostgresDBManager(DBManager):
    """
    Подключение к БД Postgres
    """
    def connect(self) -> None:
        if self.connection is None:
            self.connection = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )

    def disconnect(self) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def get_companies_and_vacancies_count(self) -> list[tuple[str, list]]:
        """
        Получение списка всех компаний и количество вакансий у каждой компании
        :return:
        """
        sql = """
            SELECT e.name, COUNT(*) as vacancies_count
            FROM employers as e
            LEFT JOIN vacancies as v ON e.id = v.employer_id
            GROUP BY e.name;
        """
        self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def get_avg_salary(self) -> float:
        """
        ПОлучение средней зарплаты по вакансиям
        :return:
        """
        sql = """SELECT AVG(v.salary_from), AVG(v.salary_to) FROM vacancies as v;"""
        self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            min_salary, max_salary = cursor.fetchone()
            average_salary = (min_salary + max_salary) / 2
            return round(average_salary, 2)



