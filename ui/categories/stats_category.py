import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class StatsCategory:
    def __init__(self, parent, content_frame, obs_colors, traffic_manager, db_manager):
        self.parent = parent
        self.content_frame = content_frame
        self.obs_colors = obs_colors
        self.traffic_manager = traffic_manager
        self.db_manager = db_manager
        
    def setup(self):
        # Основная статистика
        main_stats_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        main_stats_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(main_stats_frame, text="📈 ОСНОВНАЯ СТАТИСТИКА", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        # График активности
        fig, ax = plt.subplots(figsize=(8, 4))
        days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        activity = [random.randint(10, 100) for _ in range(7)]
        
        ax.bar(days, activity, color=self.obs_colors["accent"].lower())
        ax.set_title('Активность по дням недели')
        ax.set_ylabel('Сессии')
        
        canvas = FigureCanvasTkAgg(fig, main_stats_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="x", padx=15, pady=10)
        
        # Детальная статистика
        detail_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        detail_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(detail_frame, text="📊 ДЕТАЛЬНАя СТАТИСТИКА", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        stats_data = [
            ("Всего сессий", "1582"),
            ("Успешных", "1345 (85%)"),
            ("Доход", "12,450 руб"),
            ("Среднее время", "2.3 мин"),
            ("Лучший день", "Вчера (245)"),
            ("Топ сайт", "who-calls.ru")
        ]
        
        stats_grid = ctk.CTkFrame(detail_frame, fg_color="transparent")
        stats_grid.pack(fill="x", padx=15, pady=(0, 15))
        
        for i in range(0, len(stats_data), 2):
            row_frame = ctk.CTkFrame(stats_grid, fg_color="transparent")
            row_frame.pack(fill="x", pady=5)
            
            for j in range(2):
                if i + j < len(stats_data):
                    label, value = stats_data[i + j]
                    stat_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
                    stat_frame.pack(side="left", expand=True, padx=5)
                    
                    ctk.CTkLabel(stat_frame, text=label + ":",
                                text_color=self.obs_colors["text"]).pack(anchor="w")
                    ctk.CTkLabel(stat_frame, text=value,
                                text_color=self.obs_colors["accent"],
                                font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        
        # Отчеты
        reports_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        reports_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(reports_frame, text="📋 ГЕНЕРАЦИЯ ОТЧЕТОВ", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        report_buttons = [
            ("📊 Ежедневный отчет", self.parent.generate_daily_report, "#64B5F6"),
            ("📈 Недельный отчет", self.parent.generate_weekly_report, "#4CAF50"),
            ("📅 Месячный отчет", self.parent.generate_monthly_report, "#FF9800"),
            ("💾 Экспорт в Excel", self.parent.export_to_excel, "#9C27B0")
        ]
        
        reports_grid = ctk.CTkFrame(reports_frame, fg_color="transparent")
        reports_grid.pack(fill="x", padx=15, pady=(0, 15))
        
        for i in range(0, len(report_buttons), 2):
            row_frame = ctk.CTkFrame(reports_grid, fg_color="transparent")
            row_frame.pack(fill="x", pady=5)
            
            for j in range(2):
                if i + j < len(report_buttons):
                    text, command, color = report_buttons[i + j]
                    btn = ctk.CTkButton(row_frame, text=text, command=command,
                                       fg_color=color, hover_color=self.parent.darken_color(color),
                                       height=35)
                    btn.pack(side="left", expand=True, padx=5)