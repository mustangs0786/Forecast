import pandas as pd 
import statistics
import streamlit as st
from datetime import datetime, timedelta

def date_input(df, date_column,Analysis_column):
    try:
        train = df.copy()
        del(df)
        train.rename(columns={date_column:'ds', Analysis_column:'y'},inplace=True)
        train['ds'] = pd.to_datetime(train['ds'])
        train = train[['ds','y']]
        train.drop_duplicates(subset='ds',keep='first',inplace=True,ignore_index=True)
        year = list(train['ds'].dt.year)
        if len(year)==len(train) and (year[0]==1970):
            st.error('Please select correst date column')
            st.stop()
        else:
            return train
        
    except Exception:
        # st.info(f"Something went wrong Same Columns selected{e} ")
        st.stop()

def H_D_W_M_check(train,date_type):
    if date_type != 'None':
        df = train.copy()
        df['shift'] = df['ds'].shift(1)
        df['shift'] = pd.to_datetime(df['shift'])
        df.dropna(inplace=True)
        df['shift_diff'] = df['ds'] - df['shift']
        df['days_diff'] = df['shift_diff'].dt.days
        m = int(statistics.mode(df['days_diff']))
        # st.dataframe(df)
        # st.text(m)
        if m == 0:
            if date_type != 'Hourly':
                st.warning('It is a Hourly data, Please select Hourly')
                st.stop()
            else:
                del(df)
                return 'H'
        elif m==1:
            if date_type != 'Daily':
                st.warning('It is a Daily data, Pleaes select Daily')
                st.stop()
            else:
                del(df)
                return 'D'
        elif m==7:
            if date_type != 'Weekly':
                st.warning('It is a Weekly data, Pleaes select Weekly')
                st.stop()
            else:
                del(df)
                return 'W'
        elif (m==31) or (m==30):
            if date_type != 'Monthly':
                st.warning('It is a Monthly data, Pleaes select Monthly')
                st.stop()
            else:
                del(df)
                return 'M'
    else:
        st.stop()
        

def miss_date_check(data,date_type_return):
    # st.dataframe(data)
    data = data.set_index('ds')
    # st.dataframe(data)
    data = data.asfreq(date_type_return, method = 'ffill')
    null_count = data['y'].isnull().sum()+1
    data['y'] = data['y'].fillna(data.y.rolling(null_count,min_periods=1).mean())
    # data.dropna(inplace=True)
    data['ds'] = data.index
    # data = data[['ds','y']]
    # st.dataframe(data)
    return data

def train_test_data(data):
    try:
        start = data['ds'].min()
        end = data['ds'].max()
        Training_start_date, Training_end_data = st.sidebar.date_input(
            'select Training date range',[start,end], min_value=start,max_value=end)
        test_start = Training_end_data+timedelta(1)
        Testing_start_date, Testing_end_data = st.sidebar.date_input(
            'select Training date range',[start,end], min_value=test_start,max_value=end)

        # st.text(f'{Training_start_date}---{Training_end_data}')
        # st.text(f'{Testing_start_date}---{Testing_end_data}')
        return Training_start_date, Training_end_data, Testing_start_date,Testing_end_data
    except Exception:
        st.info('Please select both start date and end date')
    


    