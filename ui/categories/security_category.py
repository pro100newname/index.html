import customtkinter as ctk

class SecurityCategory:
    def __init__(self, parent, content_frame, obs_colors, traffic_manager, db_manager):
        self.parent = parent
        self.content_frame = content_frame
        self.obs_colors = obs_colors
        self.traffic_manager = traffic_manager
        self.db_manager = db_manager
        
    def setup(self):
        # Настройки безопасности
        security_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        security_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(security_frame, text="🛡️ НАСТРОЙКИ БЕЗОПАСНОСТИ", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        security_settings = [
            ("Скрытый режим", True),
            ("Очистка cookies", True),
            ("Смена User-Agent", True),
            ("Обход детекции", True),
            ("VPN режим", False)
        ]
        
        self.parent.security_vars = []
        for text, default in security_settings:
            var = ctk.BooleanVar(value=default)
            self.parent.security_vars.append(var)
            check = ctk.CTkCheckBox(security_frame, text=text, variable=var,
                                   text_color=self.obs_colors["text"])
            check.pack(anchor="w", padx=15, pady=2)
        
        # Уровень безопасности
        level_frame = ctk.CTkFrame(security_frame, fg_color="transparent")
        level_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(level_frame, text="Уровень безопасности:",
                    text_color=self.obs_colors["text"]).pack(side="left")
        
        self.parent.security_level_var = ctk.StringVar(value="high")
        level_combo = ctk.CTkComboBox(level_frame, values=["low", "medium", "high", "maximum"],
                                     variable=self.parent.security_level_var)
        level_combo.pack(side="right")
        
        # Аварийные протоколы
        emergency_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        emergency_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(emergency_frame, text="🚨 АВАРИЙНЫЕ ПРОТОКОЛЫ", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        emergency_settings = [
            ("Автоостановка при детекции", True),
            ("Смена IP при блокировке", True),
            ("Экстренное завершение", True),
            ("Удаление логов", False)
        ]
        
        self.parent.emergency_vars = []
        for text, default in emergency_settings:
            var = ctk.BooleanVar(value=default)
            self.parent.emergency_vars.append(var)
            check = ctk.CTkCheckBox(emergency_frame, text=text, variable=var,
                                   text_color=self.obs_colors["text"])
            check.pack(anchor="w", padx=15, pady=2)
        
        # Кнопка сохранения
        save_btn = ctk.CTkButton(self.content_frame, text="💾 Сохранить настройки безопасности",
                                command=self.parent.save_security_settings,
                                fg_color=self.obs_colors["accent"],
                                hover_color=self.parent.darken_color(self.obs_colors["accent"]),
                                height=40)
        save_btn.pack(pady=10)