import customtkinter as ctk
from utils.helpers import darken_color

class MainCategory:
    def __init__(self, parent, content_frame, obs_colors, traffic_manager, db_manager):
        self.parent = parent
        self.content_frame = content_frame
        self.obs_colors = obs_colors
        self.traffic_manager = traffic_manager
        self.db_manager = db_manager
        
    def setup(self):
        # Статистика
        stats_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        stats_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(stats_frame, text="📊 СТАТИСТИКА В РЕАЛЬНОМ ВРЕМЕНИ", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        stats_grid = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_grid.pack(fill="x", padx=15, pady=(0, 15))
        
        stats = [
            ("Всего сессий:", "total_sessions", "0", "#64B5F6"),
            ("Успешных:", "success_sessions", "0", "#4CAF50"),
            ("Кликов:", "total_clicks", "0", "#FF9800"),
            ("Доход:", "total_income", "0 руб", "#4CAF50"),
            ("Активных сайтов:", "active_sites", "0", "#64B5F6"),
            ("Прокси:", "proxy_status", "Выкл", "#F44336"),
            ("Сессий сегодня:", "sessions_today", "0", "#64B5F6")
        ]
        
        for i in range(0, len(stats), 2):
            row_frame = ctk.CTkFrame(stats_grid, fg_color="transparent")
            row_frame.pack(fill="x", pady=5)
            
            for j in range(2):
                if i + j < len(stats):
                    label, var_name, default, color = stats[i + j]
                    stat_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
                    stat_frame.pack(side="left", expand=True, padx=5)
                    
                    ctk.CTkLabel(stat_frame, text=label, 
                                text_color=self.obs_colors["text"]).pack(anchor="w")
                    setattr(self.parent, f"{var_name}_var", ctk.StringVar(value=default))
                    ctk.CTkLabel(stat_frame, textvariable=getattr(self.parent, f"{var_name}_var"),
                               font=ctk.CTkFont(weight="bold"), text_color=color).pack(anchor="w")
        
        # Быстрые действия
        actions_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        actions_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(actions_frame, text="⚡ БЫСТРЫЕ ДЕЙСТВИЯ", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        action_buttons = [
            ("🔢 Сгенерировать номера", self.parent.generate_phones, "#64B5F6"),
            ("📊 Создать отчет", self.parent.generate_report, "#4CAF50"),
            ("🔄 Обновить данные", self.parent.refresh_all, "#FF9800"),
            ("⚙️ Сохранить настройки", self.parent.save_all_settings, "#9C27B0")
        ]
        
        actions_grid = ctk.CTkFrame(actions_frame, fg_color="transparent")
        actions_grid.pack(fill="x", padx=15, pady=(0, 15))
        
        for i in range(0, len(action_buttons), 2):
            row_frame = ctk.CTkFrame(actions_grid, fg_color="transparent")
            row_frame.pack(fill="x", pady=5)
            
            for j in range(2):
                if i + j < len(action_buttons):
                    text, command, color = action_buttons[i + j]
                    btn = ctk.CTkButton(row_frame, text=text, command=command,
                                       fg_color=color, hover_color=darken_color(color),
                                       height=35)
                    btn.pack(side="left", expand=True, padx=5)
        
        # Состояние системы
        status_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        status_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(status_frame, text="📈 СОСТОЯНИЕ СИСТЕМЫ", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        status_grid = ctk.CTkFrame(status_frame, fg_color="transparent")
        status_grid.pack(fill="x", padx=15, pady=(0, 15))
        
        status_items = [
            ("Статус:", "system_status", "Остановлено", "#F44336"),
            ("ИИ:", "ai_status", "Неактивен", "#F44336"),
            ("База номеров:", "db_status", "0 номеров", "#64B5F6"),
            ("Последняя активность:", "last_activity", "Никогда", "#FF9800")
        ]
        
        for label, var_name, default, color in status_items:
            item_frame = ctk.CTkFrame(status_grid, fg_color="transparent")
            item_frame.pack(fill="x", pady=3)
            
            ctk.CTkLabel(item_frame, text=label, width=150,
                        text_color=self.obs_colors["text"]).pack(side="left")
            setattr(self.parent, f"{var_name}_var", ctk.StringVar(value=default))
            ctk.CTkLabel(item_frame, textvariable=getattr(self.parent, f"{var_name}_var"),
                       text_color=color, font=ctk.CTkFont(weight="bold")).pack(side="right")
        
        # Обновляем данные
        self.parent.update_main_stats()