import pandas as pd


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


def save_as(data, data_type, extension):
    print(data)
    if isinstance(data, dict):
        data = list(data)
    df = pd.DataFrame(data)
    if extension == 'csv':
        df.to_csv(f'{data_type}.csv')
    elif extension == 'xlsx':
        df.to_excel(f'{data_type}.xlsx')
    elif extension == 'json':
        df.to_json(f'{data_type}.json', indent=4, lines=True)
