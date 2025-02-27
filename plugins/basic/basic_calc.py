# plugins/basic/basic_calc.py

from typing import List, Tuple, Any
from core.plugin_interface import IPlugin, PluginInfo, Command
import math

class BasicCalculator(IPlugin):
    """Implementiert den Grundrechner."""
    
    def __init__(self):
        """Initialisiert einen neuen Grundrechner."""
        self.name = "Grundrechner"
        self.commands = [
            Command("Berechnung", ["Ausdruck"])
        ]
    
    def load(self) -> None:
        """Laedt das Plugin."""
        pass
    
    def get_info(self) -> PluginInfo:
        """
        Gibt Informationen ueber das Plugin zurueck.
        
        Returns:
            PluginInfo: Informationen ueber das Plugin
        """
        return PluginInfo(self.name, self.commands)
    
    def exec(self, command_name: str, params: List[Any]) -> Tuple[str, Any]:
        """
        Fuehrt einen Befehl mit den gegebenen Parametern aus.
        
        Args:
            command_name: Name des auszufuehrenden Befehls
            params: Liste der Parameter

        Returns:
            Tuple[str, Any]: (Formatierter Text der Berechnung, Ergebniswert)
        """
        if command_name == "Berechnung":
            expression_str = str(params[0])
            
            # Zur Anzeige verwendete Ausdrucksform
            display_expr = expression_str.replace("*", "x").replace("/", ":")
            
            result = self._evaluate_expression(expression_str)
            
            # Runden auf 6 signifikante Stellen
            rounded_result = self._round_significant(result, 6)
            
            return f"NR: {display_expr} = {rounded_result}", rounded_result
        
        raise ValueError(f"Unbekannter Befehl: {command_name}")
    
    def _evaluate_expression(self, expression: str) -> float:
        """
        Wertet einen mathematischen Ausdruck aus.
        
        Args:
            expression: Der auszuwertende Ausdruck

        Returns:
            float: Das Ergebnis der Auswertung
        
        Raises:
            ValueError: Wenn der Ausdruck ungueltig ist
        """
        # Zeichen fuer Operatoren standardisieren
        expression = expression.replace("x", "*").replace(":", "/")
        
        # Leerzeichen entfernen
        expression = expression.replace(" ", "")
        
        # Pruefen, ob nur erlaubte Zeichen verwendet werden
        allowed_chars = set("0123456789.+-*/()eE")
        if not all(c in allowed_chars for c in expression):
            raise ValueError("Ungueltiger Ausdruck: Nur Ziffern und Operatoren (+, -, *, /, (, )) sind erlaubt")
        
        # Pruefen auf leeren Ausdruck
        if not expression:
            return 0
        
        try:
            # Sichere Auswertung des Ausdrucks
            return self._parse_expression(expression)
        except Exception as e:
            raise ValueError(f"Fehler bei der Berechnung: {str(e)}")
    
    def _parse_expression(self, expression: str) -> float:
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
    
    def _parse_add_sub(self, expression: str) -> float:
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
    
    def _parse_mul_div(self, expression: str) -> float:
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
    
    def _round_significant(self, value: float, digits: int) -> float:
        """
        Rundet einen Wert auf die angegebene Anzahl signifikanter Stellen.
        
        Args:
            value: Der zu rundende Wert
            digits: Anzahl der signifikanten Stellen

        Returns:
            float: Der gerundete Wert
        """
        if value == 0:
            return 0
        
        from math import log10, floor
        
        # Zehnerpotenz feststellen
        magnitude = floor(log10(abs(value)))
        
        # Runden auf die gewuenschte Anzahl signifikanter Stellen
        factor = 10 ** (digits - 1 - magnitude)
        return round(value * factor) / factor