""" Read a tab-separated CSV text file into a pandas dataframe, return
(numbered) column names, number of rows, and the dictionary itself.
"""
import os
import tempfile
from pathlib import Path
import pandas as pd


INPUT_DIR = os.path.join(os.getcwd(), 'casas_gis/input_data')
INPUT_DIR.mkdir(parents=True, exist_ok=True)
TMP_DIR = os.path.join(os.getcwd(), 'casas_gis/tmp')
TMP_DIR.mkdir(parents=True, exist_ok=True)


def csv_to_df(filepath):
    return pd.read_csv(filepath, sep='\t')


def df_to_csv(df, filename, tmp_dir=TMP_DIR):
    filepath = os.path.join(tmp_dir, filename, index=False)
    df.to_csv(filepath, sep='\t')


def get_df_info(df):
    print('Dataframe head:\n')
    print(df.head(), '\n')
    rows, columns = df.shape
    print(f'Dataframe has {rows} rows and {columns} columns.', '\n')
    print('Dataframe basic info:\n')
    return df.info()


def combine_dfs_to_dict(input_dir=INPUT_DIR):
    df_dict = {}
    # https://stackoverflow.com/a/10378012 (glob directory)
    pathlist = Path(input_dir).rglob('*.txt')
    for filepath in sorted(pathlist):
        df = csv_to_df(filepath)
        dict_name = os.path.splitext(os.path.basename(filepath))[0]
        # print('...processed', dict_name)
        df_dict[dict_name] = df
    return(df_dict)


def concat_dfs(input_dir=INPUT_DIR):
    df_dict = combine_dfs_to_dict(input_dir)
    return pd.concat(df_dict.values(), ignore_index=True)


def extract_columns_from_df(df, column_id):
    if isinstance(column_id, str):
        column = df.loc[:, column_id]
    elif isinstance(column_id, int):
        column = df.iloc[:, column_id]
    else:
        raise ValueError('column_id must be str or int')
    return column


def select_variable(df_dict, lon, lat, variable, tmp_dir=TMP_DIR):
    for key, df in df_dict.items():
        lon_series = extract_columns_from_df(df, lon)
        lat_series = extract_columns_from_df(df, lat)
        variable_series = extract_columns_from_df(df, variable)
        df_select = pd.concat([lon_series,
                               lat_series,
                               variable_series], axis=1)
        df_to_csv(df_select, key)


def test_df_concat(input_dir=INPUT_DIR):
    """ This would be for generating more CSV files that include
        summary statisics for mapping e.g., mean, stardard deviation
        and coefficient of variation of yearly values for multi year
        simulations."""
    df_dict = {}
    # https://stackoverflow.com/a/10378012 (glob directory)
    pathlist = Path(input_dir).rglob('*.txt')
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
    dict_of_dataframes = combine_dfs_to_dict()
    print(dict_of_dataframes)
