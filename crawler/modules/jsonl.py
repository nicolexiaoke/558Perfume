from typing import List
import pandas as pd

def load_to_list(file_path: str) -> List[dict]:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    result = []
    for line in lines:
        data = eval(line.strip("\n"))
        result.append(data)
    return result

def dump(file_path: str, iterable: List[dict]) -> int:
    count = 0
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in iterable:
            count += f.write(str(item) + '\n')
    return count

def load_to_df(file_path: str) -> pd.DataFrame:
    pass

def pickle():
    pass