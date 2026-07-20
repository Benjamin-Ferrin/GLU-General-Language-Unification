from .helpers import bcolors

def parse(filename):

    bindings = {}
    callbacks = []
    seen_lines = {}

    with open(filename) as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        stripped = line.strip()

        if stripped == "" or stripped.startswith("#"):
            continue
        if "#" in line:
            line = line.split("#")[0].strip()
        if line in seen_lines:
            print(f"{bcolors.WARNING}ERROR: Duplicate line found (line {i+1}, previously defined on line {seen_lines[line]+1}). {bcolors.ENDC}")
            continue
        seen_lines[line] = i
        if ("BIND:" in line and "->" in line) or line.count("->") > 1:
            print(f"{bcolors.FAIL}ERROR: Function bindings must be defined on individual lines (line {i+1}). Please remove it.{bcolors.ENDC}")
            continue
        if line.startswith("BIND:"):
            continue

        if "->" in line:
            left, right = line.split("->", 1)

            source = left.strip()
            targets = parseStringList(right.strip())

            if source not in bindings:
                bindings[source] = []

            for target in targets:
                if target not in bindings[source]:
                    bindings[source].append(target)       
                                             
    return bindings

def parseStringList(string):
    return [
        item.strip()
        for item in string.split(",")
        if item.strip()
    ]

class Endpoint:
    def __init__(self, string):
        self.string = string.strip()
        self.language, self.path = self.string.split("@", 1)
        self.language = self.language.strip()
        self.path = self.path.strip()
        self.parts = self.path.split(".")

    def getLanguage(self):
        return self.language
    def getPath(self):
        return self.path
    def getObject(self):
        return self.parts[-1].split("(")[0]
    def getFilePath(self):
        return ".".join(self.parts[:-1])
    def pathToInterface(self):
        return "\\".join([str(x) for x in self.parts[:-1]]) + "\\" + self.getObject() + "." + self.getLanguage()
    def comparePaths(self, other):
        return self.pathToInterface() == other.pathToInterface()
    def pathToFile(self):
        return "\\".join([str(x) for x in self.parts[:-1]]) + "." + self.getLanguage()

# print(f"Bindings: {parse(r\"C:\\Users\\benny\\Documents\\bens-stuff\\Coding\\GLU\\APP\\main.glu\")}")
# endpoint = Endpoint("py@app.src.path.main.function")
# print(endpoint.pathToInterface())
