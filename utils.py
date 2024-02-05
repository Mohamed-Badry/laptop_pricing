import os
import pickle 
import pandas as pd

def load_model(path:str):
    with open(path, 'rb') as f:
        model = pickle.load(f)
    return model


def load_transformers(path: str='transformers') -> dict:
    """ loads the transformers in path folder to a dict with their labels as keys """
    les = {}
    for file in os.listdir(path):
        with open(f'{path}/{file}', 'rb') as f:
            les[file[:-7]] = pickle.load(f)
    return les


def transform_data(data: dict, transformers: dict) -> pd.DataFrame:
    for col, le in transformers.items():
        data[col] = le.transform(data[col])

    data = pd.DataFrame.from_dict(data)
    return data
