from datetime import datetime
from typing import List, Tuple

class CalculationLog:
    def __init__(self):
        self.calculations: List[Tuple[str, str]] = []
        self.last_date_stamp = None
    
    def add_calculation(self, calculation: str, result: str) -> None:
        current_date = datetime.now().date()
        
        if self.last_date_stamp is None or current_date != self.last_date_stamp:
            self.last_date_stamp = current_date
            date_stamp = current_date.strftime("%d.%m.%Y")
            self.calculations.append((date_stamp, ""))
        
        self.calculations.append((calculation, result))
    
    def get_calculations(self) -> List[Tuple[str, str]]:
        return self.calculations
    
    def clear(self) -> None:
        self.calculations = []
        self.last_date_stamp = None
    
    def save_to_file(self, filename: str) -> bool:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for calc, result in self.calculations:
                    if result:
                        f.write(f"{calc}: {result}\n")
                    else:
                        f.write(f"--- {calc} ---\n")
            return True
        except Exception:
            return False
    
    def load_from_file(self, filename: str) -> bool:
        try:
            self.clear()
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("--- ") and line.endswith(" ---"):
                        date_str = line[4:-4]
                        self.calculations.append((date_str, ""))
                        try:
                            self.last_date_stamp = datetime.strptime(date_str, "%d.%m.%Y").date()
                        except ValueError:
                            pass
                    elif ":" in line:
                        calc, result = line.split(":", 1)
                        self.calculations.append((calc.strip(), result.strip()))
            return True
        except Exception:
            return False