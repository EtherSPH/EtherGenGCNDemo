'''
 # @ author: bcynuaa <bcynuaa@163.com> | vox-1 <xur2006@163.com>
 # @ date: 2024/10/19 20:28:02
 # @ license: MIT
 # @ description:
 '''

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import shutil
import subprocess
import time

from config.py_config import Config

def date2string(date: time) -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", date)
    pass

class SingleCaseRunner:
    
    def __init__(
        self,
        config: Config
    ) -> None:
        self.config: Config = config
        pass
    
    def getCommandLineList(self) -> list:
        return [
            "julia",
            "-t", "32",
            "-O3",
            "--math-mode=fast",
            "--project=.",
            self.config.getScriptName()
        ]
        pass
    
    def getCommandLineString(self) -> str:
        return " ".join(self.getCommandLineList())
        pass
    
    def run(self) -> None:
        print("=" * 100)
        date: str = date2string(time.localtime())
        self.config.getInfo().setDate(date)
        self.config.writeCase()
        print(f"case recorded date: {date}")
        print(f"case file has been writing to: {self.config.getCaseName()}")
        print(f"running command: `{self.getCommandLineString()}` ...")
        return_code: int = subprocess.run(
            self.getCommandLineList(),
            shell=False,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        ).returncode
        print(f"return code: {return_code}")
        # copy the case file to the result directory
        shutil.copy(self.config.getCaseName(), self.config.getResultFolder())
        print(f"case file has been copied to: {os.path.join(self.config.getResultFolder(), self.config.getCaseName())}")
        pass
    
    pass