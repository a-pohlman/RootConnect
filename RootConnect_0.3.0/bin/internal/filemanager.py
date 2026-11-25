def csv_to_list(data:str) -> list[str]:
    item: str = ""
    new_list: list[str] = []
    for index in range(len(data)):
        if data[index] != ",": item += data[index]
        else: 
            new_list.append(item)
            item = ""
    new_list.append(item)
    return new_list

def read_file(file_path:str) -> list[list[str]]:
    data: list[list[str]] = []
    with open(file=file_path, mode="r") as file:
        for line in file:
            data.append(csv_to_list(line.rstrip('\n')))
    return data
            
def save_data_to_csv(dir:str, robot_data:list[list[str]], mode:str="w") -> None:
    with open(file=dir, mode=mode) as file:
        for data in robot_data:
            commas: int = 1
            for info in data:
                file.write(str(info))
                if commas < len(data): file.write(",")
                commas += 1
            file.write('\n')