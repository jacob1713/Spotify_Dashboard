import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import millify as mf


# Example
# st.title("🎈 My new ")
# st.write(
#     "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
# )

# Load Data
data = pd.read_csv('/workspaces/top_spotify_songs/data/Spotify Most Streamed Songs.csv')

# Clean and adjust data
# Manually change artist(s)_name for index 742 to Matuï¿½ï¿½, Wiu, Teto
data.loc[742, 'artist(s)_name'] = 'Matuï¿½ï¿½, Wiu, Teto'

# Sort by number of streams in descending order
data = data.sort_values(by='streams', ascending=False)

# Manually drop index 574
data = data.drop(574)

# Manually change released_year, released_month and released_day for index 80
data.loc[80, 'released_year'] = 2014
data.loc[80, 'released_month'] = 9
data.loc[80, 'released_day'] = 8

# Convert streams to integer
data['streams'] = data['streams'].astype(int)

# Remove all commas from deezer_playlists
data['in_deezer_playlists'] = data['in_deezer_playlists'].str.replace(',', '')

# Convert in deezer playlists to integer
data['in_deezer_playlists'] = data['in_deezer_playlists'].astype(int)

# Remove all commas from in_shazam_charts
data['in_shazam_charts'] = data['in_shazam_charts'].str.replace(',', '')

# Convert NaN values in in_shazam_charts to 0
data['in_shazam_charts'] = data['in_shazam_charts'].fillna(0)

# Convert in shazam charts to integer
data['in_shazam_charts'] = data['in_shazam_charts'].astype(int)

# Sort by number of streams in descending order
data = data.sort_values(by='streams', ascending=False)

# Reset index
data = data.reset_index(drop=True)

# Adjust index to start at 1
data.index = data.index + 1

# Change name of index column to rank
data = data.rename(columns={'index': 'rank'})

# Create release date column that combines released_day, released_month, and released_year
data['release_date'] = pd.to_datetime(data['released_day'].astype(str) + '-' + data['released_month'].astype(str) + '-' + data['released_year'].astype(str), format='%d-%m-%Y')

# Find row where artist(s)_name has the most number of artists
data['artist_count'] = data['artist(s)_name'].str.count(',') + 1

# Separate artists into individual columns, up to 8 artists
data[['artist1', 'artist2', 'artist3', 'artist4', 'artist5', 'artist6', 'artist7', 'artist8']] = data['artist(s)_name'].str.split(',', expand=True)

# Create list to store all artists
unique_artists = []

# Create string with all unique artists
unique_artists = pd.concat([data['artist1'], data['artist2'], data['artist3'], data['artist4'], data['artist5'], data['artist6'], data['artist7'], data['artist8']]).dropna().unique()

# Sort unique artists alphabetically
unique_artists = np.sort(unique_artists)

# Add a select all option at the beginning of the list
unique_artists = np.insert(unique_artists, 0, 'Select All')

# Add logo to sidebar
st.sidebar.image('/workspaces/top_spotify_songs/data/Spotify_Primary_Logo_RGB_Green.png', width=100)

# Add sidebar with app title
st.sidebar.title('Spotify Most Streamed Songs')

# Add sidebar with app description
st.sidebar.write('This app displays data and visuals for the most streamed songs on Spotify.')

# Add range slider to sidebar
st.sidebar.write('Select a range of dates to display the most streamed songs.')
date_range = st.sidebar.slider('Select Date Range', min_value= data['released_year'].min(), max_value=data['released_year'].max(), value=(1930, 2023))

# Function to handle "Select All" behavior
def handle_select_all_artists(selected_artists):
    if 'Select All' in selected_artists:
        return unique_artists[1:]  # Return all artists excluding 'Select All'
    else:
        return selected_artists

# Add multi-select box to sidebar for selecting artists from unique_artists list
st.sidebar.write('Select artists to display their most streamed songs.')

# Initialize with Select All option selected
artists = st.sidebar.multiselect('Select Artists', unique_artists, default='Select All')

# Handle "Select All" functionality
artists = handle_select_all_artists(artists)

# Filter data based on selected artists and date range
filtered_data = data[(data['released_year'] >= date_range[0]) & (data['released_year'] <= date_range[1]) & (data['artist1'].isin(artists) | data['artist2'].isin(artists) | data['artist3'].isin(artists) | data['artist4'].isin(artists) | data['artist5'].isin(artists) | data['artist6'].isin(artists) | data['artist7'].isin(artists) | data['artist8'].isin(artists))]

# Filter the data to include only the specified columns
filtered_data = filtered_data[['track_name', 'artist(s)_name', 'streams', 'release_date', 'in_spotify_playlists']]

# Create top section with 4 columns
col1, col2, col3, col4 = st.columns(4)

# Add total songs metric
col1.metric('Total Songs', filtered_data.shape[0])

# Add total streams metric
col2.metric('Total Streams', mf.millify(filtered_data['streams'].sum(), precision=2))

# Add total artists metric
col3.metric('Total Artists', len(artists))

# Add total playlists metric
col4.metric('Total Playlists', filtered_data['in_spotify_playlists'].sum())

# Create columns on the main page
col1, col2 = st.columns([1, 2])

# Add logo to the first column
col1.title('Spotify Most Streamed Songs')

# Add title to the second column
col2.title('Spotify Most Streamed Songs')

# Add  vertical borders to the columns
col1.write('____')
col2.write('______')

# Add example body text to the first column
col1.write('This app displays data and visuals for the most streamed songs on Spotify.')
with col1:
    st.dataframe(filtered_data)