'''
 # @ author: bcynuaa <bcynuaa@163.com> | vox-1 <xur2006@163.com>
 # @ date: 2024/10/19 16:53:41
 # @ license: MIT
 # @ description:
 '''

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

from py_config_base import ConfigBase

class Info(ConfigBase):
    
    def __init__(
        self,
        name: str = "case_name",
        date: str = "2024-10-19",
        author: str = "bcynuaa | vox-1",
        comment: str = "",
    ) -> None:
        super().__init__()
        self.name: str = name
        self.date: str = date
        self.author: str = author
        self.comment: str = comment
        pass
    
    def getValues(self) -> list:
        return [
            self.getName(),
            self.getDate(),
            self.getAuthor(),
            self.getComment(),
        ]
        pass
    
    def getKeys(self) -> list:
        return [
            "name",
            "date",
            "author",
            "comment",
        ]
        pass
    
    def getKeyName(self) -> str:
        return "info"
        pass
    
    def getName(self) -> str:
        return self.name
        pass
    
    def setName(self, name: str) -> None:
        self.name = name
        pass
    
    def getDate(self) -> str:
        return self.date
        pass
    
    def setDate(self, date: str) -> None:
        self.date = date
        pass
    
    def getAuthor(self) -> str:
        return self.author
        pass
    
    def setAuthor(self, author: str) -> None:
        self.author = author
        pass
    
    def getComment(self) -> str:
        return self.comment
        pass
    
    def setComment(self, comment: str) -> None:
        self.comment = comment
        pass
        
    pass