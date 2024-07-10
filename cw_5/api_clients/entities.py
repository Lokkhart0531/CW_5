from dataclasses import dataclass

@dataclass
class ShortEmployerInfo:
    """
    Класс для получения минимально необходимой информации о работадателе
    """
    id: int
    name: str
    url: str
    open_vacancies: int
@dataclass
class FullEmployerInfo:
    """
    Получение всей информации о работодателе
    """
    id: int
    name: str
    url: str
    site_url: str
    region: str
    open_vacancies: int

@dataclass
class VacancyInfo:
    """
    Получении информации о вакансии
    """
    id: int
    name: str
    url: str
    salary_from: int | None
    salary_to: int | None
    employer_id: int

