""" Read a tab-separated CSV text file into a pandas dataframe, return
    (numbered) column names, number of rows, and the dictionary itself."""

import os
from pathlib import Path
import pandas as pd


INPUT_DIR = os.path.join(os.getcwd(), 'casas_gis/input_data')
os.makedirs(INPUT_DIR, exist_ok=True)
TMP_DIR = os.path.join(os.getcwd(), 'casas_gis/tmp')
os.makedirs(TMP_DIR, exist_ok=True)


def csv_to_df(filepath):
    return pd.read_csv(filepath, sep='\t')


def df_to_csv(df, filename, tmp_dir=TMP_DIR):
    filepath = os.path.join(tmp_dir, filename)
    df.to_csv(filepath, sep='\t', index=False)


def get_df_info(df_dict):
    for key, df in df_dict.items():
        print(f'Head of {key} dataFrame:\n')
        print(df.head(), '\n')
        rows, columns = df.shape
        print(f'{key} dataFrame has {rows} rows and {columns} columns.', '\n')
        print(f'Basic info for {key} dataFrame:\n')
        df.info()
        print(f'\nEnd of {key} dataFrame info.')
        print('===========================================================\n')


def csv_to_df_dict(input_dir=INPUT_DIR):
    """ Turns CSV files in input_dir to a dictionary if dataFrames where
        keys are the names of CSV files. Works with single CSV too."""
    df_dict = {}
    # https://stackoverflow.com/a/10378012 (glob directory)
    pathlist = Path(input_dir).rglob('*.txt')
    for filepath in sorted(pathlist):
        df = csv_to_df(filepath)
        dict_name = os.path.splitext(os.path.basename(filepath))[0]
        # print('...processed', dict_name)
        df_dict[dict_name] = df
    return(df_dict)


def extract_columns_from_df(df, column_id):
    if isinstance(int(column_id), int):
        column = df.iloc[:, int(column_id)]
    elif isinstance(column_id, str):
        column = df.loc[:, column_id]
    else:
        raise ValueError('column_id must be str or int')
    return column


def select_variable(df_dict, lon, lat, variable, tmp_dir=TMP_DIR):
    # https://stackoverflow.com/a/55388872 (Loop through df_dict)
    for key, df in df_dict.items():
        lon_series = extract_columns_from_df(df, lon)
        lat_series = extract_columns_from_df(df, lat)
        variable_series = extract_columns_from_df(df, variable)
        df_select = pd.concat([lon_series,
                               lat_series,
                               variable_series], axis=1)
        # print(variable_series.name)
        tmp_file_name = f"{key}_{variable_series.name}.txt"
        df_to_csv(df_select, tmp_file_name, tmp_dir)


def concat_dfs(input_dir=INPUT_DIR):
    df_dict = csv_to_df_dict(input_dir)
    return pd.concat(df_dict.values(), ignore_index=True)


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
        print('\nDataFrame name is:\n', dict_name)
        print('\n================================\n')
        df_dict[dict_name] = df
    df_all = pd.concat(df_dict.values(), ignore_index=True)
    print('Following is info about conctatenated (combined) dataframe:\n')
    get_df_info(df_all)


if __name__ == "__main__":
    dict_of_dataframes = csv_to_df_dict()
    get_df_info(dict_of_dataframes)
    longitude = input('Enter longitude "column name" or integer index: ')
    latitude = input('Enter latitude "column name" or integer index:  ')
    variable = input('Enter variable "column name" or integer index: ')
    select_variable(dict_of_dataframes,
                    longitude, latitude, variable, tmp_dir=TMP_DIR)
