import customtkinter as ctk

class PerformanceCategory:
    def __init__(self, parent, content_frame, obs_colors, traffic_manager, db_manager):
        self.parent = parent
        self.content_frame = content_frame
        self.obs_colors = obs_colors
        self.traffic_manager = traffic_manager
        self.db_manager = db_manager
        
    def setup(self):
        # Настройки производительности
        performance_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        performance_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(performance_frame, text="⚡ НАСТРОЙКИ ПРОИЗВОДИТЕЛЬНОСТИ", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        performance_settings = [
            ("Многопоточность", True),
            ("Кэширование", True),
            ("Сжатие данных", True),
            ("Оптимизация памяти", True)
        ]
        
        self.parent.performance_vars = []
        for text, default in performance_settings:
            var = ctk.BooleanVar(value=default)
            self.parent.performance_vars.append(var)
            check = ctk.CTkCheckBox(performance_frame, text=text, variable=var,
                                   text_color=self.obs_colors["text"])
            check.pack(anchor="w", padx=15, pady=2)
        
        # Параллельные сессии
        sessions_frame = ctk.CTkFrame(performance_frame, fg_color="transparent")
        sessions_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(sessions_frame, text="Параллельные сессии:",
                    text_color=self.obs_colors["text"]).pack(side="left")
        
        self.parent.parallel_sessions_var = ctk.IntVar(value=1)
        sessions_slider = ctk.CTkSlider(sessions_frame, from_=1, to=10, variable=self.parent.parallel_sessions_var)
        sessions_slider.pack(side="right", fill="x", expand=True, padx=(10, 0))
        ctk.CTkLabel(sessions_frame, textvariable=self.parent.parallel_sessions_var,
                    text_color=self.obs_colors["accent"]).pack(side="right", padx=(5, 0))
        
        # Лимиты ресурсов
        limits_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        limits_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(limits_frame, text="📊 ЛИМИТЫ РЕСУРСОВ", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        resource_limits = [
            ("Макс. использование CPU (%):", 10, 100, 50),
            ("Макс. использование RAM (MB):", 100, 2000, 500),
            ("Макс. сессий в час:", 1, 100, 20)
        ]
        
        self.parent.resource_vars = []
        for text, min_val, max_val, default in resource_limits:
            frame = ctk.CTkFrame(limits_frame, fg_color="transparent")
            frame.pack(fill="x", padx=15, pady=5)
            
            ctk.CTkLabel(frame, text=text,
                        text_color=self.obs_colors["text"]).pack(side="left")
            
            var = ctk.IntVar(value=default)
            self.parent.resource_vars.append(var)
            slider = ctk.CTkSlider(frame, from_=min_val, to=max_val, variable=var)
            slider.pack(side="right", fill="x", expand=True, padx=(10, 0))
            ctk.CTkLabel(frame, textvariable=var,
                        text_color=self.obs_colors["accent"]).pack(side="right", padx=(5, 0))
        
        # Кнопка сохранения
        save_btn = ctk.CTkButton(self.content_frame, text="💾 Сохранить настройки производительности",
                                command=self.parent.save_performance_settings,
                                fg_color=self.obs_colors["accent"],
                                hover_color=self.parent.darken_color(self.obs_colors["accent"]),
                                height=40)
        save_btn.pack(pady=10)