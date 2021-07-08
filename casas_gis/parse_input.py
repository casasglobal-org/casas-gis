""" Read a tab-separated CSV text file into a pandas dataframe, return
(numbered) column names, number of rows, and the dictionary itself.
"""
import os
import tempfile
from pathlib import Path
import pandas as pd


INPUT_FOLDER = os.path.join(os.getcwd(), 'casas_gis/input_data')


def csv_to_df(filepath):
    return pd.read_csv(filepath, sep='\t')


def get_df_info(df):
    print('Dataframe head:\n')
    print(df.head(), '\n')
    rows, columns = df.shape
    print(f'Dataframe has {rows} rows and {columns} columns.', '\n')
    print('Dataframe basic info:\n')
    return df.info()


def combine_dfs_to_dict(input_folder=INPUT_FOLDER):
    df_dict = {}
    # https://stackoverflow.com/a/10378012 (glob directory)
    pathlist = Path(input_folder).rglob('*.txt')
    for filepath in sorted(pathlist):
        df = csv_to_df(filepath)
        dict_name = os.path.splitext(os.path.basename(filepath))[0]
        print('...processed', dict_name)
        df_dict[dict_name] = df
    return(df_dict)


# def generate_import_files():


def test_df_concat(input_folder=INPUT_FOLDER):
    """ This would be for generating more CSV files that include
        summary statisics for mapping e.g., mean, stardard deviation
        and coefficient of variation of yearly values for multi year
        simulations."""
    df_dict = {}
    # https://stackoverflow.com/a/10378012 (glob directory)
    pathlist = Path(input_folder).rglob('*.txt')
    for filepath in sorted(pathlist):
        df = csv_to_df(filepath)
        get_df_info(df)
        dict_name = os.path.splitext(os.path.basename(filepath))[0]
        print('\nFile path is:\n', filepath)
        print('\nDict name is:\n', dict_name)
        print('\n================================\n')
        df_dict[dict_name] = df
    df_all = pd.concat(df_dict.values(), ignore_index=True)
    print('Following is info about conctatenated (combined) dataframe:\n')
    get_df_info(df_all)


if __name__ == "__main__":
    test_df_concat()
    dfs_dict = combine_dfs_to_dict()
    print(dfs_dict)
