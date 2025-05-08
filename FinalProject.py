"""
CS230 Final Project - Global AQI Explorer
Author: Diego Petricioli
Description:
    This Streamlit app visualizes air quality data from around the world using AQI scores.
    It includes data cleaning, filtering, grouping, and plotting using only class-approved tools.
"""

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

filename = "C:/Users/dpetr/Final Project (Python)/AQI.csv"
df = pd.read_csv(filename)

#GETS RID OF ROWS WITHOUT COUNTRY OR COORDINATES
df = df.loc[df['Country'].notna() & df['lat'].notna() & df['lng'].notna()]

##SIDEBAR
st.title("Global Air Quality Explorer")
st.sidebar.header("Filter Options")
category_options = sorted(df['AQI Category'].unique())
selected_categories = st.sidebar.multiselect("Select AQI Categories", category_options, default=category_options)
country_options = sorted(df['Country'].dropna().unique())
selected_country = st.sidebar.selectbox("Select a Country", ["All Countries"] + country_options)

##FILTERS
filtered_df = df[df['AQI Category'].isin(selected_categories)]
if selected_country != "All Countries":
    filtered_df = filtered_df[filtered_df['Country'] == selected_country]
st.write(f"### Showing {len(filtered_df)} records")
st.dataframe(filtered_df[['Country', 'City', 'AQI Value', 'AQI Category']])

##PIECHART
fig1, ax1 = plt.subplots()
filtered_df['AQI Category'].value_counts().plot.pie(autopct='%.1f%%', ax=ax1)
ax1.set_ylabel("")
ax1.set_title("AQI Category Distribution")
st.pyplot(fig1)

##BARCHART
worst = filtered_df.sort_values(by='AQI Value', ascending=False).head(10)
fig2, ax2 = plt.subplots()
ax2.bar(worst['City'], worst['AQI Value'], color='orange')
ax2.set_title("Top 10 Most Polluted Cities")
ax2.set_ylabel("AQI Value")
ax2.set_xlabel("City")
st.pyplot(fig2)

##AVERAGE
avg_by_country = filtered_df.groupby('Country')['AQI Value'].mean().sort_values(ascending=False)
st.write("### Average AQI by Country")
st.dataframe(avg_by_country.head(10))

##MAP
st.write("### AQI Map by Location")
st.map(filtered_df.rename(columns={"lat": "latitude", "lng": "longitude"})[["latitude", "longitude"]])

