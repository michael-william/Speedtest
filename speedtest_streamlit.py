import pandas as pd
import numpy as np
from datetime import datetime
import datetime
import streamlit as st

# ML libraries
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio
import plotly.offline as pyo
pio.renderers.default = 'iframe'

st.write("""
# Hourly Wifi Speeds 
Measuring my wifi performance throughout the day. Data collection started on July 4th, 2020 with a subscription
plan for 500mbs at 2.4Ghz. On July 24th, the plan was switched to 250mbs at 5Ghz.
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
    title='Overal WiFi Performance',
    barmode='overlay', 
    hovermode='y')

    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(hovermode='closest', xaxis_title="Hour of day",legend_orientation='h',legend=dict(x=.2 , y=1.2), yaxis_title="Value", xaxis_dtick=2)
    
    return fig

@st.cache(allow_output_mutation=True)
def violin(df,df2):
    fig = make_subplots(rows=1, cols=3)

    fig.add_trace( go.Violin(
    y=df['download'],
    opacity = 0.75,
    hoverinfo="name + y",
    name='Down 500 plan',
    box_visible=True,
    points='all',
    meanline_visible=True),
    row=1, col=1)
    
    fig.add_trace( go.Violin(
    y=df2['download'],
    opacity = 0.75,
    hoverinfo="name + y",
    name='Down 250 plan',
    box_visible=True,
    points='all',
    marker_color='darkblue',
    meanline_visible=True),
    row=1, col=1)

    fig.add_trace( go.Violin(
    y=df['upload'],
    opacity = 0.75,
    hoverinfo="name+y",
    name = 'Up 500 plan',
    box_visible=True,
    points='all', 
    meanline_visible=True),
    row=1, col=2)
    
    fig.add_trace( go.Violin(
    y=df2['upload'],
    opacity = 0.75,
    hoverinfo="name+y",
    name = 'Up 250 plan',
    box_visible=True,
    points='all', 
    marker_color='darkgreen',
    meanline_visible=True),
    row=1, col=2)

    fig.add_trace( go.Violin(
    y=df['ping'],
    opacity = 0.75,
    hoverinfo="name + y",
    name='Ping 500 plan',
    box_visible=True,
    points='all', 
    meanline_visible=True),
    row=1,col=3)
    
    fig.add_trace( go.Violin(
    y=df2['ping'],
    opacity = 0.75,
    hoverinfo="name + y",
    name='Ping 250 plan',
    box_visible=True,
    points='all',
    marker_color='darkorange',
    meanline_visible=True),
    row=1,col=3)

    fig.update_layout(hovermode='closest', yaxis_title="Measures",showlegend=True)
    
    return fig
    

def user_input_features():
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        start_date = st.sidebar.date_input('Start date', datetime.date(2020,7,4))
        end_date = st.sidebar.date_input('End date', tomorrow)
        if start_date > end_date:
            st.sidebar.error('Error: End date must fall after or on start date.')
        if start_date > datetime.date(2020,7,23):
            st.sidebar.error('Error: Start must be less than 2020-7-24.')
        if end_date < datetime.date(2020,7,24):
            st.sidebar.error('Error: End must be greater than 2020-7-23.')
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
    df_base = int_data.query('date >= @start_date and date <= @end_date')
    switch_date = df_base.query('date == "2020-07-23" and hour == 17').index[0]
    df = df_base.iloc[:switch_date]
    df2 = df_base.iloc[switch_date:]
    stats = pd.DataFrame(df.describe()).round(decimals=2)
    stats2 = pd.DataFrame(df2.describe()).round(decimals=2)
    fig = viz(df)
    figv = violin(df,df2)

    st.subheader('Selected Date Range')
    st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
    st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(figv, use_container_width=True)
    st.subheader('Wifi stats from the 500 mbs plan')
    st.write(stats.loc[['count', 'mean', 'max', 'min', 'std']][['download', 'upload','ping','hour']])
    st.subheader('Wifi stats from the 250 mbs plan')
    st.write(stats2.loc[['count', 'mean', 'max', 'min', 'std']][['download', 'upload','ping','hour']])
    

    #def user_update():
      #  st.write(date_range) 

    #if st.sidebar.button('Show'):
     #   user_update()

    


if __name__ == "__main__":
    main()