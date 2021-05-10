import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
def line_chart(data,Training_start_date, Training_end_data, 
                        Testing_start_date,Testing_end_data,Analysis_column):
    st.header('**Training and Testing Data**')
    data['ds'] = pd.to_datetime(data['ds'], format="%Y%m%d").dt.date
    
    train_data = data[data['ds']<=Training_end_data]
    
    train_data = train_data[train_data['ds']>=Training_start_date]
    
    test_data = data[data['ds']>=Testing_start_date]
    test_data = test_data[test_data['ds']<=Testing_end_data]
    
    fig = make_subplots(rows=1, cols=2)
    fig.add_trace(
        go.Scatter(x=train_data['ds'],y=train_data['y'],
                mode = 'lines', name='Training Data'),
        row = 1, col=1
    )

    fig.add_trace(
        go.Scatter(x=test_data['ds'],y=test_data['y'],
            name='Test Data'),  
        row = 1, col=2
    )
    fig.update_xaxes(title_text = 'Time Period', row=1, col =1)
    fig.update_yaxes(title_text = Analysis_column, row=1, col =1)
    fig.update_layout(
                        plot_bgcolor = '#FFF', autosize=False, width=1100, height=400)
                        
    st.plotly_chart(fig)


def box_plot(data,Analysis_column):
    st.header('**Data Analysis**')
    box_train = data
    box_train['ds'] = pd.to_datetime(box_train['ds'])
    box_train['Hourly'] = box_train['ds'].dt.hour
    box_train['Daily'] = box_train['ds'].dt.day
    box_train['Monthly'] = box_train['ds'].dt.month
    box_train['Yearly'] = box_train['ds'].dt.year
    daily = box_train.groupby(['Daily'],as_index=False)['y'].mean()
    Monthly = box_train.groupby(['Monthly'],as_index=False)['y'].mean()
    Yearly = box_train.groupby(['Yearly'],as_index=False)['y'].mean()

    fig = make_subplots(rows=3, cols=2)
    fig.add_trace(
        go.Scatter(x=daily.index,y=daily['y'],
                name='Daily Trend'),
        row = 1, col=1
    )
    fig.add_trace(
        go.Box(x=box_train['Daily'],y=box_train['y'],
            name='Daily Trend BoxPlot'),  
        row = 1, col=2
    )
    fig.add_trace(
        go.Scatter(x=Monthly.index,y=Monthly['y'],
                name='Monthly Trend'),
        row = 2, col=1
    )
    fig.add_trace(
        go.Box(x=box_train['Monthly'],y=box_train['y'],
            name='Monthly Trend BoxPlot'),  
        row = 2, col=2
    )
    fig.add_trace(
        go.Scatter(x=Yearly['Yearly'],y=Yearly['y'],
                name='Yearly Trend'),
        row = 3, col=1
    )
    fig.add_trace(
        go.Box(x=box_train['Yearly'],y=box_train['y'],
            name='Yearly Trend BoxPlot'),  
        row = 3, col=2
    )
    fig.update_xaxes(title_text = 'Daily Time Period', row=1, col =1)
    fig.update_xaxes(title_text = 'Monthly Time Period', row=2, col =1)
    fig.update_xaxes(title_text = 'Yearly Time Period', row=3, col =1)
    fig.update_yaxes(title_text = Analysis_column, row=1, col =1)
    fig.update_yaxes(title_text = Analysis_column, row=2, col =1)
    fig.update_yaxes(title_text = Analysis_column, row=3, col =1)
    fig.update_layout(
                        plot_bgcolor = '#FFF', autosize=False, width=1100, height=1000,
                        )
    st.plotly_chart(fig)

def information_provided(date_column,Analysis_column,\
                        Training_start_date, Training_end_data, \
                        Testing_start_date,Testing_end_data, data):
    st.header("Information Provided")

    st.markdown('<style>h2{color: #0066ff;text-align:center}</style>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.beta_columns(4)
    with col1:
        st.warning(f'Date Column \
                    \n\
                    **{date_column}**')
    with col2:
        st.warning(f'Analysis Column \
                     \n\
                    **{Analysis_column}**')
    with col3:
        st.warning(f'Training Period from  \
                    \n\
                    **{Training_start_date}** to **{Training_end_data}**')
    with col4:
        st.warning(f'Testing Period from \
                 \n\
                  **{Testing_start_date}** to **{Testing_end_data}**')
    line_chart(data,Training_start_date, Training_end_data,
                        Testing_start_date,Testing_end_data,Analysis_column)
    box_plot(data,Analysis_column)
    anomoly_detection(data,Analysis_column)
    st.dataframe(data)



def anomoly_detection(data,Analysis_column):
    anomoly_data = data
    st.header('**Anomoly Detection**')
    col1,col2= st.beta_columns([1,4])
    with col1:
        st.text('\n \
                \n \
                ')
        window = st.slider('Select Size of Moving Window Average', 2, 3, 7)
    anomoly_data['moving'] = anomoly_data['y'].rolling(window = window, center = True).mean()
    anomoly_data.dropna(inplace=True)
    anomoly_data['diff'] = np.abs((anomoly_data['moving']-anomoly_data['y'])/anomoly_data['y'])*100
    points = anomoly_data[anomoly_data['diff']>20]
    with col2:
        fig = go.Figure()
        
        fig.add_trace(
            go.Scatter(x=anomoly_data.ds,y=anomoly_data['y'],
                    mode = 'lines', name='Original data')
            
        )
        fig.add_trace(
            go.Scatter(x=points.ds,y=points['y'],
                    mode = 'markers', name='Anomoly',
                    )
        )
        fig.add_trace(
            go.Scatter(x=anomoly_data.ds,y=anomoly_data['y'].rolling(window = window, center = True).mean(),
                    mode = 'lines', name='Moving Average')
        )
        
        fig.update_xaxes(title_text = 'Time Period')
        fig.update_yaxes(title_text = Analysis_column)
        fig.update_layout(
                            plot_bgcolor = '#FFF', autosize=False, width=800, height=400)
                            
        st.plotly_chart(fig)
    # del(anomoly_data)
    # st.text(anomoly_data)
    # st.text('gpme')