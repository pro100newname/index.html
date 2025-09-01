import customtkinter as ctk

class SearchCategory:
    def __init__(self, parent, content_frame, obs_colors, traffic_manager, db_manager):
        self.parent = parent
        self.content_frame = content_frame
        self.obs_colors = obs_colors
        self.traffic_manager = traffic_manager
        self.db_manager = db_manager
        
    def setup(self):
        # Настройки поиска
        search_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        search_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(search_frame, text="🔍 НАСТРОЙКИ ПОИскА", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        # Скорость поиска
        speed_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        speed_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(speed_frame, text="Скорость поиска:",
                    text_color=self.obs_colors["text"]).pack(side="left")
        
        self.parent.search_speed_var = ctk.StringVar(value="normal")
        speed_combo = ctk.CTkComboBox(speed_frame, values=["slow", "normal", "fast", "very_fast"],
                                    variable=self.parent.search_speed_var)
        speed_combo.pack(side="right")
        
        # Глубина поиска
        depth_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        depth_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(depth_frame, text="Глубина поиска:",
                    text_color=self.obs_colors["text"]).pack(side="left")
        
        self.parent.search_depth_var = ctk.IntVar(value=3)
        depth_slider = ctk.CTkSlider(depth_frame, from_=1, to=10, variable=self.parent.search_depth_var)
        depth_slider.pack(side="right", fill="x", expand=True, padx=(10, 0))
        ctk.CTkLabel(depth_frame, textvariable=self.parent.search_depth_var,
                    text_color=self.obs_colors["accent"]).pack(side="right", padx=(5, 0))
        
        # Тип поиска
        type_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        type_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(type_frame, text="Тип поиска:",
                    text_color=self.obs_colors["text"]).pack(side="left")
        
        self.parent.search_type_var = ctk.StringVar(value="standard")
        type_combo = ctk.CTkComboBox(type_frame, values=["standard", "advanced", "stealth"],
                                   variable=self.parent.search_type_var)
        type_combo.pack(side="right")
        
        # Дополнительные настройки
        advanced_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        advanced_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(advanced_frame, text="⚙️ ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        self.parent.enable_ai_search_var = ctk.BooleanVar(value=True)
        ai_check = ctk.CTkCheckBox(advanced_frame, text="Использовать ИИ для оптимизации поиска",
                                  variable=self.parent.enable_ai_search_var,
                                  text_color=self.obs_colors["text"])
        ai_check.pack(anchor="w", padx=15, pady=5)
        
        self.parent.randomize_search_var = ctk.BooleanVar(value=True)
        random_check = ctk.CTkCheckBox(advanced_frame, text="Случайный порядок поиска",
                                      variable=self.parent.randomize_search_var,
                                      text_color=self.obs_colors["text"])
        random_check.pack(anchor="w", padx=15, pady=5)
        
        # Кнопка сохранения
        save_btn = ctk.CTkButton(self.content_frame, text="💾 Сохранить настройки поиска",
                                command=self.parent.save_search_settings,
                                fg_color=self.obs_colors["accent"],
                                hover_color=self.parent.darken_color(self.obs_colors["accent"]),
                                height=40)
        save_btn.pack(pady=10)