import customtkinter as ctk
from tkinter import messagebox

class WebsitesCategory:
    def __init__(self, parent, content_frame, obs_colors, traffic_manager, db_manager):
        self.parent = parent
        self.content_frame = content_frame
        self.obs_colors = obs_colors
        self.traffic_manager = traffic_manager
        self.db_manager = db_manager
        
    def setup(self):
        # Основной сайт
        main_site_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        main_site_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(main_site_frame, text="🌐 ОСНОВНОЙ САЙТ", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        self.parent.main_site_var = ctk.StringVar(value=self.parent.settings['websites'][0]['url'])
        site_entry = ctk.CTkEntry(main_site_frame, textvariable=self.parent.main_site_var,
                                placeholder_text="https://who-calls.ru")
        site_entry.pack(fill="x", padx=15, pady=(0, 15))
        
        # Дополнительные сайты
        extra_sites_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        extra_sites_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(extra_sites_frame, text="🌐 ДОПОЛНИТЕЛЬНЫЕ САЙТЫ", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        ctk.CTkLabel(extra_sites_frame, text="По одному сайту на строку:",
                    text_color=self.obs_colors["text"]).pack(anchor="w", padx=15)
        
        self.parent.extra_sites_text = ctk.CTkTextbox(extra_sites_frame, height=100)
        self.parent.extra_sites_text.pack(fill="x", padx=15, pady=5)
        
        # Загрузка существующих сайтов
        if len(self.parent.settings['websites']) > 1:
            extra_sites = "\n".join([site['url'] for site in self.parent.settings['websites'][1:]])
            self.parent.extra_sites_text.insert("1.0", extra_sites)
        
        # Настройки поведения для сайтов
        behavior_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        behavior_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(behavior_frame, text="⚙️ НАСТРОЙКИ ПОВЕДЕНИЯ ДЛЯ САЙТОВ", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        self.parent.enable_search_var = ctk.BooleanVar(value=self.parent.settings['search_settings']['enable_search'])
        search_check = ctk.CTkCheckBox(behavior_frame, text="Включить поиск на сайтах",
                                      variable=self.parent.enable_search_var,
                                      text_color=self.obs_colors["text"])
        search_check.pack(anchor="w", padx=15, pady=5)
        
        self.parent.enable_ads_var = ctk.BooleanVar(value=self.parent.settings.get('click_ads', True))
        ads_check = ctk.CTkCheckBox(behavior_frame, text="Кликать по рекламе",
                                   variable=self.parent.enable_ads_var,
                                   text_color=self.obs_colors["text"])
        ads_check.pack(anchor="w", padx=15, pady=5)
        
        # Кнопка сохранения
        save_btn = ctk.CTkButton(self.content_frame, text="💾 Сохранить настройки сайтов",
                                command=self.parent.save_websites_settings,
                                fg_color=self.obs_colors["accent"],
                                hover_color=self.parent.darken_color(self.obs_colors["accent"]),
                                height=40)
        save_btn.pack(pady=10)