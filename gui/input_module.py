# gui/input_module.py

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional, Any, Callable, Tuple

from gui.theme_manager import ThemeManager

class CalculatorKeypad(ttk.Frame):
    """Tastatur-Widget fuer den Taschenrechner."""
    
    def __init__(self, parent, on_key_press=None):
        """
        Initialisiert ein neues Tastatur-Widget.
        
        Args:
            parent: Das Elternelement des Widgets
            on_key_press: Callback-Funktion fuer Tastendruecke
        """
        super().__init__(parent)
        self.on_key_press = on_key_press
        
        # Tastenanordnung
        keypad_buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "C", "+"],
            ["(", ")", "CE", "="]
        ]
        
        # Tasten erstellen
        for row_idx, row in enumerate(keypad_buttons):
            for col_idx, key in enumerate(row):
                button = ttk.Button(
                    self,
                    text=key,
                    width=3,
                    command=lambda k=key: self._on_button_press(k)
                )
                button.grid(row=row_idx, column=col_idx, padx=2, pady=2, sticky="nsew")
            
            self.rowconfigure(row_idx, weight=1)
        
        for col_idx in range(4):
            self.columnconfigure(col_idx, weight=1)
    
    def _on_button_press(self, key):
        """
        Wird aufgerufen, wenn eine Taste gedrueckt wird.
        
        Args:
            key: Die gedrueckte Taste
        """
        if self.on_key_press:
            self.on_key_press(key)

class ParameterInputPanel(ttk.Frame):
    """Panel fuer die Eingabe von Parametern."""
    
    def __init__(self, parent, param_names, on_calculate=None, on_side_calc_result=None):
        """
        Initialisiert ein neues Eingabepanel.
        
        Args:
            parent: Das Elternelement des Panels
            param_names: Die Namen der Parameter
            on_calculate: Callback-Funktion fuer die Berechnung
            on_side_calc_result: Callback-Funktion fuer die uebernahme von Nebenrechnungen
        """
        super().__init__(parent)
        self.param_names = param_names
        self.on_calculate = on_calculate
        self.on_side_calc_result = on_side_calc_result
        self.entries = []
        self.current_entry = None
        
        self._create_layout()
    
    def _create_layout(self):
        """Erstellt das Layout des Panels."""
        # Grid-Konfiguration
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        
        # Parameter-Eingabefelder
        for i, param_name in enumerate(self.param_names):
            label = ttk.Label(self, text=f"{param_name}:", anchor="e")
            label.grid(row=i, column=0, padx=(5, 10), pady=5, sticky="e")
            
            entry = ttk.Entry(self)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            entry.bind("<FocusIn>", lambda e, ent=entry: self._on_entry_focus(ent))
            
            self.entries.append(entry)
        
        # Keypad
        keypad_frame = ttk.LabelFrame(self, text="Rechner")
        keypad_frame.grid(row=len(self.param_names), column=0, columnspan=2, padx=5, pady=10, sticky="nsew")
        
        self.keypad = CalculatorKeypad(keypad_frame, on_key_press=self._on_keypad_press)
        self.keypad.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Berechnen-Button
        calculate_btn = ttk.Button(
            self, 
            text="Berechnen",
            command=self._on_calculate,
            padding=10
        )
        calculate_btn.grid(row=len(self.param_names) + 1, column=0, columnspan=2, padx=5, pady=10, sticky="ew")
        
        # Anfangs das erste Eingabefeld fokussieren
        if self.entries:
            self.entries[0].focus_set()
            self.current_entry = self.entries[0]
    
    def _on_entry_focus(self, entry):
        """
        Wird aufgerufen, wenn ein Eingabefeld den Fokus erhaelt.
        
        Args:
            entry: Das fokussierte Eingabefeld
        """
        self.current_entry = entry
    
    def _on_keypad_press(self, key):
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
            # Grundrechner-Ausdruck auswerten und Ergebnis uebernehmen
            if self.on_side_calc_result:
                expression = self.current_entry.get()
                if expression:
                    self.on_side_calc_result(expression, self.current_entry)
        else:
            # Zeichen einfuegen
            current_pos = self.current_entry.index(tk.INSERT)
            self.current_entry.insert(current_pos, key)
    
    def _on_calculate(self):
        """Wird aufgerufen, wenn der Berechnen-Button gedrueckt wird."""
        if self.on_calculate:
            # Parameter sammeln
            params = []
            errors = []
            
            for i, entry in enumerate(self.entries):
                value = entry.get().strip()
                
                if not value:
                    errors.append(f"Bitte geben Sie einen Wert fuer '{self.param_names[i]}' ein.")
                    continue
                
                try:
                    # Umwandlung in Zahl
                    if "." in value or "," in value:
                        value = value.replace(",", ".")
                        value = float(value)
                    else:
                        value = int(value)
                    
                    params.append(value)
                except ValueError:
                    errors.append(f"'{value}' ist keine gueltige Zahl fuer '{self.param_names[i]}'.")
            
            if errors:
                messagebox.showerror("Fehler", "\n".join(errors))
                return
            
            self.on_calculate(params)
    
    def clear_entries(self):
        """Leert alle Eingabefelder."""
        for entry in self.entries:
            entry.delete(0, tk.END)
        
        # Erstes Feld fokussieren
        if self.entries:
            self.entries[0].focus_set()
            self.current_entry = self.entries[0]
    
    def get_values(self) -> List[Any]:
        """
        Gibt die eingegebenen Werte zurueck.
        
        Returns:
            List[Any]: Die eingegebenen Werte
        """
        values = []
        
        for entry in self.entries:
            value = entry.get().strip()
            
            if "." in value or "," in value:
                value = value.replace(",", ".")
                try:
                    value = float(value)
                except ValueError:
                    value = value
            else:
                try:
                    value = int(value)
                except ValueError:
                    value = value
            
            values.append(value)
        
        return values