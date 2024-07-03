import numpy as np
import plotly.figure_factory as ff


def medal_tally(df):
    # the problem here is that if a team has won a gold medal then all the players are represented indivisually and thus medal count
    # goes far more than it should be. Thus we have to drop duplicates based on a subset of features

    medal_tally = df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])

    # again calculating the tally
    medal_tally = medal_tally.groupby("region").sum()[["Gold", "Silver", "Bronze"]].sort_values("Gold",
                                                                                                ascending=False).reset_index()

    # making a total medals columns
    medal_tally["Total"] = medal_tally["Gold"] + medal_tally["Silver"] + medal_tally["Bronze"]

    #converting column elements to integers
    medal_tally["Gold"] = medal_tally["Gold"].astype("int")
    medal_tally["Silver"] = medal_tally["Silver"].astype("int")
    medal_tally["Bronze"] = medal_tally["Bronze"].astype("int")
    medal_tally["Total"] = medal_tally["Total"].astype("int")

    return medal_tally

#function to return list of years and countries
def country_year_list(df):

    #extracting years
    years = df["Year"].unique().tolist()
    years.sort()
    years.insert(0, "Overall")

    #extracting countries
    country = np.unique(df["region"].dropna().values).tolist()
    country.sort()
    country.insert(0, "Overall")

    return years, country


# creating a function to display medals of a specific country in a specific year
def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])
    flag = 0

    if year == "Overall" and country == "Overall":
        temp_df = medal_df

    if year == "Overall" and country != "Overall":
        flag = 1
        temp_df = medal_df[medal_df["region"] == country]

    if year != "Overall" and country == "Overall":
        temp_df = medal_df[medal_df["Year"] == year]

    if year != "Overall" and country != "Overall":
        temp_df = medal_df[(medal_df["Year"] == year) & (medal_df["region"] == country)]

    if flag == 1:
        x = temp_df.groupby("Year").sum()[["Gold", "Silver", "Bronze"]].sort_values("Year",
                                                                                    ascending=True).reset_index()
    else:
        x = temp_df.groupby("region").sum()[["Gold", "Silver", "Bronze"]].sort_values("Gold",
                                                                                      ascending=False).reset_index()

    x["Total"] = x["Gold"] + x["Silver"] + x["Bronze"]

    return x


#function to return dataframe of yearwise participation
def data_over_years(df,col):

    data_over_time = df.drop_duplicates(["Year", col])["Year"].value_counts().reset_index().sort_values(
        "Year")

    return data_over_time


#function to return most successful athlete
def most_successful(df, sport):
    temp_df = df.dropna(subset=["Medal"])

    if sport != "Overall":
        temp_df = temp_df[temp_df["Sport"] == sport]
        x = temp_df["Name"].value_counts().reset_index().head(15).merge(df, on="Name")[
            ["Name", "count", "region"]].drop_duplicates(subset=["Name"])
    else:
        x = temp_df["Name"].value_counts().reset_index().head(15).merge(df, on="Name")[
            ["Name", "count", "Sport", "region"]].drop_duplicates(subset=["Name"])

    x.rename(columns={"count": "Medals"}, inplace=True)
    return x


#function to return yearwise country medal tally df
def yearwise_country_medals(df,country):

    temp_df = df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"], inplace=True)

    temp_df2 = temp_df[temp_df["region"] == country]
    final_df = temp_df2.groupby("Year").count()["Medal"].reset_index()

    return final_df


#function to return country's performance in each sport
def country_event_heatmap(df,country):

    temp_df = df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"], inplace=True)

    temp_df2 = temp_df[temp_df["region"] == country]

    pt =temp_df2.pivot_table(index="Sport", columns="Year", values="Medal", aggfunc="count").fillna(0).astype("int")

    return pt


#function to display most successful athletes in a country
def most_successful_athletes(df, country):
    temp_df = df.dropna(subset=["Medal"])

    temp_df = temp_df[temp_df["region"] == country]

    x = temp_df["Name"].value_counts().reset_index().head(10).merge(df, on="Name")[
        ["Name", "count", "Sport"]].drop_duplicates(subset=["Name"])
    x.rename(columns={"count":"Medals"},inplace=True)

    return x

#function to display age distribution in individual sports
def sportwise_age_distribution(df):

    athlete_df = df.drop_duplicates(subset=["Name", "region"])

    famous_sports_df = df["Sport"].value_counts().reset_index().sort_values("count", ascending=False).head(15)
    famous_sports_df

    famous_sports = famous_sports_df["Sport"].unique().tolist()
    famous_sports

    x = []
    names = []

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df["Sport"] == sport]
        x.append(temp_df[temp_df["Medal"] == "Gold"]["Age"].dropna())
        names.append(sport)

    fig = ff.create_distplot(x, names, show_hist=False, show_rug=False)

    return fig