import customtkinter as ctk
import logging
from ui.obs_interface import OBSLikeInterface

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('who_calls_ultimate.log'),
            logging.StreamHandler()
        ]
    )
    
    app = OBSLikeInterface()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()