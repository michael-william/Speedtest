import pandas as pd
import numpy as np
from datetime import datetime
import datetime
import streamlit as st

# ML libraries
import plotly.graph_objs as go
import plotly.io as pio
import plotly.offline as pyo
pio.renderers.default = 'iframe'

st.write("""
# Hourly Wifi Speeds 
Measuring my wifi performance throughout the day. My plan says I should have a 
maximum download speed of 500 mbs.
""")

@st.cache

def load_data(allow_output_mutation=True):
    
    data_source = 'https://github.com/michael-william/Speedtest/raw/master/speedtest_logs.csv'
    raw_data=pd.read_csv(data_source, parse_dates=[3,4])
    raw_data.rename(columns={'time':'hour'}, inplace=True)
    raw_data['hour'] = raw_data.hour.dt.round('H').dt.hour
    raw_data['week'] = raw_data.date.dt.week
    raw_data['month'] = raw_data.date.dt.month
    return raw_data


@st.cache(allow_output_mutation=True)
def viz(df):
    ping = go.Bar(
    x=df['hour'],
    y=df['ping'],
    opacity = 0.75,
    hoverinfo="name + y",
    name='Ping(ms)')

    down = go.Bar(
    x=df['hour'],
    y=df['download'],
    opacity = 0.75,
    hoverinfo="name + y",
    name='Download (mbs)')

    up = go.Bar(
    x=df['hour'],
    y=df['upload'],
    opacity = 0.75,
    hoverinfo="name + y",
    name = 'Upload (mbs)')

    data = [down, up, ping]

    layout = go.Layout(
    title='WiFi Stats',
    barmode='overlay', 
    hovermode='y')

    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(hovermode='closest')
    
    return fig

@st.cache(allow_output_mutation=True)
def violin(df):

    ping = go.Violin(
    y=df['ping'],
    opacity = 0.75,
    hoverinfo="name + y",
    name='Ping(ms)',
    box_visible=True,
    points='all', 
    meanline_visible=True)

    down = go.Violin(
    y=df['download'],
    opacity = 0.75,
    hoverinfo="name + y",
    name='Download (mbs)',
    box_visible=True,
    points='all',
    meanline_visible=True)

    up = go.Violin(
    y=df['upload'],
    opacity = 0.75,
    hoverinfo="name+y",
    name = 'Upload (mbs)',
    box_visible=True,
    points='all', 
    meanline_visible=True)

    data = [down, up, ping]

    layout = go.Layout(
    title='Range',
    barmode='overlay', 
    hovermode='y')

    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(hovermode='closest')
    
    return fig
    

def user_input_features():
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        start_date = st.sidebar.date_input('Start date', datetime.date(2020,7,4))
        end_date = st.sidebar.date_input('End date', tomorrow)
        if start_date <= end_date:
            st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
        else:
            st.sidebar.error('Error: End date must fall after or on start date.')
        #st.sidebar.text('City: '+(location.raw['display_name'].split(',')[3]))
        #st.sidebar.text('Longitude: '+str(longitude))
        #st.sidebar.text('Latitude: '+str(latitude))
        #latitude = st.sidebar.slider('Latitude', 50.770041, 53.333967, 51.2)
        #longitude = st.sidebar.slider('Longitude', 3.554188, 7.036756, 5.2)
        #p_type = st.sidebar.selectbox('Apartment',['Room', 'Studio', 'Apartment', 'Anti-squat', 'Student residence'])
        data = {'Start date':start_date, 'End date':end_date}
        date_range = pd.DataFrame(data, columns=['Start date', 'End date'], index=[0])
        return date_range

def main():
    int_data=load_data()
    st.sidebar.header('Select date range')
    st.sidebar.markdown('Data collection started on 2020/07/04 and is collected every hour')
    date_range = user_input_features()
    start_date = date_range['Start date'][0]
    end_date = date_range['End date'][0]
    df = int_data.query('date >= @start_date and date <= @end_date')
    stats = pd.DataFrame(df.describe()).round(decimals=2)
    fig = viz(df)
    figv = violin(df)

    st.subheader('Date Range')
    st.write(date_range)
    st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(figv, use_container_width=True)
    st.write(stats.loc[['count', 'mean', 'max', 'min', 'std']][['ping', 'download', 'upload', 'hour']])
    

    #def user_update():
      #  st.write(date_range) 

    #if st.sidebar.button('Show'):
     #   user_update()

    


if __name__ == "__main__":
    main()




