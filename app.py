import streamlit as st
import pandas as pd
import numpy as np
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')

df=preprocessor.preprocess(df,region_df)
st.sidebar.title('Olympics Analysis')
user_menu = st.sidebar.radio(
    'Choose an option',
    ('Medal Tally','Overall Analysis','Country wise analysis','Athlete-wise analysis')
)
# st.dataframe(df)

if(user_menu=='Medal Tally'):
    st.sidebar.header("Medal Tally")
    years,country = helper.country_years_list(df)
    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country",country)

    medal_tally= helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_country =='Overall' and selected_year=='Overall':
        st.title('Overall Medal Tally')
    if selected_country !='Overall' and selected_year=='Overall':
        st.title('Overall Medal Tally of '+selected_country)
    if selected_country =='Overall' and selected_year!='Overall':
        st.title('Overall Medal Tally in Year '+ str(selected_year) + ' Olympics')
    if selected_country !='Overall' and selected_year!='Overall':
        st.title(' Medal Tally of '+ selected_country + ' in '+ str(selected_year))

    st.table(medal_tally)

if(user_menu=='Overall Analysis'):
    editions= df['Year'].unique().shape[0] -1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nation = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nation)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time=helper.data_over_time(df,'region')
    fig= px.line(nations_over_time,x='Year',y='region')
    st.title('Participating Nations over years')
    st.plotly_chart(fig )

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Year', y='Event')
    st.title('Total Events over Years')
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x='Year', y='Name')
    st.title('Total Athlete Participating over Years')
    st.plotly_chart(fig)


    st.title("Number of Events over time (Every Sport)")
    # fig , ax = plt.figure(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    fig = plt.figure(figsize=(20, 20))
    sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport=st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if(user_menu=='Country wise analysis'):
    country_list = np.unique(df['region'].dropna().values).tolist()
    country_list.sort()
    st.sidebar.title('Country wise analysis')
    selected_country = st.sidebar.selectbox("Select A Country", country_list,placeholder="Choose a Country")
    country_df=helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country+' Medal Tally Over the Years')
    st.plotly_chart(fig)

    st.title(selected_country + ' excels in the following events')
    pt=helper.country_event_heatmap(df,selected_country)
    fig = plt.figure(figsize=(20, 20))
    sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title('Top 10 Athletes of ' + selected_country)
    top_10_df = helper.most_successful_per_country(df, selected_country)
    st.table(top_10_df)



if(user_menu=='Athlete-wise analysis'):
    athlete_df= df.drop_duplicates(subset=['Name','region'])

    x1=athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()

    fig=ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)
