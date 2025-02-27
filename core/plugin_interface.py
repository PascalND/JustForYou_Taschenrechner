from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple

class Command:
    
    def __init__(self, name: str, param_names: List[str]):
        self.name = name
        self.param_names = param_names

class PluginInfo:
    
    def __init__(self, name: str, commands: List[Command]):
        self.name = name
        self.commands = commands

class IPlugin(ABC):
    
    @abstractmethod
    def load(self) -> None:
        pass
    
    @abstractmethod
    def get_info(self) -> PluginInfo:
        pass
    
    @abstractmethod
    def exec(self, command_name: str, params: List[float]) -> Tuple[str, Any]:
        pass