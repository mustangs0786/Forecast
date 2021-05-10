import streamlit as st 
import pandas as pd 
from streamlit import caching
from datetime import datetime
from parameters import *
from Date_eda import *
import time 
import sys
import datetime
import numpy as np 
from eda import *
st.set_page_config(layout="wide", page_icon=":art:", page_title="Custom Theming")

st.title("**Forecasting App**")

st.markdown('<style>h1{color: #FF6A33;text-align:center}</style>', unsafe_allow_html=True)

uploaded_data = st.sidebar.file_uploader(label='Enter Data File', accept_multiple_files=False, type=['csv','xlsx'])
def main(uploaded_data):
    if uploaded_data != None:
        # @st.cache(persist=False,suppress_st_warning=True,allow_output_mutation=True)
        def read_data(uploaded_data):
            try:
                df = pd.read_excel(uploaded_data)
                return df
            except:
                df = pd.read_csv(uploaded_data)
                return df

        df = read_data(uploaded_data)
        return df
    else:
        st.image(img_path, use_column_width=True)
        st.stop()

if __name__ == "__main__":
    data = main(uploaded_data)
    # data = pd.read_csv(r'./opsd_germany_daily.csv')
    # st.dataframe(data)
    date_column = st.sidebar.selectbox('Please Select the Date Column only',list(data.columns))
    Analysis_column = st.sidebar.selectbox('Please Select the Analysis Column only',list(data.columns))
    data = date_input(data, date_column,Analysis_column)
    
    date_type = st.sidebar.selectbox('Please Select Data is Hourly,Daily,Weekly,Monthly' \
                                    ,('None','Hourly','Daily','Weekly','Monthly'))
    date_type_return = H_D_W_M_check(data,date_type)
    # st.dataframe(data)
    data = miss_date_check(data,date_type_return)
    try:
        Training_start_date, Training_end_data, Testing_start_date,Testing_end_data = train_test_data(data)
    except Exception:
        st.text(' ')
    section = st.sidebar.radio('Operational Section',('None','Run Eda','Modelling'))
    if section == 'Run Eda':
        try:
            information_provided(date_column,Analysis_column,\
                                Training_start_date, Training_end_data, \
                                Testing_start_date,Testing_end_data,data)
        except Exception:
            st.stop()
    else :
        st.stop()


    

