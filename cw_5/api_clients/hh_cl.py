from .base import APIClient
from .entities import ShortEmployerInfo, FullEmployerInfo, VacancyInfo
class HeadHunterAPIClient(APIClient):

    def __init__(self):
        """
        Функция для подключения к HH
        """
        self.__base_url = 'https://api.hh.ru/'

    def search_employers(self, search: str, *, only_with_vacancies: bool = True) -> list[ShortEmployerInfo]:
        """
        Функция для поиска по работадателям
        :rtype: object
        :param search
        :param only_with_vacancies:
        :return:
        """
        params = {
            'text': search,
            'only_with_vacancies': only_with_vacancies
        }
        employers = self._get_items('employers', params=params)
        return [
            ShortEmployerInfo(
                id=int(emp['id']),
                name=emp['name'],
                url=emp['alternate_url'],
                open_vacancies=emp['open_vacancies'],
            )
            for emp in employers
        ]

    def get_employer_info(self, employer_id: int) -> FullEmployerInfo:
        """
        Получение полной информации о работадателе
        :param employer_id:
        :return:
        """
        employer_info = self._get(f'/employers/{employer_id}')
        return FullEmployerInfo(
            id=employer_id,
            name=employer_info['name'],
            url=employer_info['alternate_url'],
            site_url=employer_info['site_url'],
            region=employer_info['area']['name'],
            open_vacancies=employer_info['open_vacancies'],

        )

    def get_employer_vacancies(self, employer_id: int) -> list[VacancyInfo]:
        """
        Получение полной информации о вакансии
        :param employer_id:
        :return:
        """
        params = {
            'employer_id': employer_id,
            'only_with_salary': True
        }
        vacancies = self._get_items('/vacancies', params=params)
        return [
            VacancyInfo(
                id=int(vac['id']),
                name=vac['name'],
                url=vac['alternate_url'],
                salary_from=vac['salary'].get('from'),
                salary_to=vac['salary'].get('to'),
                employer_id=employer_id,
            )
            for vac in vacancies

        ]



    @property
    def base_url(self) -> str:
        return self.__base_url

    def _get_items(self, url: str, params: dict) -> list[dict]:
        """
        Функция, которая позволяет забрать весь список данных с HH
        """
        items = []
        params['page'] = 0
        params['per_page'] = 100
        while True:
            data = self._get(url, params=params)
            items.extend(data['items'])

            total_pages = data['pages']
            if total_pages == params['page']:
                break
            params['page'] += 1

            if len(items) >= 2_000:
                break

        return items


