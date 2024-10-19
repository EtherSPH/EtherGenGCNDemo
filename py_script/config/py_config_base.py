'''
 # @ author: bcynuaa <bcynuaa@163.com> | vox-1 <xur2006@163.com>
 # @ date: 2024/10/19 16:13:18
 # @ license: MIT
 # @ description:
 '''

class ConfigBase:
    
    def __init__(self) -> None:
        pass
    
    def getKeys(self) -> list:
        return []
        pass
    
    def getValues(self) -> list:
        return []
        pass
    
    def getDict(self) -> dict:
        return dict(zip(self.getKeys(), self.getValues()))
        pass
    
    def getKeyName(self) -> str:
        return ""
        pass
    
    def __call__(self) -> tuple:
        return self.getKeyName(), self.getDict()
        pass
    
    def __str__(self) -> str:
        string: str = self.getKeyName() + "\n"
        for key, value in self.getDict().items():
            string += f"{key}: {value}\n"
            pass
        return string
        pass
    
    def __repr__(self) -> str:
        return self.__str__()
        pass
    
    pass