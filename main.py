# main.py

import gui_module
import excel_module

def main():
    latest_log_file = excel_module.load_closest_date_workbook()
    if latest_log_file is not None:
        gui_module.FoodLogger.filename = latest_log_file
    gui_module.init_gui()

if __name__ == "__main__":
    main()