import streamlit as st
import pandas as pd
import helper
import pickle as pkl
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

#importing main df from pickle file
df = pkl.load(open("../dataframe1.pkl", "rb"))

#showing sidebar with radio button
st.sidebar.title("Olmpics Analysis")
user_menu = st.sidebar.radio(
    "Select an option",
    ("Medal Tally","Overall Analysis","Country-wise Analysis","Athlete-wise Analysis")
)


#if user selects Medal Tally
if user_menu == "Medal Tally":

    #printing header
    st.sidebar.header("Medal Tally")

    #importing years and countries list from helper file
    years , country = helper.country_year_list(df)

    #printing sidebar dropdowns
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    #importing medals df from helper file
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    #printing headers
    if selected_year == "Overall" and selected_country == "Overall":
        st.title("Overall Tally")
    if selected_year != "Overall" and selected_country == "Overall":
        st.title("Medal Tally in " + str(selected_year))
    if selected_year == "Overall" and selected_country != "Overall":
        st.title("Medal Tally for " + selected_country)
    if selected_year != "Overall" and selected_country != "Overall":
        st.title("Medal Tally for " + selected_country + " in " + str(selected_year))

    #printing medals df
    st.table(medal_tally)



#if user selects Overall Analysis
if user_menu == "Overall Analysis":

    editions = df["Year"].unique().shape[0]-1
    cities = df["City"].unique().shape[0]
    sports = df["Sport"].unique().shape[0]
    events = df["Event"].unique().shape[0]
    athletes = df["Name"].unique().shape[0]
    nations = df["region"].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Cities")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nations)


    #displying yearwise nation participation graph
    yearwise_nation_count = helper.data_over_years(df,"region")
    fig = px.line(yearwise_nation_count, x= "Year", y = "count")
    st.title("Participating Nations Over the Years")
    st.plotly_chart(fig)

    # displying yearwise event count graph
    yearwise_event_count = helper.data_over_years(df,"Event")
    fig = px.line(yearwise_event_count, x="Year", y="count")
    st.title("Events Held Over the Years")
    st.plotly_chart(fig)

    # displying yearwise event count graph
    yearwise_event_count = helper.data_over_years(df, "Name")
    fig = px.line(yearwise_event_count, x="Year", y="count")
    st.title("Athletes Participated Over the Years")
    st.plotly_chart(fig)

    #displaying heatmap of the number of events in each sport in each year
    st.title("No. of Events in each Year")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(["Year", "Sport", "Event"])
    ax = sns.heatmap(x.pivot_table(index="Sport",columns="Year", values = "Event", aggfunc="count").fillna(0).astype("int"), annot=True)
    st.pyplot(fig)

    #displaying most successful people
    st.title("Most Successful Athlete")

    sports_list = df["Sport"].unique().tolist()
    sports_list.sort()
    sports_list.insert(0,"Overall")

    selected_sport = st.selectbox("Select a sport", sports_list)

    x = helper.most_successful(df,selected_sport)
    st.table(x)

#if user selects Country-wise Analysis
if user_menu == "Country-wise Analysis":

    #sidebar
    st.sidebar.title("Yearwise Country Performance")

    country_list = df["region"].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox("Select a country", country_list)


    #display yearwise country performance
    yearwise_country_medal_tally = helper.yearwise_country_medals(df,selected_country)

    st.title(selected_country + " Medal Tally")

    fig = px.line(yearwise_country_medal_tally, x ="Year", y = "Medal")
    st.plotly_chart(fig)


    #display yearwise performance of a country in each sport
    st.title(selected_country + " Medal Tally in Individual Sport")
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    #display most successful athletes in a country
    top_10_athletes = helper.most_successful_athletes(df,selected_country)
    st.title("Top 10 Successful Athletes of " + selected_country)
    st.table(top_10_athletes)

#if user selects athlete-wise analysis
if user_menu == "Athlete-wise Analysis":

    #displaying age distribution of athletes
    athlete_df = df.drop_duplicates(subset=["Name", "region"])
    x1 = athlete_df["Age"].dropna()
    x2 = athlete_df[athlete_df["Medal"] == "Gold"]["Age"].dropna()
    x3 = athlete_df[athlete_df["Medal"] == "Silver"]["Age"].dropna()
    x4 = athlete_df[athlete_df["Medal"] == "Bronze"]["Age"].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ["Overall Age", "Gold Medalist", "Silver Medalist", "Bronze Medalist"],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width = 1000, height = 600)
    st.title("Distribution of Age Medal-wise")
    st.plotly_chart(fig)

    #display sportwise distribution in individual sports
    st.title("Distribution of Age Sport-wise (Gold)")
    fig = helper.sportwise_age_distribution(df)
    st.plotly_chart(fig)