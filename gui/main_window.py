# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, List, Optional, Any, Tuple

from core.plugin_manager import PluginManager
from core.plugin_interface import IPlugin, Command
from core.calculation_log import CalculationLog
from gui.theme_manager import ThemeManager
from gui.triangle_input import TriangleInputPanel
from gui.side_calculator import SideCalculator

class MainWindow:
    """Hauptfenster der Anwendung."""
    
    def __init__(self, root: tk.Tk, plugin_manager: PluginManager, calculation_log: CalculationLog):
        """
        Initialisiert das Hauptfenster der Anwendung.
        
        Args:
            root: Das Wurzelelement der Tkinter-Anwendung
            plugin_manager: Der Plugin-Manager
            calculation_log: Das Berechnungsprotokoll
        """
        self.root = root
        self.plugin_manager = plugin_manager
        self.calculation_log = calculation_log
        self.current_plugin: Optional[IPlugin] = None
        self.current_command: Optional[Command] = None
        self.theme_manager = ThemeManager(root)
        self.param_entries: List[ttk.Entry] = []
        
        # Fenstereinstellungen
        root.title("JustForYou - Taschenrechner")
        root.geometry("1024x768")  # Groesseres Fenster fuer bessere Darstellung
        root.minsize(900, 700)     # Mindestgroesse anpassen
        
        # Benutzerdefinierte Styles fuer verschiedene Elemente
        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 11))
        style.configure('TButton', font=('Arial', 11))
        style.configure('TEntry', font=('Arial', 11))
        style.configure('Big.TButton', font=('Arial', 12, 'bold'))
        style.configure('Keypad.TButton', font=('Arial', 12))
        
        # Hauptframe
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Layout erstellen
        self._create_layout()
        
        # Plugins laden
        self._load_plugins()
    
    def _save_log(self) -> None:
        """Speichert das Berechnungsprotokoll in einer Datei."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Textdateien", "*.txt"), ("Alle Dateien", "*.*")]
        )

        if not filename:
            return

        if self.calculation_log.save_to_file(filename):
            messagebox.showinfo("Erfolg", "Protokoll erfolgreich gespeichert.")
        else:
            messagebox.showerror("Fehler", "Fehler beim Speichern des Protokolls.")
            
    def _load_log(self) -> None:
        """Laedt das Berechnungsprotokoll aus einer Datei."""
        filename = filedialog.askopenfilename(
            filetypes=[("Textdateien", "*.txt"), ("Alle Dateien", "*.*")]
        )

        if not filename:
            return

        if self.calculation_log.load_from_file(filename):
            self._update_log_view()
            messagebox.showinfo("Erfolg", "Protokoll erfolgreich geladen.")
        else:
            messagebox.showerror("Fehler", "Fehler beim Laden des Protokolls.")
            
    def _clear_log(self) -> None:
        """Loescht das Berechnungsprotokoll."""
        if messagebox.askyesno("Bestaetigung", "Moechten Sie das Protokoll wirklich loeschen?"):
            self.calculation_log.clear()
            self._update_log_view()
            
    def _show_about(self) -> None:
        """Zeigt Informationen ueber die Anwendung an."""
        messagebox.showinfo(
            "ueber JustForYou Taschenrechner",
            "JustForYou Taschenrechner\n\n"
            "Ein modularer Taschenrechner mit branchenspezifischen Funktionen.\n\n"
        )
            
    def _open_theme_settings(self) -> None:
        """oeffnet die Einstellungen fuer das Design."""
        self.theme_manager.open_settings_dialog()
    
    def _create_layout(self) -> None:
        """Erstellt das Layout des Hauptfensters."""
        # Oberer Bereich: Menueleiste
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        
        # Datei-Menue
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Datei", menu=file_menu)
        file_menu.add_command(label="Protokoll speichern", command=self._save_log)
        file_menu.add_command(label="Protokoll laden", command=self._load_log)
        file_menu.add_command(label="Protokoll loeschen", command=self._clear_log)
        file_menu.add_separator()
        file_menu.add_command(label="Beenden", command=self.root.quit)
        
        # Darstellung-Menue
        view_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Darstellung", menu=view_menu)
        view_menu.add_command(label="Design anpassen", command=self._open_theme_settings)
        
        # Hilfe-Menue
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Hilfe", menu=help_menu)
        help_menu.add_command(label="ueber", command=self._show_about)
        
        # Layout mit zwei Hauptbereichen: Links und Rechts
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=3)
        self.main_frame.rowconfigure(0, weight=1)
        
        # Linke Spalte: Modulauswahl
        left_frame = ttk.LabelFrame(self.main_frame, text="Module")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Liste der Module mit Scrollbar
        module_container = ttk.Frame(left_frame)
        module_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.module_listbox = tk.Listbox(
            module_container, 
            selectmode=tk.SINGLE, 
            font=("Arial", 12, "bold"),
            activestyle="none",
            highlightthickness=0,
            bd=1
        )
        module_scrollbar = ttk.Scrollbar(module_container, orient="vertical", command=self.module_listbox.yview)
        self.module_listbox.configure(yscrollcommand=module_scrollbar.set)
        
        self.module_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        module_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.module_listbox.bind("<<ListboxSelect>>", self._on_module_select)
        
        # Rechte Spalte: Berechnungen und Funktionsauswahl
        right_frame = ttk.Frame(self.main_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        right_frame.columnconfigure(0, weight=1)
        
        # aenderung: Neue Aufteilung der Hoehe fuer Nebenrechner
        # Protokoll bekommt 25%, Nebenrechner 15%, Funktionsauswahl 20%, Eingabebereich 40%
        right_frame.rowconfigure(0, weight=25)  # Protokoll
        right_frame.rowconfigure(1, weight=15)  # Nebenrechner (NEU)
        right_frame.rowconfigure(2, weight=20)  # Funktionsauswahl
        right_frame.rowconfigure(3, weight=40)  # Eingabebereich
        
        # Oberer Bereich: Protokoll
        log_frame = ttk.LabelFrame(right_frame, text="Berechnungsprotokoll")
        log_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Layout fuer Protokoll: Liste und Buttons
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        log_frame.rowconfigure(1, weight=0)
        
        # Protokollliste mit Scrollbar
        log_container = ttk.Frame(log_frame)
        log_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.log_listbox = tk.Listbox(
            log_container, 
            font=("Arial", 11),
            activestyle="none",
            highlightthickness=0,
            bd=1
        )
        scrollbar = ttk.Scrollbar(log_container, orient="vertical", command=self.log_listbox.yview)
        self.log_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.log_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Kontextmenue fuer Protokollliste zum Kopieren
        self.log_context_menu = tk.Menu(self.log_listbox, tearoff=0)
        self.log_context_menu.add_command(label="Kopieren", command=self._copy_log_entry)
        self.log_context_menu.add_command(label="In Nebenrechner einfuegen", command=self._insert_to_side_calc)
        
        # Rechtsklick auf Protokollliste
        self.log_listbox.bind("<Button-3>", self._show_log_context_menu)
        # Doppelklick fuer schnelles Kopieren
        self.log_listbox.bind("<Double-Button-1>", lambda e: self._copy_log_entry())
        
        # Protokoll-Buttons
        log_buttons_frame = ttk.Frame(log_frame)
        log_buttons_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        save_button = ttk.Button(log_buttons_frame, text="Speichern", command=self._save_log)
        save_button.pack(side=tk.LEFT, padx=5)
        
        load_button = ttk.Button(log_buttons_frame, text="Laden", command=self._load_log)
        load_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = ttk.Button(log_buttons_frame, text="Loeschen", command=self._clear_log)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # NEU: Nebenrechner-Bereich
        side_calc_frame = ttk.LabelFrame(right_frame, text="Nebenrechner")
        side_calc_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # SideCalculator-Widget einbinden
        self.side_calculator = SideCalculator(
            side_calc_frame, 
            on_result_available=self._on_side_calc_result
        )
        self.side_calculator.pack(fill=tk.BOTH, expand=True)
        
        # Mittlerer Bereich: Funktionsauswahl
        self.function_frame = ttk.LabelFrame(right_frame, text="Funktionen")
        self.function_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        
        # Platzhaltertext
        self.placeholder_label = ttk.Label(
            self.function_frame, 
            text="Bitte waehlen Sie ein Modul aus.",
            font=("Arial", 12)
        )
        self.placeholder_label.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Unterer Bereich: Parametereingabe und Taschenrechner
        self.input_frame = ttk.LabelFrame(right_frame, text="Eingabe")
        self.input_frame.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        
        # Platzhalter fuer Eingabebereich
        self.input_placeholder = ttk.Label(
            self.input_frame, 
            text="Waehlen Sie eine Funktion aus.",
            font=("Arial", 12)
        )
        self.input_placeholder.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    def _load_plugins(self) -> None:
        """Laedt die Plugins und aktualisiert die Modulanzeige."""
        self.plugin_manager.load_plugins()
        
        # Plugin-Informationen abrufen
        plugin_infos = self.plugin_manager.get_plugin_infos()
        
        # Module in Listbox anzeigen
        for plugin_info in plugin_infos:
            self.module_listbox.insert(tk.END, plugin_info.name)
        
        # Erstes Modul auswaehlen
        if self.module_listbox.size() > 0:
            self.module_listbox.select_set(0)
            self.module_listbox.event_generate("<<ListboxSelect>>")
            
    def _on_module_select(self, event) -> None:
        """
        Wird aufgerufen, wenn ein Modul in der Liste ausgewaehlt wird.
        
        Args:
            event: Das Ereignis, das den Aufruf ausgeloest hat
        """
        selection = self.module_listbox.curselection()
        if not selection:
            return
        
        # Ausgewaehltes Modul abrufen
        module_name = self.module_listbox.get(selection[0])
        
        # Plugin-Info und Plugin abrufen
        for plugin_name, plugin_info in self.plugin_manager.plugin_infos.items():
            if plugin_info.name == module_name:
                self.current_plugin = self.plugin_manager.get_plugin(plugin_name)
                break
        
        if not self.current_plugin:
            return
        
        # Funktionen des Moduls anzeigen
        self._display_functions()
        
    def _display_functions(self) -> None:
        """Zeigt die Funktionen des aktuellen Moduls an."""
        # Alte Elemente entfernen
        for widget in self.function_frame.winfo_children():
            widget.destroy()
        
        # Platzhalter fuer Eingabebereich setzen
        self.input_placeholder.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        if not self.current_plugin:
            return
        
        plugin_info = self.current_plugin.get_info()
        
        # Grid-Layout fuer Funktionsbuttons
        rows = (len(plugin_info.commands) + 2) // 3  # 3 Buttons pro Zeile
        
        for i, command in enumerate(plugin_info.commands):
            row = i // 3
            col = i % 3
            
            button = ttk.Button(
                self.function_frame,
                text=command.name,
                command=lambda cmd=command: self._on_function_select(cmd),
                padding=10
            )
            button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Grid-Konfiguration
        for i in range(rows):
            self.function_frame.rowconfigure(i, weight=1)
        
        for i in range(3):
            self.function_frame.columnconfigure(i, weight=1)
            
    def _on_function_select(self, command: Command) -> None:
        """
        Wird aufgerufen, wenn eine Funktion ausgewaehlt wird.
        
        Args:
            command: Der ausgewaehlte Befehl
        """
        self.current_command = command
        
        # Eingabebereich fuer die Funktion erstellen
        self._create_input_area(command)
        
    def _create_input_area(self, command: Command) -> None:
        """
        Erstellt den Eingabebereich fuer einen Befehl.
        
        Args:
            command: Der Befehl, fuer den der Eingabebereich erstellt werden soll
        """
        # Alte Elemente entfernen
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        
        # Spezialbehandlung fuer den Dreiecksrechner
        if command.name == "Dreieck":
            self._create_triangle_input_area()
            return
        
        # Standardbehandlung fuer andere Befehle (wie bisher)
        # Parameter-Frame
        param_frame = ttk.Frame(self.input_frame)
        param_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Layout-Aufteilung: Parameter links, Keypad rechts
        param_frame.columnconfigure(0, weight=1)  # Parameter-Bereich
        param_frame.columnconfigure(1, weight=1)  # Keypad-Bereich
        
        # Linker Bereich: Parameter-Eintraege
        left_area = ttk.Frame(param_frame)
        left_area.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Parameter-Eintraege
        self.param_entries = []
        
        for i, param_name in enumerate(command.param_names):
            entry_frame = ttk.Frame(left_area)
            entry_frame.pack(fill=tk.X, pady=8)
            
            label = ttk.Label(entry_frame, text=f"{param_name}:", width=15, anchor="e", font=("Arial", 11))
            label.pack(side=tk.LEFT, padx=(0, 5))
            
            entry = ttk.Entry(entry_frame, font=("Arial", 11))
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Kontextmenue fuer Eingabefelder
            self._add_entry_context_menu(entry)
            
            self.param_entries.append(entry)
        
        # Berechnen-Button im linken Bereich
        calculate_button = ttk.Button(
            left_area,
            text="Berechnen",
            command=self._execute_calculation,
            padding=10,
            style='Big.TButton'
        )
        calculate_button.pack(fill=tk.X, pady=15)
        
        # Rechter Bereich: Keypad
        right_area = ttk.LabelFrame(param_frame, text="Taschenrechner")
        right_area.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Tastenanordnung
        keypad_buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "C", "+"],
            ["(", ")", "CE", "="]
        ]
        
        # Aktuelle Eingabe
        self.current_entry = self.param_entries[0] if self.param_entries else None
        
        # Keypad-Container
        keypad_container = ttk.Frame(right_area)
        keypad_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tasten erstellen
        for row_idx, row in enumerate(keypad_buttons):
            for col_idx, key in enumerate(row):
                button = ttk.Button(
                    keypad_container,
                    text=key,
                    width=3,
                    command=lambda k=key: self._on_keypad_press(k),
                    style='Keypad.TButton'
                )
                button.grid(row=row_idx, column=col_idx, padx=3, pady=3, sticky="nsew")
            
            keypad_container.rowconfigure(row_idx, weight=1)
        
        for col_idx in range(4):
            keypad_container.columnconfigure(col_idx, weight=1)
        
        # Event-Handler fuer Eingabefelder setzen
        for entry in self.param_entries:
            entry.bind("<FocusIn>", lambda e, ent=entry: self._on_entry_focus(ent))
        
        # Ersten Eingabefeld fokussieren
        if self.param_entries:
            self.param_entries[0].focus_set()
            
    def _on_entry_focus(self, entry) -> None:
        """
        Wird aufgerufen, wenn ein Eingabefeld den Fokus erhaelt.
        
        Args:
            entry: Das fokussierte Eingabefeld
        """
        self.current_entry = entry
        
    def _execute_calculation(self) -> None:
        """Fuehrt die Berechnung mit den eingegebenen Parametern aus."""
        if not self.current_plugin or not self.current_command:
            return
        
        # Parameter sammeln
        params = []
        
        for entry in self.param_entries:
            value = entry.get().strip()
            
            # Parameter in geeigneten Typ umwandeln
            try:
                if "." in value or "," in value:
                    value = float(value.replace(",", "."))
                else:
                    value = int(value)
            except ValueError:
                # Als String belassen, wenn keine Zahl
                pass
            
            params.append(value)
        
        try:
            # Befehl ausfuehren
            text, result = self.current_plugin.exec(self.current_command.name, params)
            
            # Zu Protokoll hinzufuegen
            self.calculation_log.add_calculation(text, str(result))
            
            # Protokollansicht aktualisieren
            self._update_log_view()
            
            # Eingabefelder leeren
            for entry in self.param_entries:
                entry.delete(0, tk.END)
            
            # Erstes Feld fokussieren
            if self.param_entries:
                self.param_entries[0].focus_set()
                self.current_entry = self.param_entries[0]
                
            # Feedback
            self.status_message(f"Berechnung erfolgreich: {text}", 3000)
            
        except Exception as e:
            messagebox.showerror("Fehler", str(e))
            
    def _update_log_view(self) -> None:
        """Aktualisiert die Anzeige des Berechnungsprotokolls."""
        # Listbox leeren
        self.log_listbox.delete(0, tk.END)
        
        # Protokoll abrufen
        calculations = self.calculation_log.get_calculations()
        
        # In umgekehrter Reihenfolge anzeigen (neueste zuerst)
        for calculation, result in calculations:
            if result:
                self.log_listbox.insert(tk.END, f"{calculation}: {result}")
            else:
                # Datumseintraege
                self.log_listbox.insert(tk.END, f"--- {calculation} ---")
        
        # Zum Anfang scrollen
        if self.log_listbox.size() > 0:
            self.log_listbox.see(0)
    
    # Neue Methoden fuer den Nebenrechner und Kontextmenues
    
    def _on_side_calc_result(self, result):
        """
        Wird aufgerufen, wenn im Nebenrechner ein Ergebnis berechnet wurde.
        
        Args:
            result: Das berechnete Ergebnis
        """
        # Protokolleintrag hinzufuegen
        self.calculation_log.add_calculation("Nebenrechnung", str(result))
        self._update_log_view()
    
    def _show_log_context_menu(self, event):
        """
        Zeigt das Kontextmenue fuer die Protokollliste an.
        
        Args:
            event: Das Ereignis, das den Aufruf ausgeloest hat
        """
        # Aktuelles Element unter dem Cursor auswaehlen
        index = self.log_listbox.nearest(event.y)
        if index >= 0:
            self.log_listbox.selection_clear(0, tk.END)
            self.log_listbox.selection_set(index)
            self.log_listbox.activate(index)
            
            # Menue anzeigen
            self.log_context_menu.tk_popup(event.x_root, event.y_root)
    
    def _copy_log_entry(self):
        """Kopiert den ausgewaehlten Protokolleintrag in die Zwischenablage."""
        selection = self.log_listbox.curselection()
        if not selection:
            return
        
        entry_text = self.log_listbox.get(selection[0])
        
        # Extrahiere nur den Zahlenwert nach dem ":"
        if ":" in entry_text:
            value = entry_text.split(":", 1)[1].strip()
        else:
            value = entry_text
        
        # In die Zwischenablage kopieren
        self.root.clipboard_clear()
        self.root.clipboard_append(value)
        
        # Feedback geben
        self.status_message("In Zwischenablage kopiert", 1500)
    
    def _insert_to_side_calc(self):
        """Fuegt den ausgewaehlten Protokolleintrag in den Nebenrechner ein."""
        selection = self.log_listbox.curselection()
        if not selection:
            return
        
        entry_text = self.log_listbox.get(selection[0])
        
        # Extrahiere nur den Zahlenwert nach dem ":"
        if ":" in entry_text:
            value = entry_text.split(":", 1)[1].strip()
        else:
            value = entry_text
        
        # In den Nebenrechner einfuegen
        self.side_calculator.insert_value(value)
    
    def _add_entry_context_menu(self, entry):
        """
        Fuegt einem Eingabefeld ein Kontextmenue hinzu.
        
        Args:
            entry: Das Eingabefeld
        """
        context_menu = tk.Menu(entry, tearoff=0)
        context_menu.add_command(label="Einfuegen", command=lambda: entry.event_generate('<<Paste>>'))
        context_menu.add_command(label="Aus Nebenrechner einfuegen", 
                               command=lambda: self._insert_side_calc_result_to_entry(entry))
        
        # Rechtsklick auf Eingabefeld
        entry.bind("<Button-3>", lambda e: context_menu.tk_popup(e.x_root, e.y_root))
    
    def _insert_side_calc_result_to_entry(self, entry):
        """
        Fuegt das Ergebnis des Nebenrechners in ein Eingabefeld ein.
        
        Args:
            entry: Das Eingabefeld
        """
        result = self.side_calculator.get_result()
        if result:
            # Aktuelle Cursor-Position
            current_pos = entry.index(tk.INSERT)
            entry.insert(current_pos, result)
    
    def _on_keypad_press(self, key: str) -> None:
        """
        Wird aufgerufen, wenn eine Taste auf dem Zahlenfeld gedrueckt wird.
        
        Args:
            key: Die gedrueckte Taste
        """
        if not self.current_entry:
            return
        
        if key == "C":
            # Aktuellen Inhalt loeschen
            self.current_entry.delete(0, tk.END)
        elif key == "CE":
            # Letztes Zeichen loeschen
            current_text = self.current_entry.get()
            if current_text:
                self.current_entry.delete(len(current_text) - 1, tk.END)
        elif key == "=":
            # Grundrechner-Ausdruck auswerten
            try:
                expression = self.current_entry.get()
                if not expression:
                    return
                
                # Plugin fuer Grundrechner holen
                basic_calc = None
                for name, plugin in self.plugin_manager.plugins.items():
                    if plugin.get_info().name.lower() == "grundrechner":
                        basic_calc = plugin
                        break
                
                if basic_calc:
                    calc_str, result = basic_calc.exec("Berechnung", [expression])
                    
                    # Ergebnis ins Eingabefeld setzen
                    self.current_entry.delete(0, tk.END)
                    self.current_entry.insert(0, str(result))
                    
                    # Zum Protokoll hinzufuegen
                    self.calculation_log.add_calculation(calc_str, str(result))
                    self._update_log_view()
                    
                    # Auch in den Nebenrechner einfuegen
                    self.side_calculator.entry_var.set(str(result))
            except Exception as e:
                messagebox.showerror("Fehler", str(e))
        else:
            # Zeichen einfuegen
            current_pos = self.current_entry.index(tk.INSERT)
            self.current_entry.insert(current_pos, key)
    
    # Weitere Anpassungen fuer den Dreiecksrechner
    def _create_triangle_input_area(self) -> None:
        """Erstellt den speziellen Eingabebereich fuer Dreiecksberechnungen."""
        # Triangle Input Panel erstellen
        self.triangle_panel = TriangleInputPanel(
            self.input_frame,
            on_calc_method_change=self._on_triangle_method_change,
            on_calculate=self._on_triangle_calculate
        )
        self.triangle_panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Kontextmenues zu allen Eingabefeldern hinzufuegen
        for param, widgets in self.triangle_panel.entries.items():
            entry = widgets["entry"]
            self._add_entry_context_menu(entry)
    
    def _on_triangle_method_change(self, method: str) -> None:
        """
        Wird aufgerufen, wenn die Berechnungsmethode fuer das Dreieck geaendert wird.
        
        Args:
            method: Die neue Berechnungsmethode
        """
        # Hier koennen weitere Aktionen bei aenderung der Methode erfolgen
        # z.B. Anzeige von Informationen zur Berechnungsmethode
        pass
    
    def _on_triangle_calculate(self, values: Dict[str, str]) -> None:
        """
        Wird aufgerufen, wenn die Berechnung des Dreiecks ausgefuehrt werden soll.
        
        Args:
            values: Die eingegebenen Werte fuer die Berechnung
        """
        if not self.current_plugin or not self.current_command:
            return
        
        try:
            # Parameter in die richtige Reihenfolge bringen
            params = [values["Berechnungsart"]]
            
            # Alle Parameter hinzufuegen (auch leere)
            for param in ["Seite a", "Seite b", "Seite c", 
                         "Winkel A (Grad)", "Winkel B (Grad)", "Winkel C (Grad)", 
                         "Hoehe h"]:
                params.append(values.get(param, ""))
            
            # Befehl ausfuehren
            text, result = self.current_plugin.exec(self.current_command.name, params)
            
            # Zu Protokoll hinzufuegen
            self.calculation_log.add_calculation(text, str(result))
            
            # Protokollansicht aktualisieren
            self._update_log_view()
            
            # Eingabefelder leeren
            self.triangle_panel.clear_entries()
            
            # Feedback
            self.status_message(f"Dreiecksberechnung erfolgreich", 3000)
            
        except Exception as e:
            messagebox.showerror("Fehler", str(e))
    
    # Status-Anzeige-Methode
    
    def status_message(self, message, duration=2000):
        """
        Zeigt eine temporaere Statusmeldung an.
        
        Args:
            message: Die anzuzeigende Nachricht
            duration: Anzeigedauer in Millisekunden
        """
        # Status-Label erstellen, falls noch nicht vorhanden
        if not hasattr(self, 'status_label'):
            self.status_label = ttk.Label(
                self.root,
                text="",
                relief=tk.SUNKEN,
                anchor=tk.W,
                font=("Arial", 10),
                background="#f0f0f0"
            )
            self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Nachricht anzeigen
        self.status_label.config(text=message)
        
        # Timer zum Ausblenden der Nachricht
        self.root.after(duration, lambda: self.status_label.config(text=""))