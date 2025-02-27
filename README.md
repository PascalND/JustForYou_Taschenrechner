# JustForYou Taschenrechner

## 📝 Projektbeschreibung

Der **JustForYou Taschenrechner** ist eine modulare Softwarelösung, die den klassischen Windows-Taschenrechner durch ein anpassbares, branchenspezifisches Tool ersetzt. Jeder Benutzer kann seine eigene Konfiguration mit bis zu drei Branchenmodulen erhalten, die auf seine individuellen Bedürfnisse zugeschnitten sind.

Entwickelt im Auftrag der Kleinstweich Deutschland GmbH (KWD), bietet diese Anwendung einen intuitiven, geführten Arbeitsablauf für spezifische Berechnungen verschiedener Branchen.

## ✨ Hauptmerkmale

- **Modulares Design**: Basismodul plus bis zu drei individuelle Branchenmodule
- **Sequentielle Benutzerführung**: Intuitive Eingabe von Funktionsparametern
- **Protokollfunktion**: Automatische Aufzeichnung aller durchgeführten Berechnungen
- **Flexible Anpassbarkeit**: Schriftgröße, Schriftart und Hintergrundfarbe sind benutzerdefiniert einstellbar
- **Nebenrechner**: Ermöglicht zusätzliche Berechnungen während der Parametereingabe
- **AES-verschlüsselte Speicherung**: Sichere Speicherung und Einlesen der Ergebnisliste

## 🧮 Verfügbare Module

Der JustForYou Taschenrechner bietet folgende Module:

### Basismodul (standardmäßig eingebunden)
- **Grundrechner**: Unterstützt mehrere Operanden, Operatoren und Klammerrechnung

### Branchenmodule (individuell konfigurierbar)
- **Prozentrechnung**: %dazu, %weg, %davon, %Satz, Bruttopreis aus Nettopreis, Nettopreis aus Bruttopreis
- **Kreditberechnung**: Kredit mit einmaliger Rückzahlung, Ratenkredit mit Laufzeit- oder Ratenhöhenvorgabe
- **Geometrie**: Berechnungen für Dreiecke, Kreise und Parallelogramme
- **Mathematische Funktionen**: Fakultät, Quadratwurzel, Potenzfunktion, Primzahlen, Dezimal- zu gemeinem Bruch

## 🖥️ Technische Details

- **Programmiersprache**: Python
- **Benutzeroberfläche**: Tkinter mit modernem Design
- **Entwicklungsumgebung**: Visual Studio 2022
- **Architektur**: Modulare Plugin-Struktur mit dynamischen Laufzeitbibliotheken
- **Plattformunterstützung**: Windows-Betriebssysteme

## 🚀 Installation und Ausführung

1. Stelle sicher, dass Python (Version 3.7 oder höher) installiert ist
2. Klone das Repository:
   ```
   git clone https://github.com/yourusername/justforyou-calculator.git
   ```
3. Navigiere zum Projektverzeichnis:
   ```
   cd justforyou-calculator
   ```
4. Starte die Anwendung:
   ```
   python main.py
   ```

## 📁 Projektstruktur

```
justforyou-calculator/
├── assets/                 # Icons, Bilder und andere Assets
├── core/                   # Kernkomponenten
│   ├── __init__.py
│   ├── calculation_log.py  # Verwaltet das Berechnungsprotokoll
│   ├── plugin_interface.py # Interface für Plugin-Entwicklung
│   └── plugin_manager.py   # Lädt und verwaltet Plugins
├── gui/                    # Grafische Benutzeroberfläche
│   ├── __init__.py
│   ├── animations.py       # UI-Animationen
│   ├── main_window.py      # Hauptfenster der Anwendung
│   ├── side_calculator.py  # Nebenrechner-Komponente
│   ├── style_constants.py  # Design-Konstanten
│   ├── theme_manager.py    # Verwaltung des Erscheinungsbilds
│   └── triangle_input.py   # Spezielle Eingabe für Dreiecksberechnungen
├── plugins/                # Modul-Plugins
│   ├── __init__.py
│   ├── basic/              # Grundrechner-Modul
│   ├── credit/             # Kreditberechnungs-Modul
│   ├── geometry/           # Geometrie-Modul
│   ├── math_functions/     # Mathematische Funktionen
│   └── percentage/         # Prozentrechnung
├── tests/                  # Testdateien
├── main.py                 # Haupteinstiegspunkt der Anwendung
└── README.md               # Diese Datei
```

## 📊 Projektstatus

Dieses Projekt befindet sich in aktiver Entwicklung (Realisierungszeitraum: 10/2024 - 03/2025).
