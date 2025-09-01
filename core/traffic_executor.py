import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent

logger = logging.getLogger('WhoCallsUltimate')

class RealTrafficExecutor:
    def __init__(self):
        self.ua = UserAgent()
        self.driver = None
        self.current_proxy = None
        
    def create_stealth_browser(self, proxy=None):
        """Создание stealth-браузера с улучшенным анти-детектом"""
        try:
            chrome_options = Options()
            
            # Расширенный анти-детект - основные параметры
            stealth_params = [
                '--no-first-run',
                '--no-default-browser-check',
                '--disable-background-networking',
                '--disable-background-timer-throttling',
                '--disable-client-side-phishing-detection',
                '--disable-default-apps',
                '--disable-hang-monitor',
                '--disable-popup-blocking',
                '--disable-prompt-on-repost',
                '--disable-sync',
                '--disable-translate',
                '--metrics-recording-only',
                '--safebrowsing-disable-auto-update',
                '--password-store=basic',
                '--use-mock-keychain',
                '--hide-scrollbars',
                '--mute-audio',
                '--disable-web-security',
                '--allow-running-insecure-content',
                '--disable-webgl',
                '--disable-threaded-animation',
                '--disable-animations',
                '--disable-blink-features=AutomationControlled',
                '--disable-infobars',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-gpu',
            ]
            
            for param in stealth_params:
                chrome_options.add_argument(param)
            
            # Экспериментальные опции для скрытия автоматизации
            chrome_options.add_experimental_option("excludeSwitches", [
                "enable-automation",
                "enable-logging",
                "ignore-certificate-errors",
                "load-extension"
            ])
            
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Случайный User-Agent
            user_agent = self.ua.random
            chrome_options.add_argument(f'--user-agent={user_agent}')
            chrome_options.add_argument('--lang=ru-RU')
            chrome_options.add_argument('--accept-language=ru-RU,ru;q=0.9,en;q=0.8')
            
            # Прокси если есть
            if proxy:
                chrome_options.add_argument(f'--proxy-server={proxy}')
                self.current_proxy = proxy
            
            # Случайное разрешение экрана
            resolutions = [
                '1920x1080', '1366x768', '1536x864', 
                '1440x900', '1280x720', '1600x900',
                '1280x800', '1440x1080', '1680x1050'
            ]
            selected_resolution = random.choice(resolutions)
            chrome_options.add_argument(f'--window-size={selected_resolution}')
            
            # Дополнительные настройки для маскировки
            chrome_options.add_argument('--disable-features=VizDisplayCompositor')
            chrome_options.add_argument('--disable-software-rasterizer')
            
            # Headless режим (раскомментируйте если нужно)
            # chrome_options.add_argument('--headless=new')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # Скрытие WebDriver и маскировка под обычный браузер
            stealth_scripts = [
                # Скрытие webdriver
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})",
                
                # Маскировка под обычный Chrome
                "window.navigator.chrome = {runtime: {}, app: {}, webstore: {}};",
                
                # Языковые настройки
                "Object.defineProperty(navigator, 'languages', {get: () => ['ru-RU', 'ru', 'en-US', 'en']});",
                
                # Платформа
                "Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});",
                
                # Хаарктеристики hardware
                "Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});",
                
                # Память
                "Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});",
                
                # Максимальное количество touch точек
                "Object.defineProperty(navigator, 'maxTouchPoints', {get: () => 0});",
            ]
            
            for script in stealth_scripts:
                try:
                    self.driver.execute_script(script)
                except Exception as e:
                    logger.debug(f"Ошибка выполнения stealth скрипта: {e}")
                    continue
            
            # Дополнительные методы скрытия
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                '''
            })
            
            # Установка случайного времени зоны
            timezone_offset = random.randint(-720, 840)  # от -12 до +14 часов
            self.driver.execute_cdp_cmd('Emulation.setTimezoneOverride', {
                'timezoneId': 'Europe/Moscow'
            })
            
            # Случайные геолокационные координаты (примерно Москва)
            self.driver.execute_cdp_cmd('Emulation.setGeolocationOverride', {
                'latitude': 55.7558 + random.uniform(-0.1, 0.1),
                'longitude': 37.6173 + random.uniform(-0.1, 0.1),
                'accuracy': 100
            })
            
            logger.info(f"Stealth браузер создан: {selected_resolution}, User-Agent: {user_agent[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка создания stealth-браузера: {e}")
            return False
    
    def human_like_delay(self):
        """Человеческая задержка между действиями"""
        delay = random.uniform(0.8, 2.5)
        time.sleep(delay)
        return delay
    
    def human_like_typing(self, element, text):
        """Человеческий ввод текста"""
        try:
            element.clear()
            for char in text:
                element.send_keys(char)
                # Случайная задержка между символами
                time.sleep(random.uniform(0.08, 0.3))
                # Случайная пауза после некоторых символов
                if random.random() < 0.1:
                    time.sleep(random.uniform(0.2, 0.5))
            return True
        except Exception as e:
            logger.error(f"Ошибка человеческого ввода: {e}")
            return False
    
    def random_mouse_movement(self):
        """Случайное движение мышью"""
        try:
            if random.random() > 0.7:  # 30% chance
                # Случайное движение курсором
                action = ActionChains(self.driver)
                x_offset = random.randint(-100, 100)
                y_offset = random.randint(-100, 100)
                action.move_by_offset(x_offset, y_offset).perform()
                time.sleep(random.uniform(0.1, 0.5))
                action.move_by_offset(-x_offset, -y_offset).perform()
        except:
            pass
    
    def real_navigation(self, url, actions=3):
        """Реальная навигация по сайту с улучшенным анти-детектом"""
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Случайная начальная задержка
            time.sleep(random.uniform(2, 4))
            
            # Случайное движение мышью
            self.random_mouse_movement()
            
            # Получаем все ссылки на странице
            links = self.driver.find_elements(By.TAG_NAME, "a")
            valid_links = [link for link in links if link.get_attribute('href') and 'http' in link.get_attribute('href')]
            
            if valid_links:
                # Кликаем на случайные ссылки
                for _ in range(min(actions, len(valid_links))):
                    try:
                        link = random.choice(valid_links)
                        
                        # Прокрутка к элементу перед кликом
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
                        self.human_like_delay()
                        
                        # Клик с человеческой задержкой
                        ActionChains(self.driver).move_to_element(link).pause(
                            random.uniform(0.5, 1.5)
                        ).click().perform()
                        
                        time.sleep(random.uniform(3, 8))
                        
                        # Случайный скроллинг
                        if random.random() > 0.3:
                            scroll_amount = random.randint(300, 1500)
                            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                            self.human_like_delay()
                            
                            # Дополнительный микро-скроллинг
                            if random.random() > 0.5:
                                self.driver.execute_script(f"window.scrollBy(0, {random.randint(-100, 100)});")
                                time.sleep(random.uniform(0.5, 1.5))
                        
                        # Возврат назад или продолжение
                        if random.random() > 0.5:
                            self.driver.back()
                            time.sleep(random.uniform(2, 4))
                            
                    except Exception as e:
                        logger.debug(f"Ошибка при клике на ссылку: {e}")
                        continue
            
            return True
            
        except Exception as e:
            logger.error(f"Ошибка навигации: {e}")
            return False
    
    def real_search(self, website_url, phone_number):
        """Реальный поиск на сайте с улучшенным анти-детектом"""
        try:
            self.driver.get(website_url)
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            time.sleep(random.uniform(2, 4))
            
            # Поиск поля ввода
            search_selectors = [
                "input[type='tel']", "input[type='text']", 
                "input[name='phone']", "input[name='number']",
                ".search-input", "#search", "input[placeholder*='номер']",
                "input[placeholder*='телефон']", "input[placeholder*='phone']",
                "input[type='search']", ".form-control", "input.search"
            ]
            
            for selector in search_selectors:
                try:
                    search_input = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    
                    # Человеческий ввод с улучшенной реалистичностью
                    self.human_like_typing(search_input, phone_number)
                    
                    time.sleep(random.uniform(1, 2))
                    
                    # Поиск кнопки
                    button_selectors = [
                        "button[type='submit']", ".search-btn", "#search-btn",
                        "input[type='submit']", "button.search", ".btn-primary",
                        "button.btn", ".submit-btn"
                    ]
                    
                    for btn_selector in button_selectors:
                        try:
                            search_btn = self.driver.find_element(By.CSS_SELECTOR, btn_selector)
                            # Человеческий клик
                            ActionChains(self.driver).move_to_element(search_btn).pause(
                                random.uniform(0.5, 1.5)
                            ).click().perform()
                            
                            time.sleep(random.uniform(3, 6))
                            return True
                        except:
                            continue
                    
                    # Если кнопка не найдена, имитируем Enter
                    search_input.send_keys(Keys.ENTER)
                    time.sleep(random.uniform(3, 6))
                    return True
                    
                except:
                    continue
            
            # Если поле поиска не найдено, просто остаемся на странице
            return True
            
        except Exception as e:
            logger.error(f"Ошибка реального поиска: {e}")
            return False
    
    def click_ads(self):
        """Клики по рекламе с улучшенным анти-детектом"""
        ad_selectors = [
            "div[data-banner-id]", "a[href*='yandex']", "div.banner",
            "ins.adsbygoogle", "div[class*='adv']", "div[class*='ad']",
            "iframe[src*='ads']", "div[id*='ad']", "div[class*='banner']",
            "a[href*='click']", "div[data-ad]", ".ad-container",
            ".advertisement", "[class*='adsense']", ".google-ad"
        ]
        
        clicks_made = 0
        max_clicks = random.randint(1, 3)
        
        for selector in ad_selectors:
            if clicks_made >= max_clicks:
                break
                
            try:
                ads = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if ads:
                    ad = random.choice(ads)
                    
                    # Прокрутка к баннеру
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ad)
                    time.sleep(random.uniform(1, 2))
                    
                    # Человеческий клик
                    ActionChains(self.driver).move_to_element(ad).pause(
                        random.uniform(0.5, 1.5)
                    ).click().perform()
                    
                    clicks_made += 1
                    
                    # Время на рекламной странице
                    ad_time = random.randint(5, 15)
                    time.sleep(ad_time)
                    
                    # Возврат назад
                    self.driver.back()
                    time.sleep(random.uniform(2, 4))
                    
            except Exception as e:
                logger.debug(f"Ошибка клика по рекламе: {e}")
                continue
                
        return clicks_made
    
    def close(self):
        """Закрытие браузера"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass