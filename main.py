import tkinter as tk
from tkinter import ttk

from core.plugin_manager import PluginManager
from core.calculation_log import CalculationLog
from gui.main_window import MainWindow

def main():
    """Hauptfunktion der Anwendung."""
    # Wurzelelement der Tkinter-Anwendung erstellen
    root = tk.Tk()
    
    # Plugin-Manager erstellen
    plugin_manager = PluginManager()
    
    # Berechnungsprotokoll erstellen
    calculation_log = CalculationLog()
    
    # Hauptfenster erstellen
    main_window = MainWindow(root, plugin_manager, calculation_log)
    
    # Initialen Theme-Stil anwenden
    style = ttk.Style()
    style.theme_use('clam')  # 'clam' ist ein guter Kompromiss fuer moderne Darstellung
    
    # Tastenkuerzel fuer haeufige Aktionen
    root.bind("<F1>", lambda e: main_window._show_about())
    root.bind("<Control-s>", lambda e: main_window._save_log())
    root.bind("<Control-o>", lambda e: main_window._load_log())
    
    # Tkinter-Hauptschleife starten
    root.mainloop()

if __name__ == "__main__":
    main()