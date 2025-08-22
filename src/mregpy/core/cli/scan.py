import pathlib
from rich.progress import Progress

class IgnoreFile:
    def __init__(self,path:pathlib.Path):
        self.path = path
        self.__load()

    def __load(self):
        with self.path.open() as file:
            self.data = file.read()
    
    def match(self,path:pathlib.Path) -> bool:
        for line in self.data.split("\n"):
            if line.startswith("#"):
                continue
            if path.match(line):
                return True
        return False

class Scanner:
    def __init__(self,progress:Progress):
        self.progress:Progress = progress
    
    def scan(self,directory:str):
        globalignorepath = pathlib.Path(".mregignore")
        if globalignorepath.exists():
            globalignore = [IgnoreFile(globalignorepath)]
        else:
            globalignore = []
        self.root:DirToScan = DirToScan(pathlib.Path(directory),self,globalignore)

class DirToScan:
    def __init__(self,path:pathlib.Path,scanner:Scanner,ignores:list[IgnoreFile]=[]):
        self.path:pathlib.Path = path
        self.scanner:Scanner = scanner
        
        self.task = self.scanner.progress.add_task(str(self.path),total=self.size)
        
        self.ignores:list[IgnoreFile] = ignores
        self.__load_ignore()
        self.__go()
        
    @property
    def size(self) -> int:
        return len(list(self.path.iterdir()))
    
    def __load_ignore(self):
        ignore = self.path.joinpath(".mregignore")
        if ignore.exists():
            self.scanner.progress.console.log(f"Ignore at {ignore.absolute()}")
            self.ignores.append(IgnoreFile(ignore))
    
    def __go(self):
        for path in self.path.iterdir():
            if any(ignore.match(path) for ignore in self.ignores):
                self.scanner.progress.console.log(f"ignoring path {path.absolute()}")
                self.scanner.progress.advance(self.task,1)
                continue
            if path.is_dir():
                DirToScan(path,self.scanner,self.ignores.copy())
            self.scanner.progress.advance(self.task,1)