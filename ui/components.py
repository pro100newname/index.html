import customtkinter as ctk

def create_category_button(parent, text, category, command, obs_colors):
    """Создание кнопки категории"""
    return ctk.CTkButton(
        parent, 
        text=text, 
        command=lambda: command(category),
        fg_color="transparent",
        hover_color="#333333",
        anchor="w",
        text_color=obs_colors["text"],
        font=ctk.CTkFont(size=13)
    )

def create_stat_frame(parent, label, var_name, default_value, color, obs_colors):
    """Создание фрейма со статистикой"""
    stat_frame = ctk.CTkFrame(parent, fg_color="transparent")
    
    ctk.CTkLabel(stat_frame, text=label, 
                text_color=obs_colors["text"]).pack(anchor="w")
    
    var = ctk.StringVar(value=default_value)
    ctk.CTkLabel(stat_frame, textvariable=var,
               font=ctk.CTkFont(weight="bold"), text_color=color).pack(anchor="w")
    
    return stat_frame, var

def create_action_button(parent, text, command, color, obs_colors):
    """Создание кнопки действия"""
    return ctk.CTkButton(parent, text=text, command=command,
                       fg_color=color, hover_color=darken_color(color),
                       height=35)

def darken_color(color):
    """Затемнить цвет для hover эффекта"""
    if color.startswith("#"):
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        return f"#{max(0, r-30):02x}{max(0, g-30):02x}{max(0, b-30):02x}"
    return color