from abc import ABC, abstractmethod
import requests

class APIClient(ABC):
    """
    Создание базового клиента через abstractmethod
    """
    @property
    @abstractmethod
    def base_url(self) -> str:
        pass

    def _get(self, url: str, params: dict = {}) -> dict:
        """
        Функция, которая принимает ссылку и параметры, а также возвращает словарь
        """
        full_url = self.base_url + url

        response = requests.get(full_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

