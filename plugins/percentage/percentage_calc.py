# plugins/percentage/percentage_calc.py

from typing import List, Tuple, Any
from core.plugin_interface import IPlugin, PluginInfo, Command

class PercentageCalculator(IPlugin):
    """Implementiert den Prozentrechner."""
    
    def __init__(self):
        """Initialisiert einen neuen Prozentrechner."""
        self.name = "Prozentrechnung"
        self.commands = [
            Command("%dazu", ["Grundwert", "Prozentsatz"]),
            Command("%weg", ["Grundwert", "Prozentsatz"]),
            Command("%davon", ["Grundwert", "Prozentsatz"]),
            Command("%Satz", ["Grundwert", "Prozentwert"]),
            Command("Bruttopreis", ["Nettopreis", "Steuersatz"]),
            Command("Nettopreis", ["Bruttopreis", "Steuersatz"])
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
        if command_name == "%dazu":
            # Prozent dazu
            grundwert = float(params[0])
            prozentsatz = float(params[1])
            
            prozentwert = grundwert * prozentsatz / 100
            ergebnis = grundwert + prozentwert
            
            return f"Prozentrechnung: {grundwert} + {prozentsatz}% = {ergebnis}", ergebnis
            
        elif command_name == "%weg":
            # Prozent weg
            grundwert = float(params[0])
            prozentsatz = float(params[1])
            
            prozentwert = grundwert * prozentsatz / 100
            ergebnis = grundwert - prozentwert
            
            return f"Prozentrechnung: {grundwert} - {prozentsatz}% = {ergebnis}", ergebnis
            
        elif command_name == "%davon":
            # Prozent davon
            grundwert = float(params[0])
            prozentsatz = float(params[1])
            
            ergebnis = grundwert * prozentsatz / 100
            
            return f"Prozentrechnung: {prozentsatz}% von {grundwert} = {ergebnis}", ergebnis
            
        elif command_name == "%Satz":
            # Prozentsatz
            grundwert = float(params[0])
            prozentwert = float(params[1])
            
            if grundwert == 0:
                raise ValueError("Der Grundwert darf nicht 0 sein.")
            
            prozentsatz = (prozentwert / grundwert) * 100
            
            return f"Prozentrechnung: {prozentwert} ist {prozentsatz}% von {grundwert}", prozentsatz
            
        elif command_name == "Bruttopreis":
            # Bruttopreis aus Nettopreis
            nettopreis = float(params[0])
            steuersatz = float(params[1])
            
            steuer = nettopreis * steuersatz / 100
            bruttopreis = nettopreis + steuer
            
            return f"Prozentrechnung: Nettopreis {nettopreis} + {steuersatz}% MwSt = Bruttopreis {bruttopreis}", bruttopreis
            
        elif command_name == "Nettopreis":
            # Nettopreis aus Bruttopreis
            bruttopreis = float(params[0])
            steuersatz = float(params[1])
            
            if steuersatz == -100:
                raise ValueError("Der Steuersatz darf nicht -100% sein.")
            
            nettopreis = bruttopreis * 100 / (100 + steuersatz)
            
            return f"Prozentrechnung: Bruttopreis {bruttopreis} / (100 + {steuersatz}%) = Nettopreis {nettopreis}", nettopreis
        
        raise ValueError(f"Unbekannter Befehl: {command_name}")