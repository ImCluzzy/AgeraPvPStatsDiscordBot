import requests
from typing import Dict, Optional
import logging

logger = logging.getLogger('AgeraPvPAPI')


class AgeraPvPAPI:
    
    BASE_URL = "http://api.agerapvp.club"
    
    def __init__(self, api_key: str = None):
        self.session = requests.Session()
        headers = {
            'User-Agent': 'AgeraPvP-Discord-Bot/1.0'
        }
        
        if api_key:
            headers['X-Api-Key'] = api_key
        
        self.session.headers.update(headers)
    
    def get_player_stats(self, name: str, mode: str) -> Optional[Dict]:
        url = f"{self.BASE_URL}/v1/player/stats/{name}/{mode}"
        
        try:
            logger.debug(f"Запрос статистики игрока: {url}")
            response = self.session.get(url, timeout=10)
            logger.debug(f"Ответ API: статус {response.status_code}, URL: {url}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout as e:
            logger.error(f"Таймаут при запросе статистики игрока {name} ({mode}): {e}, URL: {url}")
            return None
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Ошибка подключения при запросе статистики игрока {name} ({mode}): {e}, URL: {url}")
            return None
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response is not None else 'unknown'
            response_text = e.response.text[:200] if e.response is not None else 'N/A'
            logger.error(f"HTTP ошибка при запросе статистики игрока {name} ({mode}): статус {status_code}, ответ: {response_text}, URL: {url}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе статистики игрока {name} ({mode}): {type(e).__name__}: {e}, URL: {url}")
            return None
    
    def get_player_profile(self, name: str) -> Optional[Dict]:
        url = f"{self.BASE_URL}/v1/player/profile/{name}"
        
        try:
            logger.debug(f"Запрос профиля игрока: {url}")
            response = self.session.get(url, timeout=10)
            logger.debug(f"Ответ API: статус {response.status_code}, URL: {url}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout as e:
            logger.error(f"Таймаут при запросе профиля игрока {name}: {e}, URL: {url}")
            return None
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Ошибка подключения при запросе профиля игрока {name}: {e}, URL: {url}")
            return None
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response is not None else 'unknown'
            response_text = e.response.text[:200] if e.response is not None else 'N/A'
            logger.error(f"HTTP ошибка при запросе профиля игрока {name}: статус {status_code}, ответ: {response_text}, URL: {url}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе профиля игрока {name}: {type(e).__name__}: {e}, URL: {url}")
            return None
    
    def get_staff_stats(self) -> Optional[Dict]:
        url = f"{self.BASE_URL}/v1/staff/stats"
        
        try:
            logger.debug(f"Запрос статистики стаффа: {url}")
            response = self.session.get(url, timeout=10)
            logger.debug(f"Ответ API: статус {response.status_code}, URL: {url}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout as e:
            logger.error(f"Таймаут при запросе статистики стаффа: {e}, URL: {url}")
            return None
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Ошибка подключения при запросе статистики стаффа: {e}, URL: {url}")
            return None
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response is not None else 'unknown'
            response_text = e.response.text[:200] if e.response is not None else 'N/A'
            logger.error(f"HTTP ошибка при запросе статистики стаффа: статус {status_code}, ответ: {response_text}, URL: {url}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе статистики стаффа: {type(e).__name__}: {e}, URL: {url}")
            return None
    
    def get_staff_online(self) -> Optional[Dict]:
        url = f"{self.BASE_URL}/v1/staff/online"
        
        try:
            logger.debug(f"Запрос онлайн стаффа: {url}")
            response = self.session.get(url, timeout=10)
            logger.debug(f"Ответ API: статус {response.status_code}, URL: {url}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout as e:
            logger.error(f"Таймаут при запросе онлайн стаффа: {e}, URL: {url}")
            return None
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Ошибка подключения при запросе онлайн стаффа: {e}, URL: {url}")
            return None
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response is not None else 'unknown'
            response_text = e.response.text[:200] if e.response is not None else 'N/A'
            logger.error(f"HTTP ошибка при запросе онлайн стаффа: статус {status_code}, ответ: {response_text}, URL: {url}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе онлайн стаффа: {type(e).__name__}: {e}, URL: {url}")
            return None
    
    def get_total_online(self) -> Optional[Dict]:
        url = f"{self.BASE_URL}/v1/core/online/total"
        
        try:
            logger.debug(f"Запрос общего онлайн: {url}")
            response = self.session.get(url, timeout=10)
            logger.debug(f"Ответ API: статус {response.status_code}, URL: {url}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout as e:
            logger.error(f"Таймаут при запросе общего онлайн: {e}, URL: {url}")
            return None
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Ошибка подключения при запросе общего онлайн: {e}, URL: {url}")
            return None
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response is not None else 'unknown'
            response_text = e.response.text[:200] if e.response is not None else 'N/A'
            logger.error(f"HTTP ошибка при запросе общего онлайн: статус {status_code}, ответ: {response_text}, URL: {url}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе общего онлайн: {type(e).__name__}: {e}, URL: {url}")
            return None
    
    def test_connection(self) -> bool:
        url = f"{self.BASE_URL}/v1/test"
        
        try:
            logger.info(f"Проверка подключения к API: {url}")
            logger.debug(f"Заголовки запроса: {dict(self.session.headers)}")
            response = self.session.get(url, timeout=5)
            logger.info(f"Ответ от API: статус {response.status_code}, URL: {url}")
            
            if response.status_code == 200:
                logger.info("Соединение с API успешно установлено")
                return True
            else:
                logger.warning(f"API вернул неожиданный статус код: {response.status_code}, ответ: {response.text[:200]}")
                return False
        except requests.exceptions.Timeout as e:
            logger.error(f"Таймаут при проверке подключения к API: {e}, URL: {url}")
            return False
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Ошибка подключения к API: {e}, URL: {url}")
            logger.error(f"Проверьте, доступен ли сервер {self.BASE_URL} и есть ли интернет-соединение")
            return False
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP ошибка при проверке подключения: {e}, URL: {url}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Статус код: {e.response.status_code}, ответ: {e.response.text[:200]}")
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Неожиданная ошибка при проверке подключения к API: {type(e).__name__}: {e}, URL: {url}")
            return False