# gui/theme_manager.py

import tkinter as tk
from tkinter import ttk, colorchooser, font
from typing import Dict, Any

class ThemeManager:
    """Verwaltet das Erscheinungsbild der Anwendung."""
    
    def __init__(self, root: tk.Tk):
        """
        Initialisiert einen neuen Theme-Manager.
        
        Args:
            root: Das Wurzelelement der Tkinter-Anwendung
        """
        self.root = root
        
        # Standard-Theme
        self.theme = {
            "font_family": "Arial",
            "font_size": 10,
            "bg_color": "#f0f0f0",
            "fg_color": "#000000",
            "button_bg": "#e0e0e0",
            "highlight_bg": "#d0d0d0"
        }
        
        # Theme anwenden
        self.apply_theme(root)
    
    def apply_theme(self, widget: tk.Widget) -> None:
        """
        Wendet das aktuelle Theme auf ein Widget an.
        
        Args:
            widget: Das Widget, auf das das Theme angewendet werden soll
        """
        # Schriftart erstellen
        custom_font = font.Font(
            family=self.theme["font_family"],
            size=self.theme["font_size"]
        )
        
        # Theme auf das Widget anwenden
        widget.config(bg=self.theme["bg_color"])
        
        # Stile fuer ttk-Widgets erstellen
        style = ttk.Style(widget)
        
        # TButton-Style
        style.configure(
            "TButton",
            font=custom_font,
            background=self.theme["button_bg"]
        )
        
        # TLabel-Style
        style.configure(
            "TLabel",
            font=custom_font,
            background=self.theme["bg_color"],
            foreground=self.theme["fg_color"]
        )
        
        # TEntry-Style
        style.configure(
            "TEntry",
            font=custom_font,
            fieldbackground=self.theme["bg_color"],
            foreground=self.theme["fg_color"]
        )
        
        # TFrame-Style
        style.configure(
            "TFrame",
            background=self.theme["bg_color"]
        )
        
        # TLabelframe-Style
        style.configure(
            "TLabelframe",
            font=custom_font,
            background=self.theme["bg_color"],
            foreground=self.theme["fg_color"]
        )
        
        # TLabelframe.Label-Style
        style.configure(
            "TLabelframe.Label",
            font=custom_font,
            background=self.theme["bg_color"],
            foreground=self.theme["fg_color"]
        )
        
        # Rekursiv auf alle Kinder anwenden
        for child in widget.winfo_children():
            if isinstance(child, (tk.Listbox, tk.Text, tk.Entry)):
                child.config(
                    font=custom_font,
                    bg=self.theme["bg_color"],
                    fg=self.theme["fg_color"],
                    selectbackground=self.theme["highlight_bg"]
                )
            elif isinstance(child, (tk.Button, tk.Label, tk.Frame, tk.LabelFrame)):
                child.config(
                    font=custom_font,
                    bg=self.theme["bg_color"],
                    fg=self.theme["fg_color"]
                )
            
            self.apply_theme(child)
    
    def open_settings_dialog(self) -> None:
        """oeffnet den Dialog fuer die Designeinstellungen."""
        # Toplevel-Fenster erstellen
        dialog = tk.Toplevel(self.root)
        dialog.title("Design anpassen")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.grab_set()  # Modal machen
        
        # Theme anwenden
        self.apply_theme(dialog)
        
        # Frame fuer den Inhalt
        content_frame = ttk.Frame(dialog)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Beschreibungstext
        description_label = ttk.Label(
            content_frame,
            text="Passen Sie das Erscheinungsbild der Anwendung an:"
        )
        description_label.pack(fill=tk.X, pady=(0, 10))
        
        # Schriftart-Auswahl
        font_frame = ttk.Frame(content_frame)
        font_frame.pack(fill=tk.X, pady=5)
        
        font_label = ttk.Label(font_frame, text="Schriftart:", width=15, anchor="e")
        font_label.pack(side=tk.LEFT, padx=(0, 5))
        
        available_fonts = list(font.families())
        available_fonts.sort()
        
        font_var = tk.StringVar(value=self.theme["font_family"])
        font_combo = ttk.Combobox(font_frame, textvariable=font_var, values=available_fonts)
        font_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Schriftgroesse-Auswahl
        size_frame = ttk.Frame(content_frame)
        size_frame.pack(fill=tk.X, pady=5)
        
        size_label = ttk.Label(size_frame, text="Schriftgroesse:", width=15, anchor="e")
        size_label.pack(side=tk.LEFT, padx=(0, 5))
        
        size_var = tk.IntVar(value=self.theme["font_size"])
        size_combo = ttk.Combobox(size_frame, textvariable=size_var, values=list(range(8, 21)))
        size_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Hintergrundfarbe-Auswahl
        bg_frame = ttk.Frame(content_frame)
        bg_frame.pack(fill=tk.X, pady=5)
        
        bg_label = ttk.Label(bg_frame, text="Hintergrundfarbe:", width=15, anchor="e")
        bg_label.pack(side=tk.LEFT, padx=(0, 5))
        
        bg_button = ttk.Button(
            bg_frame,
            text="Auswaehlen",
            command=lambda: self._choose_color("bg_color", bg_preview)
        )
        bg_button.pack(side=tk.LEFT)
        
        bg_preview = tk.Label(bg_frame, width=8, height=1, bg=self.theme["bg_color"])
        bg_preview.pack(side=tk.LEFT, padx=5)
        
        # Textfarbe-Auswahl
        fg_frame = ttk.Frame(content_frame)
        fg_frame.pack(fill=tk.X, pady=5)
        
        fg_label = ttk.Label(fg_frame, text="Textfarbe:", width=15, anchor="e")
        fg_label.pack(side=tk.LEFT, padx=(0, 5))
        
        fg_button = ttk.Button(
            fg_frame,
            text="Auswaehlen",
            command=lambda: self._choose_color("fg_color", fg_preview)
        )
        fg_button.pack(side=tk.LEFT)
        
        fg_preview = tk.Label(fg_frame, width=8, height=1, bg=self.theme["fg_color"])
        fg_preview.pack(side=tk.LEFT, padx=5)
        
        # Button-Hintergrundfarbe-Auswahl
        button_bg_frame = ttk.Frame(content_frame)
        button_bg_frame.pack(fill=tk.X, pady=5)
        
        button_bg_label = ttk.Label(button_bg_frame, text="Button-Farbe:", width=15, anchor="e")
        button_bg_label.pack(side=tk.LEFT, padx=(0, 5))
        
        button_bg_button = ttk.Button(
            button_bg_frame,
            text="Auswaehlen",
            command=lambda: self._choose_color("button_bg", button_bg_preview)
        )
        button_bg_button.pack(side=tk.LEFT)
        
        button_bg_preview = tk.Label(button_bg_frame, width=8, height=1, bg=self.theme["button_bg"])
        button_bg_preview.pack(side=tk.LEFT, padx=5)
        
        # OK- und Abbrechen-Buttons
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        cancel_button = ttk.Button(
            button_frame,
            text="Abbrechen",
            command=dialog.destroy
        )
        cancel_button.pack(side=tk.RIGHT, padx=5)
        
        ok_button = ttk.Button(
            button_frame,
            text="OK",
            command=lambda: self._apply_theme_settings(
                font_var.get(),
                size_var.get(),
                dialog
            )
        )
        ok_button.pack(side=tk.RIGHT, padx=5)
        
        # Dialog zentrieren
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (self.root.winfo_width() - width) // 2 + self.root.winfo_x()
        y = (self.root.winfo_height() - height) // 2 + self.root.winfo_y()
        dialog.geometry(f"{width}x{height}+{x}+{y}")
    
    def _choose_color(self, color_key: str, preview_label: tk.Label) -> None:
        """
        oeffnet einen Farbauswahldialog und aktualisiert die Vorschau.
        
        Args:
            color_key: Der Schluessel der Farbe im Theme-Dictionary
            preview_label: Das Label fuer die Farbvorschau
        """
        color = colorchooser.askcolor(initialcolor=self.theme[color_key])[1]
        
        if color:
            self.theme[color_key] = color
            preview_label.config(bg=color)
    
    def _apply_theme_settings(self, font_family: str, font_size: int, dialog: tk.Toplevel) -> None:
        """
        Wendet die ausgewaehlten Designeinstellungen an und schliesst den Dialog.
        
        Args:
            font_family: Die ausgewaehlte Schriftart
            font_size: Die ausgewaehlte Schriftgroesse
            dialog: Der zu schliessende Dialog
        """
        self.theme["font_family"] = font_family
        self.theme["font_size"] = font_size
        
        # Theme auf die gesamte Anwendung anwenden
        self.apply_theme(self.root)
        
        # Dialog schliessen
        dialog.destroy()