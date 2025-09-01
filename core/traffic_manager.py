import random
import os
from datetime import datetime
from .ai_core import WhoCallsAICore
from .traffic_executor import RealTrafficExecutor

class UltimateTrafficManager:
    def __init__(self):
        self.ai_core = WhoCallsAICore()
        self.traffic_executor = RealTrafficExecutor()
        self.stats = {
            'total_sessions': 0,
            'successful_sessions': 0,
            'total_income': 0,
            'daily_stats': {},
            'city_stats': {},
            'proxy_usage': 0,
            'ai_optimizations': 0,
            'real_clicks': 0,
            'sessions_today': 0
        }
        self.phone_database = []
        self.proxy_list = self._load_proxies()
        self.last_session_date = datetime.now().date()
        
    def _load_proxies(self):
        """Загрузка прокси из файла"""
        proxies = []
        if os.path.exists('proxies.txt'):
            try:
                with open('proxies.txt', 'r', encoding='utf-8') as f:
                    proxies = [line.strip() for line in f if line.strip()]
            except:
                pass
        return proxies
        
    def generate_advanced_phone(self):
        """Продвинутая генерация номеров с привязкой к региону"""
        regions = {
            'Москва': ['495', '499', '498'],
            'СПб': ['812', '813', '814'],
            'Новосибирск': ['383'],
            'Екатеринбург': ['343', '347'],
            'Казань': ['843', '855'],
            'Нижний Новгород': ['831'],
            'Краснодар': ['861', '862'],
            'Уфа': ['347', '349'],
            'Воронеж': ['473', '474'],
            'Ростов-на-Дону': ['863']
        }
        
        city = random.choice(list(regions.keys()))
        code = random.choice(regions[city])
        
        if random.random() > 0.3:  # Мобильные
            operators = ['900', '901', '902', '903', '904', '905', '906', '908', '909',
                        '910', '911', '912', '913', '914', '915', '916', '917', '918', '919',
                        '920', '921', '922', '923', '924', '925', '926', '927', '928', '929',
                        '930', '931', '932', '933', '934', '935', '936', '937', '938', '939']
            number = f"+7{random.choice(operators)}{random.randint(1000000, 9999999)}"
        else:  # Городские
            number = f"+7{code}{random.randint(1000000, 9999999)}"
            
        return number, city