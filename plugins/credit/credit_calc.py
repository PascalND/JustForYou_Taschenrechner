# plugins/credit/credit_calc.py

from typing import List, Tuple, Any
from core.plugin_interface import IPlugin, PluginInfo, Command

class CreditCalculator(IPlugin):
    """Implementiert den Kreditrechner."""
    
    def __init__(self):
        """Initialisiert einen neuen Kreditrechner."""
        self.name = "Kreditberechnung"
        self.commands = [
            Command("Einmalrueckzahlung", ["Kreditbetrag", "Zinssatz", "Laufzeit (Monate)"]),
            Command("Ratenkredit (Laufzeit)", ["Kreditbetrag", "Zinssatz", "Laufzeit (Monate)"]),
            Command("Ratenkredit (Ratenhoehe)", ["Kreditbetrag", "Zinssatz", "Ratenhoehe"])
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
        if command_name == "Einmalrueckzahlung":
            # Kredit mit einmaliger Rueckzahlung
            kreditbetrag = float(params[0])
            zinssatz = float(params[1])
            laufzeit = int(params[2])
            
            # Monatlicher Zinssatz
            monatlicher_zinssatz = zinssatz / 100 / 12
            
            # Endbetrag berechnen
            endbetrag = kreditbetrag * (1 + monatlicher_zinssatz) ** laufzeit
            zinsen_gesamt = endbetrag - kreditbetrag
            
            # Runden auf 2 Nachkommastellen (Waehrung)
            endbetrag = round(endbetrag, 2)
            zinsen_gesamt = round(zinsen_gesamt, 2)
            
            return (
                f"Kreditberechnung: {kreditbetrag} €, Zinsen {zinssatz} %, "
                f"Laufzeit {laufzeit} Monate → Rueckzahlung {endbetrag} €, "
                f"Zinsen gesamt {zinsen_gesamt} €",
                endbetrag
            )
            
        elif command_name == "Ratenkredit (Laufzeit)":
            # Ratenkredit mit Vorgabe der Laufzeit
            kreditbetrag = float(params[0])
            zinssatz = float(params[1])
            laufzeit = int(params[2])
            
            # Monatlicher Zinssatz
            monatlicher_zinssatz = zinssatz / 100 / 12
            
            # Ratenhoehe berechnen
            if monatlicher_zinssatz == 0:
                rate = kreditbetrag / laufzeit
            else:
                rate = (kreditbetrag * monatlicher_zinssatz) / (1 - (1 + monatlicher_zinssatz) ** -laufzeit)
            
            # Gesamtzinsen
            zinsen_gesamt = rate * laufzeit - kreditbetrag
            
            # Runden auf 2 Nachkommastellen (Waehrung)
            rate = round(rate, 2)
            zinsen_gesamt = round(zinsen_gesamt, 2)
            
            return (
                f"Ratenkredit: {kreditbetrag} €, Zinsen {zinssatz} %, "
                f"Laufzeit {laufzeit} Monate → Rate {rate} €, "
                f"Zinsen gesamt {zinsen_gesamt} €",
                rate
            )
            
        elif command_name == "Ratenkredit (Ratenhoehe)":
            # Ratenkredit mit Vorgabe der Ratenhoehe
            kreditbetrag = float(params[0])
            zinssatz = float(params[1])
            rate = float(params[2])
            
            # Pruefen, ob die Rate groesser als die monatlichen Zinsen ist
            monatlicher_zinssatz = zinssatz / 100 / 12
            min_rate = kreditbetrag * monatlicher_zinssatz
            
            if rate <= min_rate and monatlicher_zinssatz > 0:
                raise ValueError(
                    f"Die Rate muss groesser als die monatlichen Zinsen sein "
                    f"(mindestens {min_rate:.2f} €)."
                )
            
            # Laufzeit berechnen
            if monatlicher_zinssatz == 0:
                laufzeit = kreditbetrag / rate
                schlussrate = rate
            else:
                laufzeit = -1 * (
                    (
                        (
                            1 - (kreditbetrag * monatlicher_zinssatz / rate)
                        )
                    ) / (
                        (
                            1 / (
                                (1 + monatlicher_zinssatz)
                            )
                        )
                    )
                )
                
                # Laufzeit als ganze Zahl
                laufzeit_ganzzahl = int(laufzeit)
                
                # Schlussrate berechnen
                restschuld = kreditbetrag
                for _ in range(laufzeit_ganzzahl):
                    restschuld = restschuld * (1 + monatlicher_zinssatz) - rate
                
                schlussrate = restschuld * (1 + monatlicher_zinssatz)
                laufzeit = laufzeit_ganzzahl + 1  # +1 fuer die Schlussrate
            
            # Gesamtzinsen
            zinsen_gesamt = rate * (laufzeit - 1) + schlussrate - kreditbetrag
            
            # Runden
            laufzeit = round(laufzeit)
            schlussrate = round(schlussrate, 2)
            zinsen_gesamt = round(zinsen_gesamt, 2)
            
            return (
                f"Ratenkredit: {kreditbetrag} €, Zinsen {zinssatz} %, "
                f"Rate {rate} € → Laufzeit {laufzeit} Monate, "
                f"Schlussrate {schlussrate} €, Zinsen gesamt {zinsen_gesamt} €",
                laufzeit
            )
        
        raise ValueError(f"Unbekannter Befehl: {command_name}")