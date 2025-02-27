import os
import importlib.util
from typing import Dict, List, Optional
from core.plugin_interface import IPlugin, PluginInfo

class PluginManager:
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = plugin_dir
        self.plugins: Dict[str, IPlugin] = {}
        self.plugin_infos: Dict[str, PluginInfo] = {}
    
    def load_plugins(self) -> None:
        from plugins.basic.basic_calc import BasicCalculator
        basic_calc = BasicCalculator()
        basic_calc.load()
        self.plugins["basic"] = basic_calc
        self.plugin_infos["basic"] = basic_calc.get_info()
        
        available_plugins = ["credit", "geometry", "math_functions", "percentage"]
        loaded_count = 0
        
        for plugin_name in available_plugins:
            if loaded_count >= 3:
                break
                
            plugin_path = os.path.join(self.plugin_dir, plugin_name)
            if not os.path.isdir(plugin_path):
                continue
                
            try:
                module_path = os.path.join(plugin_path, f"{plugin_name}_calc.py")
                if not os.path.exists(module_path):
                    module_path = os.path.join(plugin_path, f"{plugin_name.split('_')[0]}_func.py")
                    
                if not os.path.exists(module_path):
                    continue
                    
                module_name = os.path.basename(module_path).replace(".py", "")
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if "func" in module_name:
                    class_name = module_name.replace("_func", "").capitalize() + "Functions"
                else:
                    class_name = module_name.replace("_calc", "").capitalize() + "Calculator"
                
                plugin_class = getattr(module, class_name)
                plugin = plugin_class()
                plugin.load()
                
                self.plugins[plugin_name] = plugin
                self.plugin_infos[plugin_name] = plugin.get_info()
                loaded_count += 1
                
            except Exception as e:
                print(f"Fehler beim Laden des Plugins {plugin_name}: {e}")
    
    def get_plugin_infos(self) -> List[PluginInfo]:
        return list(self.plugin_infos.values())
    
    def get_plugin(self, plugin_name: str) -> Optional[IPlugin]:
        return self.plugins.get(plugin_name)