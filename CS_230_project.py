"""
Name: Abby Hunsinger
CS230: Section 7
Data: Air Quality Index Dataset
URL: https://csproject-8wk3bl3hbmu7fyhtkxoyey.streamlit.app/

Description:
This website is a representation of what we as a group have learned in this class and how we can apply it in various areas.
We worked as a team to come up with ways to represent the data, including charts, maps, and other widgets.
The code below is what we used to construct this website from the bottom-up, using applications like Streamlit, Panda, Numpy, Dataframes, PyDeck, Seaborn, MatPlotLib, and Python.
The code analyzes the AQI data, adding it to different types of dictionaries and lists, each serving a different purpose.
We also referenced AI support tools to assist us where we needed.
Please enjoy our AQI App!
"""

#importing necessary features
import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="AQI App CS-230", layout="wide")

#[ST4] Streamlit Sidebar
#code for sidebar based on output from ChatGPT, see code 7 from supplemental document
st.sidebar.title("Air Quality App Guide")
st.sidebar.markdown("""
Welcome to the Air Quality App Dashboard!

Key app features:

    - Explore air quality by country
    - Compare two countries' average AQI
    - Filter based on average AQI
    - View global AQI values on the interactive map!
    
""")



# [DA1] Clean the data
st.title("Air Quality Indices Worldwide")

df=pd.read_excel("AQI_dataset_2.xlsx")

df.rename(columns={
    "AQI Value": "AQI",
    "PM2.5 AQI Value": "PM2.5",
    "Ozone AQI Value": "Ozone",
    "CO AQI Value": "CO",
    "NO2 AQI Value": "NO2"
}, inplace=True)

df.drop_duplicates(subset=["City"], keep='first', inplace=True)

st.write("""This website focuses on the Air Quality around the world. 
    It will demonstrate/present information necessary for people to make decisions regarding personal and economic commitments. 
    All hemispheres will be represented, along with why they have the air qualities they do. 
    The website will also allow consumers to gain a well-rounded knowledge of the areas in which they reside or places they intend to travel to. 
    Enjoy!
""")
st.subheader("Raw AQI Data")
st.dataframe(df)
st.write("""Presented above is the raw data of the air qualities we examined for this project. 
    Indicated above is the Air quality Index, different types of particulate matter, and descriptions of each country's AQI. 
    For example, it can be determined that Seoul, Korea has a poor air quality of 421. 
    From what we know about this area, we can assume that things like smoking and carbon emissions contributed to these results. """)



# [PY1] A function with two or more parameters
# [PY2] A function that returns more than one value
# [PY4] A dictionary where you write code to access its keys, values, or items
# [DA8] Iterating over a dictionary
def get_country_aqi_avg(df, aqi):
    country_dict={}
    for _, row in df.iterrows():
        country=row["Country"]
        value=float(row[aqi])

        if country in country_dict:
            country_dict[country].append(value)
        else:
            country_dict[country]=[value]

    country_avg={}
    for country, values in country_dict.items():
        country_avg[country]=sum(values)/len(values)

    return country_avg



#[SEA1] Frequency Distribution Chart
#code for frequency chart based on ChatGPT code, see code 1 on supplemental document
country_avg_dict = get_country_aqi_avg(df,"AQI")
country_avg_df = pd.DataFrame(list(country_avg_dict.items()), columns=['Country', 'Avg_AQI'])

st.subheader("Average AQI Distribution by Country")
fig, ax = plt.subplots()
sns.histplot(country_avg_df['Avg_AQI'], bins=20, kde=True, ax=ax)
ax.set_xlabel("Average AQI")
ax.set_ylabel("Number of Countries")
ax.set_title("Histogram of Country-Level AQI Averages")
st.pyplot(fig)



#[ST1] Selectbox
#[DA4] Filter data by one condition
#code for selectbox based on ChatGPT code, see code 2 on supplemental document
st.subheader("Explore AQI by Country")

indiv_countries=sorted(df['Country'].dropna().unique())
selected_country = st.selectbox("Select a Country", indiv_countries)

if selected_country:
   country_data=df[df["Country"]==selected_country]
   country_avg_dict=get_country_aqi_avg(df,"AQI")

   if selected_country in country_avg_dict:
       avg_aqi=round(country_avg_dict[selected_country],2)
       st.markdown(f"Average AQI in {selected_country}: {avg_aqi}")
st.markdown(f"Cities in {selected_country} and their AQI Values:")
st.dataframe(country_data[["City", "AQI"]].sort_values(by='AQI', ascending=False))
st.write("""The use of the select box is to depict the overall air quality of countries of interest for the user. 
    Things like the countries’ AQI Averages, the cities indicated in the original dataset and their individual AQIs are shown. 
    They are organized by worst air quality to best air quality. """)



#[ST2] comparing countries side by side
#code for country comparison feature based on ChatGPT code, see code 6 on supplemental document
st.subheader("Compare Countries by Average AQI")

comparison_countries = st.multiselect(
    "Select Countries to Compare",
    options=sorted(country_avg_df["Country"].astype(str)),
    default=['Australia','India']
)
if comparison_countries:
    comparison_df = country_avg_df[country_avg_df["Country"].isin(comparison_countries)]
    st.markdown("### Average AQI by Selected Countries")
    st.dataframe(comparison_df)
