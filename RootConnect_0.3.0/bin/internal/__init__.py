#import python modules
import sys

__version__ = "0.3.0"
__system__ = sys.platform

if __system__ == "darwin" or __system__.startswith("lin") == True: __path_separator__ = "/"
elif sys.platform.startswith("win"): __path_separator__ = "\\"

def get_dir_path(path: str, stop_at_dir: str) -> str:
    path_array: list = []
    single_dir: str = ""
    instance: int = 0
    final_path: str = ""
        
    while True:
        if single_dir == stop_at_dir:
            path_array.append(single_dir)
            break

        if path[instance] == __path_separator__:
            path_array.append(single_dir+__path_separator__)
            single_dir = ""
            instance += 1

        single_dir += path[instance]
        instance += 1

    for i in path_array: final_path += i
    return final_path

__base_dir__ = get_dir_path(__file__, "RootConnect_0.3.0")
__bin_dir__ = f"{__base_dir__}{__path_separator__}bin{__path_separator__}"
__icon_dir__ = f"{__base_dir__}{__path_separator__}icons{__path_separator__}"
__style_dir__ = f"{__base_dir__}{__path_separator__}stylesheets{__path_separator__}"
__cache_dir__ = f"{__base_dir__}{__path_separator__}cache{__path_separator__}"