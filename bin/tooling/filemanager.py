#import internal modules
from tooling.__init__ import __file_dir__

def save_info(info:list) -> None:

    with open(file=__file_dir__, mode="w") as file:
        for item in info:
            file.write(f"{item}\n")

def load_info() -> list:
    info:list = []

    try:
        with open(file=__file_dir__, mode="r") as file:
            while True:
                item = file.readline()
                if len(item) == 0: break
                info.append(item.strip())
        return info
    except:
        save_info(["None", "10", "Root", "0", "Marker Up/Down", "Eraser Up/Down", "Honk", "Quick Turn", "500", "0"])
        return load_info()
