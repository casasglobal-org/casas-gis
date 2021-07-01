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
    print('rows, columns:', df.shape, '\n')
    return df.info()


# Deprecated as filepth and df are now two separate functions
def get_ascii_table(filename, path=INPUT_FOLDER):
    df = pd.read_csv(os.path.join(path, filename), sep='\t')
    print(df.head(), '\n')
    print('rows, columns:', df.shape, '\n')
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
