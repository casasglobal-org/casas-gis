""" Read a tab-separated text file into a pandas dataframe, return (numbered)
column names, number of rows, and the dictionary itself.
"""
import os
import glob
import pandas as pd


INPUT_FOLDER = os.path.join(os.getcwd(), 'casas_gis/input_data')


def csv_to_df(filepath):
    return pd.read_csv(filepath, sep='\t')


def get_df_info(df):
    print(df.head(), '\n')
    rows, columns = df.shape
    print(f'Dataframe has {rows} rows and {columns} columns.', '\n')
    return df.info()


if __name__ == "__main__":
    df_dict = {}
    for filepath in glob.iglob(f'{INPUT_FOLDER}/*.txt'):
        print(filepath)
        df = csv_to_df(filepath)
        get_df_info(df)
        dict_name = os.path.splitext(os.path.basename(filepath))[0]
        print(dict_name)
        df_dict[dict_name] = df

    pd.concat(df_dict.values(), ignore_index=True)
