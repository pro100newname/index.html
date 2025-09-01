import customtkinter as ctk
import os

class ProxyCategory:
    def __init__(self, parent, content_frame, obs_colors, traffic_manager, db_manager):
        self.parent = parent
        self.content_frame = content_frame
        self.obs_colors = obs_colors
        self.traffic_manager = traffic_manager
        self.db_manager = db_manager
        
    def setup(self):
        # Настройки прокси
        proxy_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        proxy_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(proxy_frame, text="🔗 НАСТРОЙКИ ПРОКСИ", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        self.parent.enable_proxy_var = ctk.BooleanVar(value=False)
        proxy_check = ctk.CTkCheckBox(proxy_frame, text="Включить использование прокси",
                                     variable=self.parent.enable_proxy_var,
                                     text_color=self.obs_colors["text"])
        proxy_check.pack(anchor="w", padx=15, pady=5)
        
        # Ротация прокси
        rotation_frame = ctk.CTkFrame(proxy_frame, fg_color="transparent")
        rotation_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(rotation_frame, text="Ротация прокси:",
                    text_color=self.obs_colors["text"]).pack(side="left")
        
        self.parent.proxy_rotation_var = ctk.StringVar(value="session")
        rotation_combo = ctk.CTkComboBox(rotation_frame, values=["never", "session", "hour", "minute_10"],
                                        variable=self.parent.proxy_rotation_var)
        rotation_combo.pack(side="right")
        
        # Управление прокси-листом
        list_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        list_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(list_frame, text="📋 УПРАВЛЕНИЕ ПРОКСИ-ЛИСТОМ", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        ctk.CTkLabel(list_frame, text="Формат: ip:port:login:password (по одному на строку)",
                    text_color=self.obs_colors["text"]).pack(anchor="w", padx=15)
        
        self.parent.proxy_text = ctk.CTkTextbox(list_frame, height=100)
        self.parent.proxy_text.pack(fill="x", padx=15, pady=5)
        
        # Загрузка существующих прокси
        if os.path.exists('proxies.txt'):
            try:
                with open('proxies.txt', 'r', encoding='utf-8') as f:
                    proxies = f.read()
                    self.parent.proxy_text.insert("1.0", proxies)
            except:
                pass
        
        # Кнопки управления
        proxy_buttons_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        proxy_buttons_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        proxy_buttons = [
            ("📥 Импорт прокси", self.parent.import_proxies, "#64B5F6"),
            ("💾 Сохранить прокси", self.parent.save_proxies, "#4CAF50"),
            ("🧹 Очистить список", self.parent.clear_proxies, "#F44336"),
            ("🔄 Проверить прокси", self.parent.test_proxies, "#FF9800")
        ]
        
        for text, command, color in proxy_buttons:
            btn = ctk.CTkButton(proxy_buttons_frame, text=text, command=command,
                               fg_color=color, hover_color=self.parent.darken_color(color),
                               height=30)
            btn.pack(side="left", padx=5)
        
        # Статистика прокси
        stats_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        stats_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(stats_frame, text="📊 СТАТИСТИКА ПРОКСИ", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        proxy_stats = [
            ("Всего прокси:", "total_proxies", "0"),
            ("Активных:", "active_proxies", "0"),
            ("Скорость ответа:", "proxy_speed", "0ms"),
            ("Последняя проверка:", "last_proxy_check", "Никогда")
        ]
        
        stats_grid = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_grid.pack(fill="x", padx=15, pady=(0, 15))
        
        for i in range(0, len(proxy_stats), 2):
            row_frame = ctk.CTkFrame(stats_grid, fg_color="transparent")
            row_frame.pack(fill="x", pady=5)
            
            for j in range(2):
                if i + j < len(proxy_stats):
                    label, var_name, default = proxy_stats[i + j]
                    stat_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
                    stat_frame.pack(side="left", expand=True, padx=5)
                    
                    ctk.CTkLabel(stat_frame, text=label, 
                                text_color=self.obs_colors["text"]).pack(anchor="w")
                    setattr(self.parent, f"{var_name}_var", ctk.StringVar(value=default))
                    ctk.CTkLabel(stat_frame, textvariable=getattr(self.parent, f"{var_name}_var"),
                               text_color=self.obs_colors["accent"]).pack(anchor="w")