import customtkinter as ctk
from tkinter import messagebox, filedialog
import threading
import time
import random
import json
import os
import sqlite3
import logging
from datetime import datetime

from core.traffic_manager import UltimateTrafficManager
from core.database import DatabaseManager
from utils.constants import OBS_COLORS, CATEGORIES, CATEGORY_TITLES
from utils.helpers import load_settings, save_settings

# Импорт всех категорий
from ui.categories.main_category import MainCategory
from ui.categories.websites_category import WebsitesCategory
from ui.categories.phones_category import PhonesCategory
from ui.categories.search_category import SearchCategory
from ui.categories.schedule_category import ScheduleCategory
from ui.categories.ai_category import AICategory
from ui.categories.proxy_category import ProxyCategory
from ui.categories.behavior_category import BehaviorCategory
from ui.categories.security_category import SecurityCategory
from ui.categories.performance_category import PerformanceCategory
from ui.categories.stats_category import StatsCategory
from ui.categories.general_category import GeneralCategory

logger = logging.getLogger('WhoCallsUltimate')

class OBSLikeInterface(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("WhoCalls ULTIMATE Suite v6.0 ★ OBS Style")
        self.geometry("1400x800")
        self.minsize(1200, 700)
        
        # Цветовая схема в стиле OBS
        self.obs_colors = OBS_COLORS
        
        ctk.set_appearance_mode("Dark")
        
        self.traffic_manager = UltimateTrafficManager()
        self.db_manager = DatabaseManager()
        self.is_running = False
        self.current_day = datetime.now().strftime("%Y-%m-%d")
        self.settings = self.load_settings()
        self.current_tab = None
        
        self.setup_obs_layout()
        self.setup_database()
        self.load_initial_data()
        
    def setup_obs_layout(self):
        """Интерфейс в стиле OBS Studio"""
        # Main grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Левая панель с категориями (как в OBS)
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=self.obs_colors["sidebar"])
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(12, weight=1)
        
        # Логотип
        self.logo_label = ctk.CTkLabel(
            self.sidebar, 
            text="WhoCalls ULTIMATE",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.obs_colors["accent"]
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 15))
        
        # Разделитель
        separator = ctk.CTkFrame(self.sidebar, height=2, fg_color="#444444")
        separator.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        
        # Категории настроек (как в OBS)
        self.category_buttons = {}
        for i, (text, category) in enumerate(CATEGORIES, 2):
            btn = ctk.CTkButton(
                self.sidebar, 
                text=text, 
                command=lambda c=category: self.show_category(c),
                fg_color="transparent",
                hover_color="#333333",
                anchor="w",
                text_color=self.obs_colors["text"],
                font=ctk.CTkFont(size=13)
            )
            btn.grid(row=i, column=0, padx=10, pady=2, sticky="ew")
            self.category_buttons[category] = btn
        
        # Кнопка запуска/остановки внизу
        self.start_stop_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.start_stop_frame.grid(row=13, column=0, sticky="ew", padx=10, pady=10)
        
        self.start_btn = ctk.CTkButton(
            self.start_stop_frame,
            text="🚀 Запуск",
            command=self.start_all,
            fg_color=self.obs_colors["success"],
            hover_color="#3D8C40",
            height=40
        )
        self.start_btn.pack(fill="x", pady=5)
        
        self.stop_btn = ctk.CTkButton(
            self.start_stop_frame,
            text="⏹️ Стоп",
            command=self.stop_all,
            fg_color=self.obs_colors["danger"],
            hover_color="#C13535",
            height=40
        )
        self.stop_btn.pack(fill="x", pady=5)
        
        # Правая панель с настройками
        self.settings_frame = ctk.CTkFrame(self, fg_color=self.obs_colors["background"])
        self.settings_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.settings_frame.grid_columnconfigure(0, weight=1)
        self.settings_frame.grid_rowconfigure(1, weight=1)
        
        # Заголовок текущей категории
        self.category_title = ctk.CTkLabel(
            self.settings_frame,
            text="Главная панель",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.obs_colors["accent"]
        )
        self.category_title.grid(row=0, column=0, sticky="w", padx=20, pady=15)
        
        # Контейнер для содержимого категории
        self.content_frame = ctk.CTkScrollableFrame(self.settings_frame, fg_color=self.obs_colors["background"])
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Статус бар внизу
        self.status_bar = ctk.CTkFrame(self, height=30, fg_color=self.obs_colors["sidebar"])
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")
        
        self.status_label = ctk.CTkLabel(
            self.status_bar, 
            text="Готов к работе",
            text_color=self.obs_colors["success"],
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side="left", padx=10)
        
        # Показываем главную категорию по умолчанию
        self.show_category("main")
        
    def show_category(self, category):
        """Показать выбранную категорию настроек"""
        # Сбрасываем выделение всех кнопок
        for btn in self.category_buttons.values():
            btn.configure(fg_color="transparent")
        
        # Выделяем активную кнопку
        self.category_buttons[category].configure(fg_color="#333333")
        
        # Очищаем контент
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Устанавливаем заголовок
        self.category_title.configure(text=CATEGORY_TITLES.get(category, "Настройки"))
        
        # Загружаем содержимое категории
        if category == "main":
            main_cat = MainCategory(self, self.content_frame, self.obs_colors, self.traffic_manager, self.db_manager)
            main_cat.setup()
        elif category == "websites":
            websites_cat = WebsitesCategory(self, self.content_frame, self.obs_colors, self.traffic_manager, self.db_manager)
            websites_cat.setup()
        elif category == "phones":
            phones_cat = PhonesCategory(self, self.content_frame, self.obs_colors, self.traffic_manager, self.db_manager)
            phones_cat.setup()
        elif category == "search":
            search_cat = SearchCategory(self, self.content_frame, self.obs_colors, self.traffic_manager, self.db_manager)
            search_cat.setup()
        elif category == "schedule":
            schedule_cat = ScheduleCategory(self, self.content_frame, self.obs_colors, self.traffic_manager, self.db_manager)
            schedule_cat.setup()
        elif category == "ai":
            ai_cat = AICategory(self, self.content_frame, self.obs_colors, self.traffic_manager, self.db_manager)
            ai_cat.setup()
        elif category == "proxy":
            proxy_cat = ProxyCategory(self, self.content_frame, self.obs_colors, self.traffic_manager, self.db_manager)
            proxy_cat.setup()
        elif category == "behavior":
            behavior_cat = BehaviorCategory(self, self.content_frame, self.obs_colors, self.traffic_manager, self.db_manager)
            behavior_cat.setup()
        elif category == "security":
            security_cat = SecurityCategory(self, self.content_frame, self.obs_colors, self.traffic_manager, self.db_manager)
            security_cat.setup()
        elif category == "performance":
            performance_cat = PerformanceCategory(self, self.content_frame, self.obs_colors, self.traffic_manager, self.db_manager)
            performance_cat.setup()
        elif category == "stats":
            stats_cat = StatsCategory(self, self.content_frame, self.obs_colors, self.traffic_manager, self.db_manager)
            stats_cat.setup()
        elif category == "general":
            general_cat = GeneralCategory(self, self.content_frame, self.obs_colors, self.traffic_manager, self.db_manager)
            general_cat.setup()
        
        self.current_tab = category

    def setup_database(self):
        """Настройка базы данных"""
        try:
            if not self.db_manager.connect():
                raise Exception("Не удалось подключиться к базе данных")
            
            if not self.db_manager.setup_tables():
                raise Exception("Не удалось создать таблицы")
            
        except Exception as e:
            logger.error(f"Ошибка базы данных: {e}")
            messagebox.showerror("Ошибка", f"Ошибка базы данных: {e}")

    def load_settings(self):
        """Загрузка настроек"""
        default_settings = {
            'websites': [{'url': 'https://who-calls.ru', 'enabled': True}],
            'click_ads': True,  # ДОБАВЬТЕ ЭТУ СТРОКУ
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

    def save_settings(self):
        """Сохранение настроек"""
        try:
            with open('settings.json', 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f"Ошибка сохранения настроек: {e}")
            return False

    def load_initial_data(self):
        """Загрузка начальных данных"""
        # Загрузка номеров из базы
        try:
            self.db_manager.cursor.execute("SELECT COUNT(*) FROM phones")
            count = self.db_manager.cursor.fetchone()[0]
            if hasattr(self, 'total_phones_var'):
                self.total_phones_var.set(f"{count} номеров")
        except:
            if hasattr(self, 'total_phones_var'):
                self.total_phones_var.set("0 номеров")

    def update_main_stats(self):
        """Обновление главной статистики"""
        try:
            # Обновляем счетчик сессий сегодня
            today = datetime.now().strftime("%Y-%m-%d")
            self.db_manager.cursor.execute("SELECT COUNT(*) FROM sessions WHERE date(timestamp) = ?", (today,))
            sessions_today = self.db_manager.cursor.fetchone()[0]
            self.sessions_today_var.set(str(sessions_today))
            
            # Общая статистика
            self.db_manager.cursor.execute("SELECT COUNT(*) FROM sessions")
            total_sessions = self.db_manager.cursor.fetchone()[0]
            self.total_sessions_var.set(str(total_sessions))
            
            self.db_manager.cursor.execute("SELECT COUNT(*) FROM sessions WHERE success = 1")
            success_sessions = self.db_manager.cursor.fetchone()[0]
            self.success_sessions_var.set(str(success_sessions))
            
            self.db_manager.cursor.execute("SELECT SUM(income) FROM sessions")
            total_income = self.db_manager.cursor.fetchone()[0] or 0
            self.total_income_var.set(f"{total_income:.2f} руб")
            
            # Обновляем статус системы
            if self.is_running:
                self.system_status_var.set("Работает")
            else:
                self.system_status_var.set("Остановлено")
                
        except Exception as e:
            logger.error(f"Ошибка обновления статистики: {e}")

    def update_phones_stats(self):
        """Обновление статистики номеров"""
        try:
            self.db_manager.cursor.execute("SELECT COUNT(*) FROM phones")
            total = self.db_manager.cursor.fetchone()[0]
            self.total_phones_var.set(str(total))
            
            self.db_manager.cursor.execute("SELECT COUNT(*) FROM phones WHERE used = 1")
            used = self.db_manager.cursor.fetchone()[0]
            self.used_phones_var.set(str(used))
            
            self.db_manager.cursor.execute("SELECT MAX(last_used) FROM phones")
            last_update = self.db_manager.cursor.fetchone()[0] or "Никогда"
            self.last_update_var.set(str(last_update))
            
        except Exception as e:
            logger.error(f"Ошибка обновления статистики номеров: {e}")

    def start_all(self):
        """Запуск всех процессов"""
        if not self.is_running:
            self.is_running = True
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            self.status_label.configure(text="Работает", text_color=self.obs_colors["success"])
            self.system_status_var.set("Работает")
            
            # Запуск в отдельном потоке
            threading.Thread(target=self.run_traffic, daemon=True).start()
            
            logger.info("Система запущена")

    def stop_all(self):
        """Остановка всех процессов"""
        if self.is_running:
            self.is_running = False
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
            self.status_label.configure(text="Остановлено", text_color=self.obs_colors["danger"])
            self.system_status_var.set("Остановлено")
            
            logger.info("Система остановлена")

    def run_traffic(self):
        """Основной цикл трафика"""
        while self.is_running:
            try:
                # Проверяем суточный лимит
                today = datetime.now().strftime("%Y-%m-%d")
                self.db_manager.cursor.execute("SELECT COUNT(*) FROM sessions WHERE date(timestamp) = ?", (today,))
                sessions_today = self.db_manager.cursor.fetchone()[0]
                
                if sessions_today >= self.settings['schedule']['daily_limit']:
                    logger.info(f"Достигнут суточный лимит сессий: {sessions_today}")
                    time.sleep(60)
                    continue
                
                # Генерация номера
                phone, city = self.traffic_manager.generate_advanced_phone()
                
                # Выбор сайта
                website = random.choice(self.settings['websites'])['url']
                
                # Запуск сессии
                success = self.run_session(website, phone)
                
                # Сохранение в базу
                timestamp = datetime.now().isoformat()
                income = random.uniform(0.5, 2.5) if success else 0
                
                self.db_manager.cursor.execute(
                    "INSERT INTO sessions (timestamp, website, phone, success, duration, income) VALUES (?, ?, ?, ?, ?, ?)",
                    (timestamp, website, phone, success, random.uniform(10, 60), income)
                )
                
                # Обновление статистики номера
                self.db_manager.cursor.execute(
                    "INSERT OR IGNORE INTO phones (number, city) VALUES (?, ?)",
                    (phone, city)
                )
                self.db_manager.cursor.execute(
                    "UPDATE phones SET used = 1, last_used = ? WHERE number = ?",
                    (timestamp, phone)
                )
                
                self.db_manager.conn.commit()
                
                # Обновляем UI
                self.after(0, self.update_main_stats)
                
                # Пауза между сессиями
                time.sleep(random.uniform(5, 15))
                
            except Exception as e:
                logger.error(f"Ошибка в основном цикле: {e}")
                time.sleep(10)

    def run_session(self, website, phone):
        """Запуск одной сессии"""
        try:
            # Создание браузера
            proxy = random.choice(self.traffic_manager.proxy_list) if self.traffic_manager.proxy_list else None
            if not self.traffic_manager.traffic_executor.create_stealth_browser(proxy):
                return False
            
            # Навигация
            success = self.traffic_manager.traffic_executor.real_navigation(website)
            if not success:
                return False
            
            # Поиск
            if self.settings['search_settings']['enable_search']:
                search_success = self.traffic_manager.traffic_executor.real_search(website, phone)
                if not search_success:
                    return False
            
            # Клики по рекламе
            if hasattr(self, 'enable_ads_var') and self.enable_ads_var.get():
                self.traffic_manager.traffic_executor.click_ads()
            
            # Закрытие браузера
            self.traffic_manager.traffic_executor.close()
            
            return True
            
        except Exception as e:
            logger.error(f"Ошибка сессии: {e}")
            return False

    def generate_phones(self):
        """Генерация номеров телефонов"""
        try:
            count = 1000  # Генерируем 1000 номеров
            new_phones = []
            
            for _ in range(count):
                phone, city = self.traffic_manager.generate_advanced_phone()
                new_phones.append((phone, city))
            
            # Сохранение в базу
            self.db_manager.cursor.executemany(
                "INSERT OR IGNORE INTO phones (number, city) VALUES (?, ?)",
                new_phones
            )
            self.db_manager.conn.commit()
            
            messagebox.showinfo("Успех", f"Сгенерировано {count} номеров")
            self.update_phones_stats()
            
        except Exception as e:
            logger.error(f"Ошибка генерации номеров: {e}")
            messagebox.showerror("Ошибка", f"Ошибка генерации: {e}")

    def generate_report(self):
        """Генерация отчета"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            
            self.db_manager.cursor.execute("""
                SELECT COUNT(*), SUM(success), SUM(income), AVG(duration)
                FROM sessions 
                WHERE date(timestamp) = ?
            """, (today,))
            
            result = self.db_manager.cursor.fetchone()
            total, success, income, avg_duration = result
            
            report = f"""
📊 ОТЧЕТ ЗА {today}
────────────────
Всего сессий: {total or 0}
Успешных: {success or 0}
Успешность: {(success/total*100 if total else 0):.1f}%
Доход: {income or 0:.2f} руб
Среднее время: {avg_duration or 0:.1f} сек
            """
            
            messagebox.showinfo("Отчет", report)
            
        except Exception as e:
            logger.error(f"Ошибка генерации отчета: {e}")
            messagebox.showerror("Ошибка", f"Ошибка генерации отчета: {e}")

    def refresh_all(self):
        """Обновление всех данных"""
        self.update_main_stats()
        self.update_phones_stats()
        self.status_label.configure(text="Данные обновлены", text_color=self.obs_colors["success"])
        self.after(2000, lambda: self.status_label.configure(text="Готов к работе", text_color=self.obs_colors["success"]))

    def save_all_settings(self):
        """Сохранение всех настроек"""
        self.save_websites_settings()
        self.save_search_settings()
        self.save_schedule_settings()
        self.save_ai_settings()
        self.save_settings()
        
        self.status_label.configure(text="Настройки сохранены", text_color=self.obs_colors["success"])
        self.after(2000, lambda: self.status_label.configure(text="Готов к работе", text_color=self.obs_colors["success"]))

    def save_websites_settings(self):
        """Сохранение настроек сайтов"""
        try:
            main_site = self.main_site_var.get().strip()
            if not main_site:
                messagebox.showerror("Ошибка", "Основной сайт не может быть пустым")
                return
            
            extra_sites = self.extra_sites_text.get("1.0", "end-1c").strip().split('\n')
            extra_sites = [site.strip() for site in extra_sites if site.strip()]
            
            self.settings['websites'] = [{'url': main_site, 'enabled': True}]
            for site in extra_sites:
                self.settings['websites'].append({'url': site, 'enabled': True})
                # СОХРАНЕНИЕ НАСТРОЙКИ РЕКЛАМЫ (ДОБАВЬТЕ ЭТУ СТРОКУ)
            self.settings['click_ads'] = self.enable_ads_var.get()
            
            messagebox.showinfo("Успех", "Настройки сайтов сохранены")
            
        except Exception as e:
            logger.error(f"Ошибка сохранения сайтов: {e}")
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {e}")

    def save_search_settings(self):
        """Сохранение настроек поиска"""
        try:
            self.settings['search_settings'] = {
                'enable_search': self.enable_search_var.get(),
                'search_speed': self.search_speed_var.get(),
                'search_depth': self.search_depth_var.get(),
                'search_type': self.search_type_var.get()
            }
            
            messagebox.showinfo("Успех", "Настройки поиска сохранены")
            
        except Exception as e:
            logger.error(f"Ошибка сохранения поиска: {e}")
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {e}")

    def save_schedule_settings(self):
        """Сохранение настроек расписания"""
        try:
            self.settings['schedule'] = {
                'enabled': self.enable_schedule_var.get(),
                'start_time': self.start_time_var.get(),
                'end_time': self.end_time_var.get(),
                'days': [var.get() for var in self.days_vars],
                'daily_limit': self.daily_limit_var.get(),
                'enable_breaks': self.enable_breaks_var.get(),
                'break_duration': self.break_duration_var.get(),
                'break_interval': self.break_interval_var.get()
            }
            
            messagebox.showinfo("Успех", "Настройки расписания сохранены")
            
        except Exception as e:
            logger.error(f"Ошибка сохранения расписания: {e}")
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {e}")

    def save_ai_settings(self):
        """Сохранение настроек ИИ"""
        try:
            self.settings['ai_settings'] = {
                'enabled': self.enable_ai_var.get(),
                'level': self.ai_level_var.get(),
                'learning': self.enable_learning_var.get(),
                'learning_speed': self.learning_speed_var.get(),
                'optimizations': [var.get() for var in self.optimization_vars]
            }
            
            messagebox.showinfo("Успех", "Настройки ИИ сохранены")
            
        except Exception as e:
            logger.error(f"Ошибка сохранения ИИ: {e}")
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {e}")

    def import_phones(self):
        """Импорт номеров из файла"""
        try:
            file_path = filedialog.askopenfilename(
                title="Выберите файл с номерами",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as f:
                    phones = [line.strip() for line in f if line.strip()]
                
                # Сохранение в базу
                phone_data = [(phone, "Неизвестно") for phone in phones]
                self.db_manager.cursor.executemany(
                    "INSERT OR IGNORE INTO phones (number, city) VALUES (?, ?)",
                    phone_data
                )
                self.db_manager.conn.commit()
                
                messagebox.showinfo("Успех", f"Импортировано {len(phones)} номеров")
                self.update_phones_stats()
                
        except Exception as e:
            logger.error(f"Ошибка импорта номеров: {e}")
            messagebox.showerror("Ошибка", f"Ошибка импорта: {e}")

    def export_phones(self):
        """Экспорт номеров в файл"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Сохранить номера",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if file_path:
                self.db_manager.cursor.execute("SELECT number FROM phones")
                phones = [row[0] for row in self.db_manager.cursor.fetchall()]
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(phones))
                
                messagebox.showinfo("Успех", f"Экспортировано {len(phones)} номеров")
                
        except Exception as e:
            logger.error(f"Ошибка экспорта номеров: {e}")
            messagebox.showerror("Ошибка", f"Ошибка экспорта: {e}")

    def clear_phones(self):
        """Очистка базы номеров"""
        if messagebox.askyesno("Подтверждение", "Очистить всю базу номеров?"):
            try:
                self.db_manager.cursor.execute("DELETE FROM phones")
                self.db_manager.conn.commit()
                
                messagebox.showinfo("Успех", "База номеров очищена")
                self.update_phones_stats()
                
            except Exception as e:
                logger.error(f"Ошибка очистки номеров: {e}")
                messagebox.showerror("Ошибка", f"Ошибка очистки: {e}")

    def import_proxies(self):
        """Импорт прокси из файла"""
        try:
            file_path = filedialog.askopenfilename(
                title="Выберите файл с прокси",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as f:
                    proxies = [line.strip() for line in f if line.strip()]
                
                self.proxy_text.delete("1.0", "end")
                self.proxy_text.insert("1.0", '\n'.join(proxies))
                
                messagebox.showinfo("Успех", f"Импортировано {len(proxies)} прокси")
                
        except Exception as e:
            logger.error(f"Ошибка импорта прокси: {e}")
            messagebox.showerror("Ошибка", f"Ошибка импорта: {e}")

    def save_proxies(self):
        """Сохранение прокси в файл"""
        try:
            proxies = self.proxy_text.get("1.0", "end-1c").strip().split('\n')
            proxies = [proxy.strip() for proxy in proxies if proxy.strip()]
            
            with open('proxies.txt', 'w', encoding='utf-8') as f:
                f.write('\n'.join(proxies))
            
            # Обновляем список в менеджере
            self.traffic_manager.proxy_list = proxies
            
            messagebox.showinfo("Успех", f"Сохранено {len(proxies)} прокси")
            
        except Exception as e:
            logger.error(f"Ошибка сохранения прокси: {e}")
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {e}")

    def clear_proxies(self):
        """Очистка списка прокси"""
        if messagebox.askyesno("Подтверждение", "Очистить список прокси?"):
            self.proxy_text.delete("1.0", "end")
            messagebox.showinfo("Успех", "Список прокси очищен")

    def test_proxies(self):
        """Тестирование прокси"""
        messagebox.showinfo("Инфо", "Тестирование прокси будет реализовано в следующей версии")

    def generate_daily_report(self):
        """Генерация ежедневного отчета"""
        self.generate_report()

    def generate_weekly_report(self):
        """Генерация недельного отчета"""
        messagebox.showinfo("Инфо", "Недельный отчет будет реализован в следующей версии")

    def generate_monthly_report(self):
        """Генерация месячного отчета"""
        messagebox.showinfo("Инфо", "Месячный отчет будет реализован в следующей версии")

    def export_to_excel(self):
        """Экспорт в Excel"""
        messagebox.showinfo("Инфо", "Экспорт в Excel будет реализован в следующей версии")

    def create_backup(self):
        """Создание backup"""
        try:
            backup_data = {
                'settings': self.settings,
                'phones': [],
                'sessions': []
            }
            
            # Сохранение номеров
            self.db_manager.cursor.execute("SELECT number, city, used, last_used FROM phones")
            backup_data['phones'] = self.db_manager.cursor.fetchall()
            
            # Сохранение сессий
            self.db_manager.cursor.execute("SELECT timestamp, website, phone, success, duration, income FROM sessions")
            backup_data['sessions'] = self.db_manager.cursor.fetchall()
            
            file_path = filedialog.asksaveasfilename(
                title="Сохранить backup",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(backup_data, f, ensure_ascii=False, indent=2)
                
                messagebox.showinfo("Успех", "Backup создан успешно")
                
        except Exception as e:
            logger.error(f"Ошибка создания backup: {e}")
            messagebox.showerror("Ошибка", f"Ошибка создания backup: {e}")

    def restore_backup(self):
        """Восстановление из backup"""
        try:
            file_path = filedialog.askopenfilename(
                title="Выберите backup файл",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as f:
                    backup_data = json.load(f)
                
                # Восстановление настроек
                if 'settings' in backup_data:
                    self.settings = backup_data['settings']
                    self.save_settings()
                
                # Восстановление номеров
                if 'phones' in backup_data:
                    self.db_manager.cursor.execute("DELETE FROM phones")
                    self.db_manager.cursor.executemany(
                        "INSERT INTO phones (number, city, used, last_used) VALUES (?, ?, ?, ?)",
                        backup_data['phones']
                    )
                
                # Восстановление сессий
                if 'sessions' in backup_data:
                    self.db_manager.cursor.execute("DELETE FROM sessions")
                    self.db_manager.cursor.executemany(
                        "INSERT INTO sessions (timestamp, website, phone, success, duration, income) VALUES (?, ?, ?, ?, ?, ?)",
                        backup_data['sessions']
                    )
                
                self.db_manager.conn.commit()
                
                messagebox.showinfo("Успех", "Backup восстановлен успешно")
                self.update_main_stats()
                self.update_phones_stats()
                
        except Exception as e:
            logger.error(f"Ошибка восстановления backup: {e}")
            messagebox.showerror("Ошибка", f"Ошибка восстановления backup: {e}")

    def export_settings(self):
        """Экспорт настроек"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Экспорт настроек",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.settings, f, ensure_ascii=False, indent=2)
                
                messagebox.showinfo("Успех", "Настройки экспортированы")
                
        except Exception as e:
            logger.error(f"Ошибка экспорта настроек: {e}")
            messagebox.showerror("Ошибка", f"Ошибка экспорта: {e}")

    def import_settings(self):
        """Импорт настроек"""
        try:
            file_path = filedialog.askopenfilename(
                title="Импорт настроек",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as f:
                    imported_settings = json.load(f)
                
                self.settings = imported_settings
                self.save_settings()
                
                messagebox.showinfo("Успех", "Настройки импортированы")
                
        except Exception as e:
            logger.error(f"Ошибка импорта настроек: {e}")
            messagebox.showerror("Ошибка", f"Ошибка импорта: {e}")

    def reset_settings(self):
        """Сброс настроек"""
        if messagebox.askyesno("Подтверждение", "Сбросить все настройки к значениям по умолчанию?"):
            try:
                # Удаляем файлы настроек
                if os.path.exists('settings.json'):
                    os.remove('settings.json')
                
                if os.path.exists('proxies.txt'):
                    os.remove('proxies.txt')
                
                # Перезагружаем настройки
                self.settings = self.load_settings()
                
                messagebox.showinfo("Успех", "Настройки сброшены")
                
            except Exception as e:
                logger.error(f"Ошибка сброса настроек: {e}")
                messagebox.showerror("Ошибка", f"Ошибка сброса: {e}")

    def darken_color(self, color):
        """Затемнить цвет для hover эффекта"""
        if color.startswith("#"):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            return f"#{max(0, r-30):02x}{max(0, g-30):02x}{max(0, b-30):02x}"
        return color

    def on_closing(self):
        """Обработчик закрытия приложения"""
        try:
            self.is_running = False
            self.save_settings()
            if hasattr(self, 'db_manager') and self.db_manager:
                self.db_manager.close()
            self.destroy()
        except Exception as e:
            logger.error(f"Ошибка при закрытии: {e}")
            self.destroy()