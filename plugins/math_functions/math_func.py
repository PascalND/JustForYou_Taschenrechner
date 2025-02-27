# plugins/math_functions/math_func.py

from typing import List, Tuple, Any
from core.plugin_interface import IPlugin, PluginInfo, Command
import math

class MathFunctions(IPlugin):
    """Implementiert mathematische Funktionen."""
    
    def __init__(self):
        """Initialisiert neue mathematische Funktionen."""
        self.name = "Mathematische Funktionen"
        self.commands = [
            Command("Fakultaet", ["n"]),
            Command("Quadratwurzel", ["x"]),
            Command("Potenz", ["Basis", "Exponent"]),
            Command("Primzahlen", ["Untergrenze", "Obergrenze"]),
            Command("Dezimalbruch zu gemeinem Bruch", ["Dezimalbruch"])
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
        if command_name == "Fakultaet":
            # Fakultaet berechnen
            n = int(params[0])
            
            if n < 0:
                raise ValueError("Die Fakultaet ist nur fuer nicht-negative Zahlen definiert.")
            
            if n > 170:
                raise ValueError("Die Berechnung fuer n > 170 wuerde zu Speicherueberlauf fuehren.")
            
            ergebnis = self._fakultaet(n)
            
            return f"Fakultaet: {n}! = {ergebnis}", ergebnis
            
        elif command_name == "Quadratwurzel":
            # Quadratwurzel berechnen
            x = float(params[0])
            
            if x < 0:
                raise ValueError("Die Quadratwurzel ist nur fuer nicht-negative Zahlen definiert.")
            
            ergebnis = self._sqrt(x)
            
            # Runden auf 6 signifikante Stellen
            ergebnis = self._round_significant(ergebnis, 6)
            
            return f"Quadratwurzel: √{x} = {ergebnis}", ergebnis
            
        elif command_name == "Potenz":
            # Potenz berechnen
            basis = float(params[0])
            exponent = float(params[1])
            
            if basis == 0 and exponent <= 0:
                raise ValueError("0 hoch 0 oder negative Exponenten sind nicht definiert.")
            
            ergebnis = self._power(basis, exponent)
            
            # Runden auf 6 signifikante Stellen
            ergebnis = self._round_significant(ergebnis, 6)
            
            return f"Potenz: {basis}^{exponent} = {ergebnis}", ergebnis
            
        elif command_name == "Primzahlen":
            # Primzahlen in einem Bereich finden
            untergrenze = int(params[0])
            obergrenze = int(params[1])
            
            if untergrenze < 0 or obergrenze < 0:
                raise ValueError("Die Grenzen muessen nicht-negativ sein.")
            
            if untergrenze > obergrenze:
                raise ValueError("Die Untergrenze muss kleiner oder gleich der Obergrenze sein.")
            
            primzahlen = self._primzahlen(untergrenze, obergrenze)
            
            return (
                f"Primzahlen zwischen {untergrenze} und {obergrenze}: "
                f"{', '.join(map(str, primzahlen))}",
                primzahlen
            )
            
        elif command_name == "Dezimalbruch zu gemeinem Bruch":
            dezimalbruch_str = str(params[0])
            
            dezimalbruch_str = dezimalbruch_str.replace(',', '.')
            
            try:
                dezimalbruch = float(dezimalbruch_str)
                
                zaehler, nenner = self._decimal_to_fraction(dezimalbruch)
                
                return f"Gemeiner Bruch: {dezimalbruch} = {zaehler}/{nenner}", (zaehler, nenner)
            except ValueError:
                raise ValueError(f"Ungueltiger Dezimalbruch: {dezimalbruch_str}")
    
    def _fakultaet(self, n: int) -> int:
        """
        Berechnet die Fakultaet einer Zahl.
        
        Args:
            n: Die Zahl, deren Fakultaet berechnet werden soll

        Returns:
            int: Die Fakultaet von n
        """
        if n <= 1:
            return 1
        
        result = 1
        for i in range(2, n + 1):
            result *= i
        
        return result
    
    def _sqrt(self, x: float) -> float:
        """
        Berechnet die Quadratwurzel einer Zahl.
        
        Args:
            x: Die Zahl, deren Quadratwurzel berechnet werden soll

        Returns:
            float: Die Quadratwurzel von x
        """
        # Newton-Raphson-Verfahren zur Berechnung der Quadratwurzel
        if x == 0:
            return 0
        
        # Startwert
        y = x
        
        # Epsilon fuer Abbruchbedingung
        epsilon = 1e-10
        
        while True:
            # Neuer Naeherungswert
            y_new = 0.5 * (y + x / y)
            
            # Abbruchbedingung
            if abs(y - y_new) < epsilon:
                return y_new
            
            y = y_new
    
    def _power(self, basis: float, exponent: float) -> float:
        """
        Berechnet eine Potenz.
        
        Args:
            basis: Die Basis
            exponent: Der Exponent

        Returns:
            float: basis^exponent
        """
        # Fuer ganzzahlige Exponenten
        if exponent == int(exponent):
            exponent = int(exponent)
            
            if exponent >= 0:
                result = 1
                for _ in range(exponent):
                    result *= basis
                return result
            else:
                result = 1
                for _ in range(-exponent):
                    result *= basis
                return 1 / result
        
        # Fuer nicht-ganzzahlige Exponenten
        return math.exp(exponent * math.log(basis))
    
    def _ist_primzahl(self, n: int) -> bool:
        """
        Prueft, ob eine Zahl eine Primzahl ist.
        
        Args:
            n: Die zu pruefende Zahl

        Returns:
            bool: True, wenn n eine Primzahl ist, sonst False
        """
        if n <= 1:
            return False
        
        if n <= 3:
            return True
        
        if n % 2 == 0 or n % 3 == 0:
            return False
        
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        
        return True
    
    def _primzahlen(self, untergrenze: int, obergrenze: int) -> List[int]:
        """
        Findet alle Primzahlen in einem Bereich.
        
        Args:
            untergrenze: Die untere Grenze des Bereichs
            obergrenze: Die obere Grenze des Bereichs

        Returns:
            List[int]: Liste der Primzahlen im Bereich
        """
        primzahlen = []
        
        for n in range(max(2, untergrenze), obergrenze + 1):
            if self._ist_primzahl(n):
                primzahlen.append(n)
        
        return primzahlen
    
    def _gcd(self, a: int, b: int) -> int:
        """
        Berechnet den groessten gemeinsamen Teiler.
        
        Args:
            a: Erste Zahl
            b: Zweite Zahl

        Returns:
            int: Der groesste gemeinsame Teiler von a und b
        """
        while b:
            a, b = b, a % b
        return a
    
    def _decimal_to_fraction(self, dezimalbruch: float) -> Tuple[int, int]:
        """
        Wandelt einen Dezimalbruch in einen gemeinen Bruch um.
        
        Args:
            dezimalbruch: Der umzuwandelnde Dezimalbruch

        Returns:
            Tuple[int, int]: (Zaehler, Nenner)
        """
        # Vorzeichenbehandlung
        sign = 1 if dezimalbruch >= 0 else -1
        dezimalbruch = abs(dezimalbruch)
        
        # Ganzzahligen Teil extrahieren
        ganzzahl = int(dezimalbruch)
        nachkomma = dezimalbruch - ganzzahl
        
        # Abbruch, wenn es keine Nachkommastellen gibt
        if nachkomma == 0:
            return sign * ganzzahl, 1

        common_fractions = {
            0.25: (1, 4),
            0.33: (1, 3),
            0.333: (1, 3),
            0.5: (1, 2),
            0.75: (3, 4),
            0.2: (1, 5),
            0.4: (2, 5),
            0.6: (3, 5),
            0.8: (4, 5),
            0.125: (1, 8),
            0.375: (3, 8),
            0.625: (5, 8),
            0.875: (7, 8),
            0.33333333: (1, 3),
            0.66666667: (2, 3),
            0.16666667: (1, 6),
            0.83333333: (5, 6),
            0.11111111: (1, 9),
            0.22222222: (2, 9),
            0.44444444: (4, 9),
            0.55555556: (5, 9),
            0.77777778: (7, 9),
            0.88888889: (8, 9)
        }
        
        # Rundungsfehler tolerieren
        for value, fraction in common_fractions.items():
            if abs(nachkomma - value) < 1e-6:
                z, n = fraction
                return sign * (ganzzahl * n + z), n
        
        # Umwandlung in Bruch mit Kettenbruch-Approximation
        max_nenner = 1000000  # Maximaler Nenner
        
        # Kontinuierliche Bruch-Approximation
        h1, h2 = 1, 0
        k1, k2 = 0, 1
        b = dezimalbruch
        
        while k1 < max_nenner:
            a = int(b)
            aux = h1
            h1 = a * h1 + h2
            h2 = aux
            aux = k1
            k1 = a * k1 + k2
            k2 = aux
            b = 1 / (b - a) if b - a != 0 else 0
            
            if abs(dezimalbruch - h1 / k1) < 1e-10:
                break
        
        zaehler = ganzzahl * k1 + h1
        nenner = k1

        return sign * h1, k1
    
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
        
        # Feststellen der Zehnerpotenz
        magnitude = floor(log10(abs(value)))
        
        # Runden auf die gewuenschte Anzahl signifikanter Stellen
        factor = 10 ** (digits - 1 - magnitude)
        return round(value * factor) / factor