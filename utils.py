import pathlib
from typing import Union
import pandas as pd
from inspect import isclass, getmembers


def convert_file_to_list(filelocation):
    urls = None
    if filelocation.endswith('.csv'):
        df = pd.read_csv(filelocation)
        urls = df['products'].to_list()
    elif filelocation.endswith('.xlsx'):
        df = pd.read_excel(filelocation)
        urls = df['products'].to_list()
    else:
        print('Currently only csv and excel file format are supported')
    return urls

