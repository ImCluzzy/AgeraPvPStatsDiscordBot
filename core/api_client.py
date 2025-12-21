import requests
from typing import Dict, Optional


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
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return None
    
    def get_player_profile(self, name: str) -> Optional[Dict]:
        url = f"{self.BASE_URL}/v1/player/profile/{name}"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе профиля к API: {e}")
            return None
    
    def get_staff_stats(self) -> Optional[Dict]:
        url = f"{self.BASE_URL}/v1/staff/stats"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе статистики стаффа к API: {e}")
            return None
    
    def get_staff_online(self) -> Optional[Dict]:
        url = f"{self.BASE_URL}/v1/staff/online"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе онлайн стаффа к API: {e}")
            return None
    
    def get_total_online(self) -> Optional[Dict]:
        url = f"{self.BASE_URL}/v1/core/online/total"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе общего онлайн к API: {e}")
            return None
    
    def test_connection(self) -> bool:
        url = f"{self.BASE_URL}/v1/test"
        
        try:
            response = self.session.get(url, timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False