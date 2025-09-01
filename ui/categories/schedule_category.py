import customtkinter as ctk

class ScheduleCategory:
    def __init__(self, parent, content_frame, obs_colors, traffic_manager, db_manager):
        self.parent = parent
        self.content_frame = content_frame
        self.obs_colors = obs_colors
        self.traffic_manager = traffic_manager
        self.db_manager = db_manager
        
    def setup(self):
        # Основное расписание
        main_schedule_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        main_schedule_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(main_schedule_frame, text="⏰ РАСПИСАНИЕ РАБОТЫ", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        # Включить расписание
        self.parent.enable_schedule_var = ctk.BooleanVar(value=False)
        schedule_check = ctk.CTkCheckBox(main_schedule_frame, text="Включить расписание",
                                        variable=self.parent.enable_schedule_var,
                                        text_color=self.obs_colors["text"])
        schedule_check.pack(anchor="w", padx=15, pady=5)
        
        # Время работы
        time_frame = ctk.CTkFrame(main_schedule_frame, fg_color="transparent")
        time_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(time_frame, text="Время работы:",
                    text_color=self.obs_colors["text"]).pack(side="left")
        
        self.parent.start_time_var = ctk.StringVar(value="09:00")
        self.parent.end_time_var = ctk.StringVar(value="18:00")
        
        start_entry = ctk.CTkEntry(time_frame, textvariable=self.parent.start_time_var, width=60)
        start_entry.pack(side="left", padx=(10, 5))
        
        ctk.CTkLabel(time_frame, text="до",
                    text_color=self.obs_colors["text"]).pack(side="left", padx=5)
        
        end_entry = ctk.CTkEntry(time_frame, textvariable=self.parent.end_time_var, width=60)
        end_entry.pack(side="left", padx=5)
        
        # Дни недели
        days_frame = ctk.CTkFrame(main_schedule_frame, fg_color="transparent")
        days_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(days_frame, text="Дни недели:",
                    text_color=self.obs_colors["text"]).pack(side="left")
        
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        self.parent.days_vars = [ctk.BooleanVar(value=True) for _ in range(7)]
        
        days_buttons_frame = ctk.CTkFrame(days_frame, fg_color="transparent")
        days_buttons_frame.pack(side="right")
        
        for i, day in enumerate(days):
            btn = ctk.CTkCheckBox(days_buttons_frame, text=day, variable=self.parent.days_vars[i],
                                 width=30, text_color=self.obs_colors["text"])
            btn.pack(side="left", padx=2)
        
        # Суточный лимит сессий
        daily_limit_frame = ctk.CTkFrame(main_schedule_frame, fg_color="transparent")
        daily_limit_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(daily_limit_frame, text="Суточный лимит сессий:",
                    text_color=self.obs_colors["text"]).pack(side="left")
        
        self.parent.daily_limit_var = ctk.IntVar(value=100)
        limit_slider = ctk.CTkSlider(daily_limit_frame, from_=1, to=500, variable=self.parent.daily_limit_var)
        limit_slider.pack(side="right", fill="x", expand=True, padx=(10, 0))
        ctk.CTkLabel(daily_limit_frame, textvariable=self.parent.daily_limit_var,
                    text_color=self.obs_colors["accent"]).pack(side="right", padx=(5, 0))
        
        # Перерывы
        breaks_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        breaks_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(breaks_frame, text="☕ ПЕРЕРЫВЫ", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        self.parent.enable_breaks_var = ctk.BooleanVar(value=True)
        breaks_check = ctk.CTkCheckBox(breaks_frame, text="Включить автоматические перерывы",
                                      variable=self.parent.enable_breaks_var,
                                      text_color=self.obs_colors["text"])
        breaks_check.pack(anchor="w", padx=15, pady=5)
        
        # Длительность перерыва
        break_duration_frame = ctk.CTkFrame(breaks_frame, fg_color="transparent")
        break_duration_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(break_duration_frame, text="Длительность перерыва (мин):",
                    text_color=self.obs_colors["text"]).pack(side="left")
        
        self.parent.break_duration_var = ctk.IntVar(value=5)
        duration_slider = ctk.CTkSlider(break_duration_frame, from_=1, to=30, variable=self.parent.break_duration_var)
        duration_slider.pack(side="right", fill="x", expand=True, padx=(10, 0))
        ctk.CTkLabel(break_duration_frame, textvariable=self.parent.break_duration_var,
                    text_color=self.obs_colors["accent"]).pack(side="right", padx=(5, 0))
        
        # Интервал между перерывами
        break_interval_frame = ctk.CTkFrame(breaks_frame, fg_color="transparent")
        break_interval_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        ctk.CTkLabel(break_interval_frame, text="Интервал между перерывами (мин):",
                    text_color=self.obs_colors["text"]).pack(side="left")
        
        self.parent.break_interval_var = ctk.IntVar(value=30)
        interval_slider = ctk.CTkSlider(break_interval_frame, from_=5, to=120, variable=self.parent.break_interval_var)
        interval_slider.pack(side="right", fill="x", expand=True, padx=(10, 0))
        ctk.CTkLabel(break_interval_frame, textvariable=self.parent.break_interval_var,
                    text_color=self.obs_colors["accent"]).pack(side="right", padx=(5, 0))
        
        # Кнопка сохранения
        save_btn = ctk.CTkButton(self.content_frame, text="💾 Сохранить расписание",
                                command=self.parent.save_schedule_settings,
                                fg_color=self.obs_colors["accent"],
                                hover_color=self.parent.darken_color(self.obs_colors["accent"]),
                                height=40)
        save_btn.pack(pady=10)