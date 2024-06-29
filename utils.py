import os
import pickle 
import pandas as pd

def load_model(path:str):
    with open(path, 'rb') as f:
        model = pickle.load(f)
    return model


def load_label_encoders(path: str='label_encoders') -> dict:
    """ loads the label_encoders in path folder to a dict with their labels as keys """
    les = {}
    for file in os.listdir(path):
        with open(f'{path}/{file}', 'rb') as f:
            les[file[:-7]] = pickle.load(f)
    return les


def transform_data(data: dict, label_encoders: dict) -> pd.DataFrame:
    for col, le in label_encoders.items():
        data[col] = le.transform(data[col])

    data = pd.DataFrame.from_dict(data)
    return data
