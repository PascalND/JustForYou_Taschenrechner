# plugins/geometry/geometry_calc.py

from typing import List, Tuple, Any, Dict, Optional
from core.plugin_interface import IPlugin, PluginInfo, Command
import math

class GeometryCalculator(IPlugin):
    """Implementiert den Geometrierechner."""
    
    def __init__(self):
        """Initialisiert einen neuen Geometrierechner."""
        self.name = "Geometrie"
        self.commands = [
            # Universeller Dreiecksrechner
            Command("Dreieck", ["Berechnungsart", "Seite a", "Seite b", "Seite c", "Winkel A (Grad)", "Winkel B (Grad)", "Winkel C (Grad)", "Hoehe h"]),
            # Weitere Geometrie-Funktionen
            Command("Kreis", ["Radius"]),
            Command("Parallelogramm", ["Seite a", "Seite b", "Hoehe h"])
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
        if command_name == "Dreieck":
            # Dreiecksberechnung mit flexibler Eingabe
            berechnungsart = str(params[0])
            
            # Extrahieren der Parameter
            # Werte koennen leer oder ungueltig sein, je nach Berechnungsart
            try:
                seite_a = float(params[1]) if params[1] else None
            except ValueError:
                seite_a = None
                
            try:
                seite_b = float(params[2]) if params[2] else None
            except ValueError:
                seite_b = None
                
            try:
                seite_c = float(params[3]) if params[3] else None
            except ValueError:
                seite_c = None
                
            try:
                winkel_a = float(params[4]) if params[4] else None
            except ValueError:
                winkel_a = None
                
            try:
                winkel_b = float(params[5]) if params[5] else None
            except ValueError:
                winkel_b = None
                
            try:
                winkel_c = float(params[6]) if params[6] else None
            except ValueError:
                winkel_c = None
                
            try:
                hoehe_h = float(params[7]) if params[7] else None
            except ValueError:
                hoehe_h = None
            
            # Je nach Berechnungsart die entsprechende Methode aufrufen
            if berechnungsart == "SSS (drei Seiten)":
                if seite_a is None or seite_b is None or seite_c is None:
                    raise ValueError("Fuer die SSS-Methode werden alle drei Seiten benoetigt.")
                return self._calculate_triangle_sss(seite_a, seite_b, seite_c)
                
            elif berechnungsart == "SWS (zwei Seiten, ein Winkel)":
                if seite_a is None or seite_b is None or winkel_c is None:
                    raise ValueError("Fuer die SWS-Methode werden zwei Seiten und der eingeschlossene Winkel benoetigt.")
                return self._calculate_triangle_sws(seite_a, winkel_c, seite_b)
                
            elif berechnungsart == "WSW (zwei Winkel, eine Seite)":
                if winkel_a is None or seite_c is None or winkel_b is None:
                    raise ValueError("Fuer die WSW-Methode werden zwei Winkel und die eingeschlossene Seite benoetigt.")
                return self._calculate_triangle_wsw(winkel_a, seite_c, winkel_b)
                
            elif berechnungsart == "SSW (zwei Seiten, gegenueberliegender Winkel)":
                if seite_a is None or seite_b is None or winkel_c is None:
                    raise ValueError("Fuer die SSW-Methode werden zwei Seiten und der gegenueberliegende Winkel benoetigt.")
                return self._calculate_triangle_ssw(seite_a, seite_b, winkel_c)
                
            elif berechnungsart == "Grundseite und Hoehe":
                # Annahme: Seite a ist die Grundseite und Hoehe h ist gegeben
                if seite_a is None or hoehe_h is None:
                    raise ValueError("Fuer diese Methode werden Grundseite und Hoehe benoetigt.")
                return self._calculate_triangle_base_height(seite_a, hoehe_h)
                
            else:
                raise ValueError(f"Unbekannte Berechnungsart: {berechnungsart}")
            
        # Andere Geometrie-Funktionen
        elif command_name == "Kreis":
            # Berechnung von Umfang und Flaecheninhalt eines Kreises
            radius = float(params[0])
            
            if radius <= 0:
                raise ValueError("Der Radius muss positiv sein.")
            
            # Umfang
            umfang = 2 * math.pi * radius
            
            # Flaecheninhalt
            flaeche = math.pi * radius ** 2
            
            # Runden auf 6 signifikante Stellen
            umfang = self._round_significant(umfang, 6)
            flaeche = self._round_significant(flaeche, 6)
            
            return (
                f"Geometrie Kreis: r={radius} → "
                f"Umfang={umfang}, Flaeche={flaeche}",
                (umfang, flaeche)
            )
            
        elif command_name == "Parallelogramm":
            # Berechnung von Umfang und Flaecheninhalt eines Parallelogramms
            a = float(params[0])
            b = float(params[1])
            h = float(params[2])
            
            if a <= 0 or b <= 0 or h <= 0:
                raise ValueError("Alle Werte muessen positiv sein.")
            
            if h > a and h > b:
                raise ValueError("Die Hoehe kann nicht groesser als beide Seiten sein.")
            
            # Umfang
            umfang = 2 * (a + b)
            
            # Flaecheninhalt
            flaeche = a * h
            
            # Runden auf 6 signifikante Stellen
            umfang = self._round_significant(umfang, 6)
            flaeche = self._round_significant(flaeche, 6)
            
            return (
                f"Geometrie Parallelogramm: a={a}, b={b}, h={h} → "
                f"Umfang={umfang}, Flaeche={flaeche}",
                (umfang, flaeche)
            )
        
        raise ValueError(f"Unbekannter Befehl: {command_name}")
    
    def _calculate_triangle_sss(self, a: float, b: float, c: float) -> Tuple[str, Dict[str, float]]:
        """
        Berechnet alle Daten eines Dreiecks aus drei Seiten (SSS).
        
        Args:
            a: Seite a
            b: Seite b
            c: Seite c
            
        Returns:
            Tuple[str, Dict[str, float]]: (Formatierter Text, Ergebniswerte)
        """
        # Pruefen, ob ein Dreieck konstruierbar ist
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError("Alle Seiten muessen positiv sein.")
            
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError(
                "Die Summe von zwei Seiten muss groesser als die dritte Seite sein (Dreiecksungleichung)."
            )
        
        # Umfang
        umfang = a + b + c
        
        # Flaecheninhalt nach Heronsche Formel
        s = umfang / 2  # Halbumfang
        flaeche = math.sqrt(s * (s - a) * (s - b) * (s - c))
        
        # Winkel berechnen (Kosinussatz)
        alpha_rad = math.acos((b**2 + c**2 - a**2) / (2 * b * c))
        beta_rad = math.acos((a**2 + c**2 - b**2) / (2 * a * c))
        gamma_rad = math.acos((a**2 + b**2 - c**2) / (2 * a * b))
        
        # Umrechnung in Grad
        alpha_deg = math.degrees(alpha_rad)
        beta_deg = math.degrees(beta_rad)
        gamma_deg = math.degrees(gamma_rad)
        
        # Hoehen berechnen
        ha = 2 * flaeche / a
        hb = 2 * flaeche / b
        hc = 2 * flaeche / c
        
        # Inkreisradius
        inradius = flaeche / s
        
        # Umkreisradius
        umkreisradius = (a * b * c) / (4 * flaeche)
        
        # Ergebnisse runden
        results = {
            "a": self._round_significant(a, 6),
            "b": self._round_significant(b, 6),
            "c": self._round_significant(c, 6),
            "umfang": self._round_significant(umfang, 6),
            "flaeche": self._round_significant(flaeche, 6),
            "alpha_grad": self._round_significant(alpha_deg, 6),
            "beta_grad": self._round_significant(beta_deg, 6),
            "gamma_grad": self._round_significant(gamma_deg, 6),
            "hoehe_a": self._round_significant(ha, 6),
            "hoehe_b": self._round_significant(hb, 6),
            "hoehe_c": self._round_significant(hc, 6),
            "inkreisradius": self._round_significant(inradius, 6),
            "umkreisradius": self._round_significant(umkreisradius, 6)
        }
        
        # Formatierte Ausgabe
        output = (
            f"Dreieck mit Seiten a={a}, b={b}, c={c}:\n"
            f"Umfang: {results['umfang']}\n"
            f"Flaeche: {results['flaeche']}\n"
            f"Winkel A: {results['alpha_grad']}Grad\n"
            f"Winkel B: {results['beta_grad']}Grad\n"
            f"Winkel C: {results['gamma_grad']}Grad\n"
            f"Hoehe ha: {results['hoehe_a']}\n"
            f"Hoehe hb: {results['hoehe_b']}\n"
            f"Hoehe hc: {results['hoehe_c']}\n"
            f"Inkreisradius: {results['inkreisradius']}\n"
            f"Umkreisradius: {results['umkreisradius']}"
        )
        
        return output, results
    
    def _calculate_triangle_sws(self, a: float, gamma_deg: float, b: float) -> Tuple[str, Dict[str, float]]:
        """
        Berechnet alle Daten eines Dreiecks aus zwei Seiten und dem eingeschlossenen Winkel (SWS).
        
        Args:
            a: Seite a
            gamma_deg: Winkel C in Grad (zwischen a und b)
            b: Seite b
            
        Returns:
            Tuple[str, Dict[str, float]]: (Formatierter Text, Ergebniswerte)
        """
        if a <= 0 or b <= 0:
            raise ValueError("Alle Seiten muessen positiv sein.")
            
        if gamma_deg <= 0 or gamma_deg >= 180:
            raise ValueError("Der Winkel muss zwischen 0Grad und 180Grad liegen.")
        
        # Umrechnung in Bogenmass
        gamma_rad = math.radians(gamma_deg)
        
        # Dritte Seite berechnen (Kosinussatz)
        c = math.sqrt(a**2 + b**2 - 2 * a * b * math.cos(gamma_rad))
        
        # Rest der Berechnung mit SSS durchfuehren
        return self._calculate_triangle_sss(a, b, c)
    
    def _calculate_triangle_wsw(self, alpha_deg: float, c: float, beta_deg: float) -> Tuple[str, Dict[str, float]]:
        """
        Berechnet alle Daten eines Dreiecks aus zwei Winkeln und der eingeschlossenen Seite (WSW).
        
        Args:
            alpha_deg: Winkel A in Grad
            c: Seite c (zwischen Winkel A und B)
            beta_deg: Winkel B in Grad
            
        Returns:
            Tuple[str, Dict[str, float]]: (Formatierter Text, Ergebniswerte)
        """
        if c <= 0:
            raise ValueError("Die Seite muss positiv sein.")
            
        if alpha_deg <= 0 or alpha_deg >= 180 or beta_deg <= 0 or beta_deg >= 180:
            raise ValueError("Die Winkel muessen zwischen 0Grad und 180Grad liegen.")
        
        # Berechnen des dritten Winkels
        gamma_deg = 180 - alpha_deg - beta_deg
        
        if gamma_deg <= 0:
            raise ValueError("Die Summe der beiden Winkel muss kleiner als 180Grad sein.")
        
        # Umrechnung in Bogenmass
        alpha_rad = math.radians(alpha_deg)
        beta_rad = math.radians(beta_deg)
        gamma_rad = math.radians(gamma_deg)
        
        # Seiten berechnen (Sinussatz)
        a = c * math.sin(alpha_rad) / math.sin(gamma_rad)
        b = c * math.sin(beta_rad) / math.sin(gamma_rad)
        
        # Rest der Berechnung mit SSS durchfuehren
        return self._calculate_triangle_sss(a, b, c)
    
    def _calculate_triangle_ssw(self, a: float, b: float, gamma_deg: float) -> Tuple[str, Dict[str, float]]:
        """
        Berechnet alle Daten eines Dreiecks aus zwei Seiten und dem gegenueberliegenden Winkel (SSW).
        
        Args:
            a: Seite a
            b: Seite b
            gamma_deg: Winkel C in Grad (gegenueber von c)
            
        Returns:
            Tuple[str, Dict[str, float]]: (Formatierter Text, Ergebniswerte)
        """
        if a <= 0 or b <= 0:
            raise ValueError("Alle Seiten muessen positiv sein.")
            
        if gamma_deg <= 0 or gamma_deg >= 180:
            raise ValueError("Der Winkel muss zwischen 0Grad und 180Grad liegen.")
        
        # Umrechnung in Bogenmass
        gamma_rad = math.radians(gamma_deg)
        
        # Dritte Seite berechnen (Kosinussatz)
        c = math.sqrt(a**2 + b**2 - 2 * a * b * math.cos(gamma_rad))
        
        # Rest der Berechnung mit SSS durchfuehren
        return self._calculate_triangle_sss(a, b, c)
    
    def _calculate_triangle_base_height(self, base: float, height: float) -> Tuple[str, Dict[str, float]]:
        """
        Berechnet grundlegende Daten eines Dreiecks aus Grundseite und Hoehe.
        
        Args:
            base: Grundseite
            height: Hoehe
            
        Returns:
            Tuple[str, Dict[str, float]]: (Formatierter Text, Ergebniswerte)
        """
        if base <= 0 or height <= 0:
            raise ValueError("Grundseite und Hoehe muessen positiv sein.")
        
        # Flaecheninhalt
        flaeche = 0.5 * base * height
        
        # Begrenztes Ergebnis, da nicht alle Werte berechenbar sind
        results = {
            "grundseite": self._round_significant(base, 6),
            "hoehe": self._round_significant(height, 6),
            "flaeche": self._round_significant(flaeche, 6)
        }
        
        # Formatierte Ausgabe
        output = (
            f"Dreieck mit Grundseite={base}, Hoehe={height}:\n"
            f"Flaeche: {results['flaeche']}\n"
            f"Hinweis: Weitere Werte koennen nicht eindeutig bestimmt werden."
        )
        
        return output, results
    
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