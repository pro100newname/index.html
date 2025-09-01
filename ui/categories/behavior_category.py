import customtkinter as ctk

class BehaviorCategory:
    def __init__(self, parent, content_frame, obs_colors, traffic_manager, db_manager):
        self.parent = parent
        self.content_frame = content_frame
        self.obs_colors = obs_colors
        self.traffic_manager = traffic_manager
        self.db_manager = db_manager
        
    def setup(self):
        # Настройки поведения браузера
        behavior_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        behavior_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(behavior_frame, text="🎯 НАСТРОЙКИ ПОВЕДЕНИЯ БРАУЗЕРА", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        behaviors = [
            ("Имитация человека", True),
            ("Случайные задержки", True),
            ("Скроллинг страниц", True),
            ("Переходы по ссылкам", True),
            ("Клики по рекламе", True),
            ("Заполнение форм", False)
        ]
        
        self.parent.behavior_vars = []
        for text, default in behaviors:
            var = ctk.BooleanVar(value=default)
            self.parent.behavior_vars.append(var)
            check = ctk.CTkCheckBox(behavior_frame, text=text, variable=var,
                                   text_color=self.obs_colors["text"])
            check.pack(anchor="w", padx=15, pady=2)
        
        # Настройки задержек
        delays_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        delays_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(delays_frame, text="⏱️ НАСТРОЙКИ ЗАДЕРЖЕК", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        delay_settings = [
            ("Задержка между действиями (сек):", 1, 10, 2),
            ("Задержка между сессиями (сек):", 5, 60, 15),
            ("Время на сайте (сек):", 10, 300, 30)
        ]
        
        self.parent.delay_vars = []
        for text, min_val, max_val, default in delay_settings:
            frame = ctk.CTkFrame(delays_frame, fg_color="transparent")
            frame.pack(fill="x", padx=15, pady=5)
            
            ctk.CTkLabel(frame, text=text,
                        text_color=self.obs_colors["text"]).pack(side="left")
            
            var = ctk.IntVar(value=default)
            self.parent.delay_vars.append(var)
            slider = ctk.CTkSlider(frame, from_=min_val, to=max_val, variable=var)
            slider.pack(side="right", fill="x", expand=True, padx=(10, 0))
            ctk.CTkLabel(frame, textvariable=var,
                        text_color=self.obs_colors["accent"]).pack(side="right", padx=(5, 0))
        
        # Кнопка сохранения
        save_btn = ctk.CTkButton(self.content_frame, text="💾 Сохранить настройки поведения",
                                command=self.parent.save_behavior_settings,
                                fg_color=self.obs_colors["accent"],
                                hover_color=self.parent.darken_color(self.obs_colors["accent"]),
                                height=40)
        save_btn.pack(pady=10)