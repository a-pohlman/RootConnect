def parse_dir_path(path: str, stop_at_dir: str) -> str:
    path_array: list = []
    single_dir: str = ""
    instance: int = 0
    final_path: str = ""
        
    while True:
        if single_dir == stop_at_dir:
            path_array.append(single_dir)
            break

        if path[instance] == "\\":
            path_array.append(single_dir+"\\")
            single_dir = ""
            instance += 1

        single_dir += path[instance]
        instance += 1

    for i in path_array: final_path += i
    return final_path

__base_dir__ = parse_dir_path(__file__, "bin")