import pandas as pd
import numpy as np

def run(pdf_data, config):
    pd.set_option('display.max_rows', None)
    df_list = []
    total_tables = pdf_data.n
    df_list = [pdf_data[table_number].df for table_number in range(0, total_tables)]
    data_frame = pd.concat(df_list)
    data_frame.index = range(len(data_frame.index))
    final_data = clean_file(data_frame, config)
    change_datatypes(final_data)
    return final_data

def clean_file(data_frame, config):
    data_frame = remove_column_name(data_frame)
    data_frame = remove_header_and_page_info(data_frame)
    data_frame = clean_data(data_frame, config)

    return data_frame

def remove_column_name(data_frame):
    data_frame.columns = range(data_frame.shape[1])

    return data_frame


def remove_header_and_page_info(data_frame):
    data_frame.drop(data_frame[data_frame.iloc[:,0]=='Date'].index, inplace=True)
    return data_frame


def clean_data(data_frame, config):
    data_frame[1].replace(to_replace=r"\n", value="", regex=True, inplace=True)
    data_frame.drop([2,3], axis=1, inplace=True)
    data_frame = remove_column_name(data_frame)
    data_frame.rename(columns = {0: 'date', 1: 'description', 2: 'debit',
                                 3: 'credit', 4: 'balance'}, inplace=True)
    return data_frame


def change_datatypes(data_frame):
    data_frame['date'] = pd.to_datetime(data_frame['date'], dayfirst=True)
    data_frame['credit'] = data_frame['credit'].str.replace(",", "").astype(float)
    data_frame['debit'] = data_frame['debit'].str.replace(",", "").astype(float)
    data_frame['balance'] = data_frame['balance'].str.replace(",", "").astype(float)
    return data_frame