st.write("""The side-by-side AQI comparison chart is a useful tool for users who want to directly compare air quality levels across multiple regions. 
    This feature is especially helpful for those planning travel, relocation, or even outdoor activities, allowing them to assess which areas currently have the cleanest air. 
    By visually comparing AQI values for selected cities or countries over time, you can make more informed decisions based on the data. 
    This is even more beneficial for people with respiratory conditions or sensitivities to pollutants like carbon monoxide, ozone, or particulate matter (PM2.5/PM10), helping them identify safer environments and avoid high-risk locations.
""")


#[DA3] find top largest values
#[PY3] Lists (max countries aqi for bar chart)
#[CHART1] bar chart with top countries, find top 5 max and add to list
#code for bar chart based on ChatGPT code, see code 3 on supplemental document
top5_countries=[]
top5_values=[]

for country in country_avg_dict:
    avg=country_avg_dict[country]

    if len(top5_values)<5:
        top5_countries.append(country)
        top5_values.append(avg)
    else:
        min_avg=min(top5_values)
        min_index=top5_values.index(min_avg)

        if avg>min_avg:
            top5_values[min_index]=avg
            top5_countries[min_index]=country

st.subheader("Top 5 Countries with the Worst Air Quality")
fig, ax = plt.subplots()
bars = ax.bar(top5_countries, top5_values, color="purple")
ax.set_title("Top 5 Most Polluted Countries (Avg AQI)")
ax.set_xlabel("Country")
ax.set_ylabel("Average AQI")

for bar in bars:
    height=bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height + 2, f"{height:.1f}", ha='center')

st.pyplot(fig)



#[CHART2] Pie Chart for Descriptive Values
#code for pie chart based on ChatGPT code, see code 4 on supplemental document
aqi_counts={}

for _, row in df.iterrows():
    cat=row["AQI Category"]

    if cat in aqi_counts:
        aqi_counts[cat]+=1
    else:
        aqi_counts[cat]=1

st.subheader("Air Quality Descriptive Characteristics")
labels=list(aqi_counts.keys())
sizes=list(aqi_counts.values())

colors=['blue','green','yellow','orange', 'red','maroon']

fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors[:len(labels)])
ax.axis('equal')
ax.set_title("Breakdown of Global AQI Categories")

st.pyplot(fig)
st.write("""The Pie chart shows the distribution of Good, Moderate, Unhealthy, Very Unhealthy, Unhealthy for Sensitive Groups, and Hazardous in relation to the entire data set.
         As you can see from the data set, most of the countries are in the good/moderate range with few of them landing in hazardous or very unhealthy range.  """)


#[ST3] slider
#code for slider based on ChatGPT code, see code 5 on supplemental document
st.subheader("Filter Countries by Average AQI")

country_avg_dict = get_country_aqi_avg(df, "AQI")
country_avg_df = pd.DataFrame(list(country_avg_dict.items()), columns=['Country', 'Avg_AQI'])

min_avg = int(country_avg_df['Avg_AQI'].min())
max_avg = int(country_avg_df['Avg_AQI'].max())

aqi_range = st.slider(
    "Select average AQI range",
    min_value=min_avg,
    max_value=max_avg,
    value=(min_avg, max_avg)
)
filtered_df = country_avg_df[
    (country_avg_df['Avg_AQI'] >= aqi_range[0]) &
    (country_avg_df['Avg_AQI'] <= aqi_range[1])
]
st.dataframe(filtered_df)



#[MAP]
#code for interactive map based on code from ChatGPT, see code 8 in supplemental document
st.title("Interactive World Map")
country_coordinates={}

for _, row in df.iterrows():
    country=row["Country"]
    latitude=row["lat"]
    longitude=row["lng"]

    if country not in country_coordinates:
        country_coordinates[country]=(latitude, longitude)

country_avg_df['lat'] = country_avg_df['Country'].map(lambda x: country_coordinates.get(x, (None, None))[0])
country_avg_df['lon'] = country_avg_df['Country'].map(lambda x: country_coordinates.get(x, (None, None))[1])

def get_aqi_color(avg_aqi):
    if avg_aqi>250:
        return [128, 0, 0, 160]
    elif avg_aqi>200:
        return [153, 0, 76, 160]
    elif avg_aqi>150:
        return [255, 0, 0, 160]
    elif avg_aqi>100:
        return [255, 165, 0, 160]
    else:
        return [0, 255, 0, 160]

country_avg_df['color'] = country_avg_df['Avg_AQI'].apply(get_aqi_color)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=country_avg_df,
    get_position='[lon, lat]',
    get_fill_color='color',
    get_radius=500000,
    pickable=True,
    auto_highlight=True
)
view_state = pdk.ViewState(
    latitude=0,
    longitude=0,
    zoom=1.2,
    pitch=30
)
deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{Country}\nAverage AQI: {Avg_AQI}"},
    map_style="mapbox://styles/mapbox/light-v9"
)

st.subheader("World Map of Average AQI by Country")
st.pydeck_chart(deck)
st.write("""This interactive map showcases the AQI all around the world compared to one another, by selecting different regions, you can see how different the indices are and make conclusions based on latitude and longitude as to why certain areas may have similar AQI’s. 
    Or even the opposite, how different regions could have such drastically different AQIs.""" )

