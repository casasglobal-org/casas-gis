#!/usr/bin/env python3
#
# AUTHOR(S):    Luigi Ponti quartese gmail com
#
# PURPOSE:      
#
# NOTE:         
#
# Copyright:    (c) 2021-2024 CASAS (Center for the Analysis
#                   of Sustainable Agricultural Systems).
#                   https://www.casasglobal.org/).
#
#               SPDX-License-Identifier: GPL-3.0-or-later

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
    """Read a tab-separated CSV text file into a pandas dataframe.

    Args:
        filepath (str): Path of the input text file.

    Returns:
        pandas.DataFrame: The parsed dataframe."""
    return pd.read_csv(filepath, sep='\t')


def df_to_csv(df, filename, tmp_dir=TMP_DIR):
    """Write a pandas dataframe to a tab-separated CSV text file.

    Args:
        df (pandas.DataFrame): Dataframe to write.
        filename (str): Name of the output file.
        tmp_dir (str): Directory where the file is written.

    Returns:
        None."""
    filepath = os.path.join(tmp_dir, filename)
    df.to_csv(filepath, sep='\t', index=False)


def get_df_info(df_dict):
    """Print basic info (head, shape, memory usage) of each dataframe.

    Args:
        df_dict (dict): Dictionary of dataframes keyed by file name.

    Returns:
        None."""
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
    """Turn CSV files in input_dir into a dictionary of dataframes
    whose keys are the names of the CSV files. Works with a single
    CSV too.

    Args:
        input_dir (str): Directory to scan for tab-separated text
            files.

    Returns:
        dict: Dictionary mapping file stems to pandas DataFrames."""
    df_dict = {}
    # https://stackoverflow.com/a/10378012 (glob directory)
    pathlist = Path(input_dir).rglob('*.txt')
    for filepath in sorted(pathlist):
        df = csv_to_df(filepath)
        dict_name = os.path.splitext(os.path.basename(filepath))[0]
        # print('...processed', dict_name)
        df_dict[dict_name] = df
    return df_dict


def extract_columns_from_df(df, column_id):
    """Get a column from a dataframe by integer position or by name.

    Args:
        df (pandas.DataFrame): Dataframe to extract the column from.
        column_id (int or str): Integer index (uses iloc) or column
            name (uses loc).

    Returns:
        pandas.Series: The requested column."""
    try:
        column_id = int(column_id)
        column = df.iloc[:, column_id]
    except ValueError:
        column = df.loc[:, column_id]
    return column


def select_variable(df_dict, lon, lat, variable, tmp_dir=TMP_DIR):
    """Select longitude, latitude and a variable column from each
    dataframe and write them to a tab-separated text file per input.

    Raises ValueError when no input file is found in the input
    directory.

    Args:
        df_dict (dict): Dictionary of dataframes keyed by file name.
        lon (int or str): Longitude column index or name.
        lat (int or str): Latitude column index or name.
        variable (int or str): Variable column index or name.
        tmp_dir (str): Directory where the temporary text files are
            written.

    Returns:
        None."""
    # https://stackoverflow.com/a/55388872 (Loop through df_dict)
    if not df_dict:
        raise ValueError(
            "No tab-separated text files were found in the input directory "
            f"'{INPUT_DIR}' (site PBDM output files). 'select_variable()' "
            "cannot select any variable from an empty input directory.")
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
    """Concatenate all dataframes found in input_dir into a single one.

    Args:
        input_dir (str): Directory to scan for tab-separated text
            files.

    Returns:
        pandas.DataFrame: Concatenated dataframe of all inputs."""
    df_dict = csv_to_df_dict(input_dir)
    return pd.concat(df_dict.values(), ignore_index=True)


def test_df_concat(input_dir=INPUT_DIR):
    """ This would be for generating more CSV files that include
        summary statistics for mapping e.g., mean, standard deviation
        and coefficient of variation of yearly values for multi year
        simulations.

        Args:
            input_dir (str): Directory to scan for tab-separated text
                files.

        Returns:
            None."""
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
