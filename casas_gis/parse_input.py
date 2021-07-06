""" Read a tab-separated CSV text file into a pandas dataframe, return
(numbered) column names, number of rows, and the dictionary itself.
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


def test_df_concat(input_folder=INPUT_FOLDER):
    """ This would be for generating more CSV files that include
        summary statisics for mapping e.g., mean, stardard deviation
        and coefficient of variation of yearly values for multi year
        simulations."""
    df_dict = {}
    for filepath in glob.iglob(f'{input_folder}/*.txt'):
        print(filepath)
        df = csv_to_df(filepath)
        get_df_info(df)
        dict_name = os.path.splitext(os.path.basename(filepath))[0]
        print(dict_name)
        df_dict[dict_name] = df
    df_all = pd.concat(df_dict.values(), ignore_index=True)
    print('\n================================\n')
    print('Following are info about conctatenated dataframe:\n')
    get_df_info(df_all)


if __name__ == "__main__":
    test_df_concat()
