""" Read a tab-separated text file into a dictionary, return (numbered)
column names, number of rows, and the dictionary itself.
"""
import os
import pandas as pd


INPUT_FOLDER = os.path.join(os.getcwd(), 'casas_gis/input_data')


def get_ascii_table(filename, path=INPUT_FOLDER):
    df = pd.read_csv("path/filename")
    return df


get_ascii_table("Olive_30set19_00002.txt")

# def get_table_info(table):
