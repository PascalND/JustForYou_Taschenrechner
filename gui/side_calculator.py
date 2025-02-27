import tkinter as tk
from tkinter import ttk
import math
import re

class SideCalculator(ttk.Frame):
    """Ein einfacher Taschenrechner fuer Nebenrechnungen."""
    
    def __init__(self, parent, on_result_available=None):
        """
        Initialisiert einen neuen Nebenrechner.
        
        Args:
            parent: Das Elternelement des Widgets
            on_result_available: Callback wenn ein Ergebnis berechnet wurde
        """
        super().__init__(parent)
        self.on_result_available = on_result_available
        
        # Erstelle das Layout
        self._create_layout()
        
        # Historie der Berechnungen
        self.calculation_history = []
        self.history_index = -1
    
    def _create_layout(self):
        """Erstellt das Layout des Nebenrechners."""
        # Hauptcontainer
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)  # Eingabefeld
        self.rowconfigure(1, weight=1)  # Ergebnisanzeige
        
        # Oberer Bereich: Eingabefeld und Buttons
        input_frame = ttk.Frame(self)
        input_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        input_frame.columnconfigure(0, weight=1)
        
        # Eingabefeld
        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(
            input_frame, 
            textvariable=self.entry_var, 
            font=("Arial", 11)
        )
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=0, column=1, sticky="e")
        
        calculate_btn = ttk.Button(
            button_frame, 
            text="=", 
            command=self._calculate,
            width=3
        )
        calculate_btn.pack(side=tk.LEFT, padx=2)
        
        clear_btn = ttk.Button(
            button_frame, 
            text="C", 
            command=self._clear_entry,
            width=3
        )
        clear_btn.pack(side=tk.LEFT, padx=2)
        
        # Tastatureingaben abfangen
        self.entry.bind("<Return>", lambda e: self._calculate())
        self.entry.bind("<Escape>", lambda e: self._clear_entry())
        self.entry.bind("<Up>", lambda e: self._navigate_history(-1))
        self.entry.bind("<Down>", lambda e: self._navigate_history(1))
        
        # Unterer Bereich: Ergebnisanzeige
        result_frame = ttk.LabelFrame(self, text="Ergebnisse")
        result_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Ergebnisanzeige mit Scrollbar
        result_container = ttk.Frame(result_frame)
        result_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.result_list = tk.Listbox(
            result_container,
            font=("Arial", 11),
            activestyle="none",
            highlightthickness=0,
            bd=1
        )
        scrollbar = ttk.Scrollbar(
            result_container, 
            orient="vertical", 
            command=self.result_list.yview
        )
        self.result_list.configure(yscrollcommand=scrollbar.set)
        
        self.result_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Kontextmenue fuer Kopieren
        self.context_menu = tk.Menu(self.result_list, tearoff=0)
        self.context_menu.add_command(label="Kopieren", command=self._copy_result)
        self.context_menu.add_command(label="In Berechnung einfuegen", command=self._insert_result)
        
        # Rechtsklick auf Ergebnisliste
        self.result_list.bind("<Button-3>", self._show_context_menu)
        # Doppelklick fuer schnelles Kopieren
        self.result_list.bind("<Double-Button-1>", lambda e: self._copy_result())
    
    def _calculate(self):
        """Berechnet den aktuellen Ausdruck."""
        expression = self.entry_var.get().strip()
        if not expression:
            return
        
        # Operatoren standardisieren
        expression = expression.replace("x", "*").replace(":", "/")
        
        try:
            # Fuehre die Berechnung aus
            result = self._evaluate_expression(expression)
            
            # Anzeige formatieren (Operatoren zurueck in Anzeigeformat)
            display_expr = expression.replace("*", "x").replace("/", ":")
            
            # Zum Protokoll hinzufuegen
            formatted_result = f"{display_expr} = {result}"
            self.result_list.insert(0, formatted_result)
            self.calculation_history.insert(0, expression)
            
            # Reset Historie-Index
            self.history_index = -1
            
            # Callback, falls vorhanden
            if self.on_result_available:
                self.on_result_available(result)
            
            # Eingabefeld leeren
            self.entry_var.set("")
            
        except Exception as e:
            # Fehler anzeigen
            error_msg = f"Fehler: {str(e)}"
            self.result_list.insert(0, error_msg)
            
        # Scrolle nach oben
        self.result_list.see(0)
    
    def _evaluate_expression(self, expression):
        """
        Wertet einen mathematischen Ausdruck aus.
        
        Args:
            expression: Der auszuwertende Ausdruck

        Returns:
            float: Das Ergebnis der Berechnung
        """
        # ueberpruefe auf gueltige Zeichen
        if not re.match(r'^[0-9\s\+\-\*\/\(\)\.\,eE]+$', expression):
            raise ValueError("Ungueltige Zeichen im Ausdruck")
        
        # Komma durch Punkt ersetzen
        expression = expression.replace(",", ".")
        
        # Sicherheitscheck: Keine gefaehrlichen Funktionen
        if "eval" in expression or "exec" in expression or "__" in expression:
            raise ValueError("Unerlaubter Ausdruck")
        
        # Sichere Auswertung ohne eval
        # Hier koennten wir ein eigenes Parsing implementieren, aber fuer die
        # Einfachheit verwenden wir den bestehenden Parser aus basic_calc.py
        
        # Vereinfachtes Parsing fuer grundlegende Berechnungen
        # Dies ist eine vereinfachte Version - eine vollstaendige
        # Implementierung wuerde den Rahmen sprengen
        
        # Entferne alle Leerzeichen
        expression = expression.replace(" ", "")
        
        return self._parse_expression(expression)
    
    def _parse_expression(self, expression):
        """
        Parst und wertet einen Ausdruck rekursiv aus.
        
        Args:
            expression: Der zu parsende Ausdruck

        Returns:
            float: Das Ergebnis der Auswertung
        """
        # Leerer Ausdruck
        if not expression:
            return 0
        
        # Auswertung von Klammerausdruecken
        idx = 0
        while idx < len(expression):
            if expression[idx] == '(':
                # Klammern suchen
                bracket_count = 1
                start_idx = idx
                idx += 1
                
                while idx < len(expression) and bracket_count > 0:
                    if expression[idx] == '(':
                        bracket_count += 1
                    elif expression[idx] == ')':
                        bracket_count -= 1
                    idx += 1
                
                if bracket_count != 0:
                    raise ValueError("Unbalancierte Klammern")
                
                # Subausdruck extrahieren und auswerten
                sub_expr = expression[start_idx+1:idx-1]
                sub_result = self._parse_expression(sub_expr)
                
                # Subausdruck durch sein Ergebnis ersetzen
                expression = expression[:start_idx] + str(sub_result) + expression[idx:]
                
                # Index zuruecksetzen
                idx = 0
            else:
                idx += 1
        
        # Addition und Subtraktion auswerten
        return self._parse_add_sub(expression)
    
    def _parse_add_sub(self, expression):
        """
        Wertet Addition und Subtraktion aus.
        
        Args:
            expression: Der auszuwertende Ausdruck

        Returns:
            float: Das Ergebnis der Auswertung
        """
        terms = []
        operators = []
        current_term = ""
        i = 0
        
        # Negative Zahl am Anfang behandeln
        if expression.startswith("-"):
            expression = "0" + expression
        
        while i < len(expression):
            char = expression[i]
            
            if char in "+-" and i > 0 and expression[i-1] not in "+-*/":
                terms.append(current_term)
                operators.append(char)
                current_term = ""
            else:
                current_term += char
            
            i += 1
        
        # Letzten Term hinzufuegen
        if current_term:
            terms.append(current_term)
        
        # Multiplikation und Division fuer jeden Term auswerten
        results = [self._parse_mul_div(term) for term in terms]
        
        # Addition und Subtraktion anwenden
        result = results[0]
        for i in range(len(operators)):
            if operators[i] == "+":
                result += results[i+1]
            else:  # "-"
                result -= results[i+1]
        
        return result
    
    def _parse_mul_div(self, expression):
        """
        Wertet Multiplikation und Division aus.
        
        Args:
            expression: Der auszuwertende Ausdruck

        Returns:
            float: Das Ergebnis der Auswertung
        """
        factors = []
        operators = []
        current_factor = ""
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            if char in "*/" and i > 0:
                factors.append(current_factor)
                operators.append(char)
                current_factor = ""
            else:
                current_factor += char
            
            i += 1
        
        # Letzten Faktor hinzufuegen
        if current_factor:
            factors.append(current_factor)
        
        # Faktoren in Zahlen umwandeln
        numbers = []
        for factor in factors:
            try:
                numbers.append(float(factor))
            except ValueError:
                raise ValueError(f"Ungueltiger Wert: {factor}")
        
        # Multiplikation und Division anwenden
        result = numbers[0]
        for i in range(len(operators)):
            if operators[i] == "*":
                result *= numbers[i+1]
            else:  # "/"
                if numbers[i+1] == 0:
                    raise ValueError("Division durch Null")
                result /= numbers[i+1]
        
        return result
    
    def _clear_entry(self):
        """Leert das Eingabefeld."""
        self.entry_var.set("")
        self.entry.focus()
    
    def _navigate_history(self, direction):
        """
        Navigiert durch die Historie der Berechnungen.
        
        Args:
            direction: Richtung (-1 fuer aufwaerts, 1 fuer abwaerts)
        """
        if not self.calculation_history:
            return
        
        new_index = self.history_index + direction
        
        if new_index >= 0 and new_index < len(self.calculation_history):
            self.history_index = new_index
            self.entry_var.set(self.calculation_history[new_index])
            self.entry.icursor(tk.END)  # Cursor ans Ende setzen
        elif new_index < 0:
            # Unterhalb der Historie -> leeres Feld
            self.history_index = -1
            self.entry_var.set("")
    
    def _show_context_menu(self, event):
        """
        Zeigt das Kontextmenue fuer die Ergebnisliste an.
        
        Args:
            event: Das Ereignis, das den Aufruf ausgeloest hat
        """
        # Aktuelles Element unter dem Cursor auswaehlen
        index = self.result_list.nearest(event.y)
        if index >= 0:
            self.result_list.selection_clear(0, tk.END)
            self.result_list.selection_set(index)
            self.result_list.activate(index)
            
            # Menue anzeigen
            self.context_menu.tk_popup(event.x_root, event.y_root)
    
    def _copy_result(self):
        """Kopiert das ausgewaehlte Ergebnis in die Zwischenablage."""
        selection = self.result_list.curselection()
        if not selection:
            return
        
        result_text = self.result_list.get(selection[0])
        
        # Extrahiere nur den Zahlenwert nach dem "="
        if "=" in result_text:
            value = result_text.split("=")[1].strip()
        else:
            value = result_text
        
        # In die Zwischenablage kopieren
        self.clipboard_clear()
        self.clipboard_append(value)
    
    def _insert_result(self):
        """Fuegt das ausgewaehlte Ergebnis in das Eingabefeld ein."""
        selection = self.result_list.curselection()
        if not selection:
            return
        
        result_text = self.result_list.get(selection[0])
        
        # Extrahiere nur den Zahlenwert nach dem "="
        if "=" in result_text:
            value = result_text.split("=")[1].strip()
            
            # Hinzufuegen zum aktuellen Eingabefeld
            current_pos = self.entry.index(tk.INSERT)
            self.entry.insert(current_pos, value)
            self.entry.focus()
    
    def insert_value(self, value):
        """
        Fuegt einen Wert ins Eingabefeld ein.
        
        Args:
            value: Der einzufuegende Wert
        """
        current_text = self.entry_var.get()
        cursor_pos = self.entry.index(tk.INSERT)
        
        new_text = current_text[:cursor_pos] + str(value) + current_text[cursor_pos:]
        self.entry_var.set(new_text)
        
        # Cursor nach dem eingefuegten Wert positionieren
        self.entry.icursor(cursor_pos + len(str(value)))
        self.entry.focus()
    
    def get_result(self):
        """
        Gibt das letzte Ergebnis zurueck, falls vorhanden.
        
        Returns:
            str: Das letzte Ergebnis oder None, wenn kein Ergebnis vorhanden
        """
        if self.result_list.size() > 0:
            result_text = self.result_list.get(0)
            if "=" in result_text:
                return result_text.split("=")[1].strip()
        return None