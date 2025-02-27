# gui/triangle_input.py

import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional, Callable

class TriangleInputPanel(ttk.Frame):
    """Panel fuer die dynamische Eingabe von Dreiecksparametern."""
    
    def __init__(self, parent, on_calc_method_change=None, on_calculate=None):
        """
        Initialisiert ein neues Panel fuer Dreiecksberechnungen.
        
        Args:
            parent: Das Elternelement des Panels
            on_calc_method_change: Callback bei aenderung der Berechnungsmethode
            on_calculate: Callback bei Klick auf Berechnen-Button
        """
        super().__init__(parent)
        self.on_calc_method_change = on_calc_method_change
        self.on_calculate = on_calculate
        self.entries = {}  # Speichert alle Eingabefelder
        
        # Verfuegbare Berechnungsmethoden
        self.calc_methods = [
            "SSS (drei Seiten)",
            "SWS (zwei Seiten, ein Winkel)",
            "WSW (zwei Winkel, eine Seite)",
            "SSW (zwei Seiten, gegenueberliegender Winkel)",
            "Grundseite und Hoehe"
        ]
        
        # Parameter-Definitionen fuer jede Methode
        self.method_params = {
            "SSS (drei Seiten)": ["Seite a", "Seite b", "Seite c"],
            "SWS (zwei Seiten, ein Winkel)": ["Seite a", "Seite b", "Winkel C (Grad)"],
            "WSW (zwei Winkel, eine Seite)": ["Winkel A (Grad)", "Seite c", "Winkel B (Grad)"],
            "SSW (zwei Seiten, gegenueberliegender Winkel)": ["Seite a", "Seite b", "Winkel C (Grad)"],
            "Grundseite und Hoehe": ["Seite a", "Hoehe h"]
        }
        
        # Alle moeglichen Parameter
        self.all_params = [
            "Seite a", "Seite b", "Seite c", 
            "Winkel A (Grad)", "Winkel B (Grad)", "Winkel C (Grad)", 
            "Hoehe h"
        ]
        
        self._create_layout()
    
    def _create_layout(self):
        """Erstellt das Layout des Panels."""
        # Hauptcontainer mit zwei Spalten
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
        # Berechnungsmethode-Auswahl
        method_frame = ttk.LabelFrame(self, text="Berechnungsmethode")
        method_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        self.method_var = tk.StringVar(value=self.calc_methods[0])
        method_combo = ttk.Combobox(
            method_frame, 
            textvariable=self.method_var,
            values=self.calc_methods,
            state="readonly",
            font=("Arial", 11)
        )
        method_combo.pack(fill=tk.X, padx=10, pady=10)
        method_combo.bind("<<ComboboxSelected>>", self._on_method_change)
        
        # Eingabefelder-Container
        inputs_frame = ttk.LabelFrame(self, text="Parameter")
        inputs_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Erstellen aller moeglichen Eingabefelder
        for i, param in enumerate(self.all_params):
            row = i // 2
            col = i % 2
            
            param_frame = ttk.Frame(inputs_frame)
            param_frame.grid(row=row, column=col, sticky="ew", padx=10, pady=5)
            
            label = ttk.Label(param_frame, text=f"{param}:", width=12, anchor="e")
            label.pack(side=tk.LEFT, padx=(0, 5))
            
            entry = ttk.Entry(param_frame)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Eintrag speichern
            self.entries[param] = {
                "frame": param_frame,
                "label": label,
                "entry": entry
            }
        
        # Berechnen-Button
        calculate_btn = ttk.Button(
            self, 
            text="Berechnen",
            command=self._on_calculate,
            padding=10,
            style='Big.TButton'
        )
        calculate_btn.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        # Initialen Zustand setzen
        self._update_input_fields()
    
    def _on_method_change(self, event):
        """
        Wird aufgerufen, wenn die Berechnungsmethode geaendert wird.
        
        Args:
            event: Das Ereignis, das den Aufruf ausgeloest hat
        """
        self._update_input_fields()
        
        if self.on_calc_method_change:
            self.on_calc_method_change(self.method_var.get())
    
    def _update_input_fields(self):
        """Aktualisiert die Eingabefelder basierend auf der aktuellen Berechnungsmethode."""
        current_method = self.method_var.get()
        required_params = self.method_params.get(current_method, [])
        
        # Alle Felder durchgehen
        for param, widgets in self.entries.items():
            if param in required_params:
                # Feld aktivieren
                widgets["frame"].grid()
                widgets["entry"].config(state="normal")
                widgets["label"].config(foreground="black")
            else:
                # Feld deaktivieren/ausgrauen
                widgets["entry"].delete(0, tk.END)  # Inhalt loeschen
                widgets["entry"].config(state="disabled")
                widgets["label"].config(foreground="gray")
    
    def _on_calculate(self):
        """Wird aufgerufen, wenn der Berechnen-Button gedrueckt wird."""
        if self.on_calculate:
            # Werte sammeln
            values = {}
            values["Berechnungsart"] = self.method_var.get()
            
            current_method = self.method_var.get()
            required_params = self.method_params.get(current_method, [])
            
            # Alle Parameter sammeln (benoetigt und nicht benoetigt)
            for param in self.all_params:
                entry = self.entries[param]["entry"]
                if param in required_params:
                    value = entry.get().strip()
                    if not value:
                        # Fehlende Eingabe fuer benoetigten Parameter
                        return
                else:
                    value = ""  # Leerer Wert fuer nicht benoetigte Parameter
                
                values[param] = value
            
            # Callback mit allen Werten aufrufen
            self.on_calculate(values)
    
    def get_values(self) -> Dict[str, str]:
        """
        Gibt die aktuellen Werte aller Eingabefelder zurueck.
        
        Returns:
            Dict[str, str]: Die Eingabewerte
        """
        values = {}
        values["Berechnungsart"] = self.method_var.get()
        
        for param in self.all_params:
            entry = self.entries[param]["entry"]
            values[param] = entry.get().strip()
        
        return values
    
    def clear_entries(self):
        """Leert alle Eingabefelder."""
        for widgets in self.entries.values():
            entry = widgets["entry"]
            if entry["state"] != "disabled":
                entry.delete(0, tk.END)