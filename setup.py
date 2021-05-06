import sys
from cx_Freeze import setup, Executable

base = None

if sys.platform == "win32":
    base = "Win32GUI"

exe = Executable(script='main.py', base = base, icon='icon.ico')

setup(
    name = "Battaile de bases",
    version = "1.0",
    author = "Nathan Lefevre",
    description = "Jeu cree pour mon projet final de NSI, CNED",
    options = {"build_exe": {"packages": ["pygame", "random", "sys","time"], "include_files": ['main.py','icon.ico',"grass.png","icelake.png","sand.png","forest.png","swamp.png","boulder.png","snowymountain.png","mountain.png","lava.png","volcano.png","water.png","redworker.png","redinfantry.png","redcavalry.png","redarchers.png","redbase.png","bluebase.png","blueworker.png","blueinfantry.png","bluecavalry.png","bluearchers.png","wood.png","stone.png","metal.png"]}},
    executables = [exe]
)  