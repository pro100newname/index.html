DEFAULT_SETTINGS = {
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