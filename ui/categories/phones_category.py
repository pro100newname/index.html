import customtkinter as ctk
from tkinter import messagebox

class PhonesCategory:
    def __init__(self, parent, content_frame, obs_colors, traffic_manager, db_manager):
        self.parent = parent
        self.content_frame = content_frame
        self.obs_colors = obs_colors
        self.traffic_manager = traffic_manager
        self.db_manager = db_manager
        
    def setup(self):
        # Статистика номеров
        stats_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        stats_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(stats_frame, text="📊 СТАТИСТИКА НОМЕРОВ", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        stats_grid = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_grid.pack(fill="x", padx=15, pady=(0, 15))
        
        phone_stats = [
            ("Всего номеров:", "total_phones", "0"),
            ("Использовано:", "used_phones", "0"),
            ("Уникальных:", "unique_phones", "0"),
            ("Последнее обновление:", "last_update", "Никогда")
        ]
        
        for i in range(0, len(phone_stats), 2):
            row_frame = ctk.CTkFrame(stats_grid, fg_color="transparent")
            row_frame.pack(fill="x", pady=5)
            
            for j in range(2):
                if i + j < len(phone_stats):
                    label, var_name, default = phone_stats[i + j]
                    stat_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
                    stat_frame.pack(side="left", expand=True, padx=5)
                    
                    ctk.CTkLabel(stat_frame, text=label, 
                                text_color=self.obs_colors["text"]).pack(anchor="w")
                    setattr(self.parent, f"{var_name}_var", ctk.StringVar(value=default))
                    ctk.CTkLabel(stat_frame, textvariable=getattr(self.parent, f"{var_name}_var"),
                               text_color=self.obs_colors["accent"]).pack(anchor="w")
        
        # Управление номерами
        manage_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        manage_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(manage_frame, text="🛠️ УПРАВЛЕНИЕ БАЗОЙ НОМЕРОВ", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        manage_buttons = [
            ("📥 Импорт номеров", self.parent.import_phones, "#64B5F6"),
            ("📤 Экспорт номеров", self.parent.export_phones, "#4CAF50"),
            ("🔢 Сгенерировать", self.parent.generate_phones, "#FF9800"),
            ("🧹 Очистить базу", self.parent.clear_phones, "#F44336")
        ]
        
        manage_grid = ctk.CTkFrame(manage_frame, fg_color="transparent")
        manage_grid.pack(fill="x", padx=15, pady=(0, 15))
        
        for i in range(0, len(manage_buttons), 2):
            row_frame = ctk.CTkFrame(manage_grid, fg_color="transparent")
            row_frame.pack(fill="x", pady=5)
            
            for j in range(2):
                if i + j < len(manage_buttons):
                    text, command, color = manage_buttons[i + j]
                    btn = ctk.CTkButton(row_frame, text=text, command=command,
                                       fg_color=color, hover_color=self.parent.darken_color(color),
                                       height=35)
                    btn.pack(side="left", expand=True, padx=5)
        
        # Просмотр номеров
        view_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        view_frame.pack(fill="both", expand=True, pady=5)
        
        ctk.CTkLabel(view_frame, text="👁️ ПРОСМОТР НОМЕРОВ", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        # Таблица номеров
        columns = ["phone", "city", "used", "last_used"]
        self.parent.phones_table = ctk.CTkScrollableFrame(view_frame, height=200)
        self.parent.phones_table.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Обновляем данные
        self.parent.update_phones_stats()