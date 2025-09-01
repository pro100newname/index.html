import customtkinter as ctk
from tkinter import messagebox
import os

class GeneralCategory:
    def __init__(self, parent, content_frame, obs_colors, traffic_manager, db_manager):
        self.parent = parent
        self.content_frame = content_frame
        self.obs_colors = obs_colors
        self.traffic_manager = traffic_manager
        self.db_manager = db_manager
        
    def setup(self):
        # Основные настройки
        general_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        general_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(general_frame, text="⚙️ ОБЩИЕ НАСТРОЙКИ", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        general_settings = [
            ("Автозапуск", False),
            ("Автообновление", True),
            ("Уведомления", True),
            ("Звуковые эффекты", False),
            ("Темная тема", True)
        ]
        
        self.parent.general_vars = []
        for text, default in general_settings:
            var = ctk.BooleanVar(value=default)
            self.parent.general_vars.append(var)
            check = ctk.CTkCheckBox(general_frame, text=text, variable=var,
                                   text_color=self.obs_colors["text"])
            check.pack(anchor="w", padx=15, pady=2)
        
        # Язык интерфейса
        language_frame = ctk.CTkFrame(general_frame, fg_color="transparent")
        language_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(language_frame, text="Язык интерфейса:",
                    text_color=self.obs_colors["text"]).pack(side="left")
        
        self.parent.language_var = ctk.StringVar(value="ru")
        language_combo = ctk.CTkComboBox(language_frame, values=["ru", "en", "de", "fr"],
                                        variable=self.parent.language_var)
        language_combo.pack(side="right")
        
        # Резервное копирование
        backup_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        backup_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(backup_frame, text="💾 РЕЗЕРВНОЕ КОПИРОВАНИЕ", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        backup_buttons = [
            ("Создать backup", self.parent.create_backup, "#64B5F6"),
            ("Восстановить", self.parent.restore_backup, "#4CAF50"),
            ("Экспорт настроек", self.parent.export_settings, "#FF9800"),
            ("Импорт настроек", self.parent.import_settings, "#9C27B0")
        ]
        
        backup_grid = ctk.CTkFrame(backup_frame, fg_color="transparent")
        backup_grid.pack(fill="x", padx=15, pady=(0, 15))
        
        for i in range(0, len(backup_buttons), 2):
            row_frame = ctk.CTkFrame(backup_grid, fg_color="transparent")
            row_frame.pack(fill="x", pady=5)
            
            for j in range(2):
                if i + j < len(backup_buttons):
                    text, command, color = backup_buttons[i + j]
                    btn = ctk.CTkButton(row_frame, text=text, command=command,
                                       fg_color=color, hover_color=self.parent.darken_color(color),
                                       height=35)
                    btn.pack(side="left", expand=True, padx=5)
        
        # Сброс настроек
        reset_frame = ctk.CTkFrame(self.content_frame, fg_color=self.obs_colors["panel"], corner_radius=5)
        reset_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(reset_frame, text="🔄 СБРОС НАСТРОЕК", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.obs_colors["accent"]).pack(anchor="w", padx=15, pady=10)
        
        reset_btn = ctk.CTkButton(reset_frame, text="Сбросить все настройки",
                                 command=self.parent.reset_settings,
                                 fg_color=self.obs_colors["danger"],
                                 hover_color=self.parent.darken_color(self.obs_colors["danger"]),
                                 height=40)
        reset_btn.pack(padx=15, pady=(0, 15))