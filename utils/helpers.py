import json
import os

def darken_color(color):
    """Затемнить цвет для hover эффекта"""
    if color.startswith("#"):
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        return f"#{max(0, r-30):02x}{max(0, g-30):02x}{max(0, b-30):02x}"
    return color

def load_settings():
    """Загрузка настроек"""
    default_settings = {
        'websites': [{'url': 'https://who-calls.ru', 'enabled': True}],
        'search_settings': {
            'enable_search': True,
            'search_speed': 'normal',
            'search_depth': 3,
            'search_type': 'standard'
        },
        'schedule': {
            'enabled': False,
            'start_time': '09:00',
            'end_time': '18:00',
            'days': [True, True, True, True, True, False, False],
            'daily_limit': 100,
            'enable_breaks': True,
            'break_duration': 5,
            'break_interval': 30
        },
        'ai_settings': {
            'enabled': True,
            'level': 'advanced',
            'learning': True,
            'learning_speed': 'normal',
            'optimizations': [True, True, True, True]
        }
    }
    
    try:
        if os.path.exists('settings.json'):
            with open('settings.json', 'r', encoding='utf-8') as f:
                loaded_settings = json.load(f)
                # Объединяем с настройками по умолчанию
                for key, value in loaded_settings.items():
                    if key in default_settings:
                        if isinstance(value, dict) and isinstance(default_settings[key], dict):
                            default_settings[key].update(value)
                        else:
                            default_settings[key] = value
                    else:
                        default_settings[key] = value
    except:
        pass
        
    return default_settings

def save_settings(settings):
    """Сохранение настроек"""
    try:
        with open('settings.json', 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        return False