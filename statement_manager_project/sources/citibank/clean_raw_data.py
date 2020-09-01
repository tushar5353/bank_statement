import pandas as pd
import numpy as np

def run(pdf_data, config):
    pd.set_option('display.max_rows', None)
    df_list = []
    total_tables = pdf_data.n
    for table_number in range(1, total_tables):
        df_list.append(pdf_data[table_number].df)
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
    data_frame.drop(data_frame[data_frame.iloc[:,1]==''].index, inplace=True)
    data_frame.drop(data_frame[(data_frame.iloc[:,1]=='-') & (data_frame.iloc[:,2]=='') & (data_frame.iloc[:,3]=='') & (data_frame.iloc[:,4]=='')].index, inplace=True)
    data_frame.index = range(len(data_frame.index))
    return data_frame


def clean_data(data_frame, config):
    temp = 0
    for row in data_frame.itertuples():
        if str(row[3]) == '' and str(row[4]) == '' and str(row[5]) == '':
            data_frame[1][temp] = data_frame[1][temp] + row[2]
        else:
            temp = row[0]
    data_frame.drop(data_frame[data_frame.iloc[:,0]==''].index, inplace=True)
    data_frame.rename(columns = {0: 'date', 1: 'description', 2: 'debit',
                                 3: 'credit', 4: 'balance'}, inplace=True)
    data_frame.index = range(len(data_frame.index))
    return data_frame


def change_datatypes(data_frame):
    data_frame['date'] = pd.to_datetime(data_frame['date'], dayfirst=True)
    data_frame['credit'] = pd.to_numeric(data_frame['credit'], errors='coerce')
    data_frame['debit'] = pd.to_numeric(data_frame['debit'], errors='coerce')
    data_frame['balance'] = pd.to_numeric(data_frame['balance'], errors='coerce')
    data_frame = data_frame.replace(np.nan, 0, regex=True)
    return data_frame
