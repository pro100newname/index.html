import customtkinter as ctk

class AICategory:
    def __init__(self, parent, content_frame, obs_colors, traffic_manager, db_manager):
        self.parent = parent
        self.content_frame = content_frame
        self.obs_colors = obs_colors
        self.traffic_manager = traffic_manager
        self.db_manager = db_manager
        
    def setup(self):
        # Основные настройки ИИ
        main_ai_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        main_ai_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(main_ai_frame, text="🤖 НАСТРОЙКИ ИСКУССТВЕННОГО ИНТЕЛЛЕКТА", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        self.parent.enable_ai_var = ctk.BooleanVar(value=True)
        ai_check = ctk.CTkCheckBox(main_ai_frame, text="Включить ИИ оптимизацию",
                                  variable=self.parent.enable_ai_var,
                                  text_color=self.obs_colors["text"])
        ai_check.pack(anchor="w", padx=15, pady=5)
        
        # Уровень ИИ
        level_frame = ctk.CTkFrame(main_ai_frame, fg_color="transparent")
        level_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(level_frame, text="Уровень ИИ:",
                    text_color=self.obs_colors["text"]).pack(side="left")
        
        self.parent.ai_level_var = ctk.StringVar(value="advanced")
        level_combo = ctk.CTkComboBox(level_frame, values=["basic", "standard", "advanced", "expert"],
                                     variable=self.parent.ai_level_var)
        level_combo.pack(side="right")
        
        # Обучение ИИ
        training_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        training_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(training_frame, text="📚 ОБУЧЕНИЕ ИИ", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        self.parent.enable_learning_var = ctk.BooleanVar(value=True)
        learning_check = ctk.CTkCheckBox(training_frame, text="Включить самообучение",
                                        variable=self.parent.enable_learning_var,
                                        text_color=self.obs_colors["text"])
        learning_check.pack(anchor="w", padx=15, pady=5)
        
        # Скорость обучения
        learning_speed_frame = ctk.CTkFrame(training_frame, fg_color="transparent")
        learning_speed_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(learning_speed_frame, text="Скорость обучения:",
                    text_color=self.obs_colors["text"]).pack(side="left")
        
        self.parent.learning_speed_var = ctk.StringVar(value="normal")
        speed_combo = ctk.CTkComboBox(learning_speed_frame, values=["slow", "normal", "fast"],
                                     variable=self.parent.learning_speed_var)
        speed_combo.pack(side="right")
        
        # Оптимизации ИИ
        optimization_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        optimization_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(optimization_frame, text="⚡ ОПТИМИЗАЦИИ", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        optimizations = [
            ("Оптимизация времени", True),
            ("Анализ паттернов", True),
            ("Предсказание успеха", True),
            ("Автоподстройка", True)
        ]
        
        self.parent.optimization_vars = []
        for text, default in optimizations:
            var = ctk.BooleanVar(value=default)
            self.parent.optimization_vars.append(var)
            check = ctk.CTkCheckBox(optimization_frame, text=text, variable=var,
                                   text_color=self.obs_colors["text"])
            check.pack(anchor="w", padx=15, pady=2)
        
        # Кнопка сохранения
        save_btn = ctk.CTkButton(self.content_frame, text="💾 Сохранить настройки ИИ",
                                command=self.parent.save_ai_settings,
                                fg_color=self.obs_colors["accent"],
                                hover_color=self.parent.darken_color(self.obs_colors["accent"]),
                                height=40)
        save_btn.pack(pady=10)