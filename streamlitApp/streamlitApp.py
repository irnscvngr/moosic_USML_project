# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 09:18:36 2024

@author: Patrick
"""

# =============================================================================
# %% import modules
# =============================================================================
import streamlit as st
# ---
import numpy as np
import pandas as pd
# ---
import plotly.graph_objects as go


# =============================================================================
# PAGE TITLE AND IMAGE
# =============================================================================
about = '''
	Made by Patrick Hausmann.\n
 	2024\n
  	www.github.com/irnscvngr
   	'''
menu_items = dict(about = about)

st.set_page_config(page_title = 'Moosic Playlist Assistant',
		   page_icon = 'streamlitApp/favicon.png',
		   menu_items = menu_items,
		  )

st.image('streamlitApp/Moose_Logo.png')

# Draw a title and some text to the app:
'''
# PLAYLIST ASSISTANT

This assistant draws from our music database and provides you with
pre-sorted lists of songs. Pre-sorting is based on auditive features using ML and thereby prone to error.

Have a look at the visualization below to see how the song-clusters differ in auditive features and see how various songs compare.

*Use with caution for playlist generation.*
'''
st.divider()

# =============================================================================
# %% cluster overview
# =============================================================================
'''
### Cluster Overview
'''
# -----------------------------------------------------------------------------
# --- DISPLAY CLUSTERGENRES DATAFRAME

# --- IMPORT CLUSTERGENRES
df_clustergenres = pd.read_csv('streamlitApp/cluster_genres.csv')
df_clustergenres['main_genres'] = df_clustergenres['main_genres'].astype(str)

# --- DISPLAY DATAFRAME
st.dataframe(
    # pretty print columnnames
    (df_clustergenres
     .rename(columns={'cluster':'Cluster','main_genres':'Genres'})
     ),
    # Don't display dataframe-index
    hide_index = True,
    width=1000,
    height=300
    )

# -----------------------------------------------------------------------------
# --- MULTISELECT

# --- MAKE DF TO BE DISPLAYED IN MULTISELECT
df_clusterselect = (
    # join cluster-numbering and genres
    df_clustergenres['cluster'].astype(str) +
    ' - ' +
    df_clustergenres['main_genres']
    )

# --- FORMAT FUNCTION FOR MULTISELECT
def ffunc_cl(cl_select):
    return df_clusterselect[cl_select]

# --- INITIALIZE MULTISELECT SESSION STATE
if 'cl_select' not in st.session_state:
    # initialize session state for cold start
    st.session_state['cl_select'] = [3]

# --- MULTISELECT CLUSTERS
cl_select = st.multiselect(
    'Select clusters:',
    # iterables for multiselect
    list(df_clustergenres['cluster']),
    # format function to also display cluster-names instead of integers only
    format_func = ffunc_cl,
    key = 'cl_select'
    )

# Stop creating remaining app-parts in case no cluster is selected
if not cl_select:
    st.write('No cluster selected.')
    exit()

# --- GET SELECTED GENRE-LISTS
main_genres = (
    df_clustergenres
    .loc[df_clustergenres['cluster'].isin(cl_select),'main_genres']
    )

'''**Genres from selection:**'''

# --- ADD UNIQUE GENRES INFO
# Join pd.Series to single string with commas between genre-names
genre_select_str = (', '.join(pd.Series(
    # Sort genre-names
    sorted(
        # Use list-comprehension to go through list of genre-names
        [name.strip() for name in main_genres.str
         # Make list from genre-names by splitting at commas
         .split(',')
         # Extract list elements from dataframe-row and make individual rows
         # from them (e.g. 1 row with 3 genres to 3 rows with 1 genre each)
         .explode()]
        )
    )
    # Check for double-entries and only keep unique elements
    .unique()
    )
    )

# Display selected unique genres
st.write(genre_select_str)

st.divider()

# =============================================================================
# %% song list and spotify player
# =============================================================================
'''
### Song List
'''

# --- IMPORT SONG-LIST
df_songs = pd.read_csv('streamlitApp/spotify_5000_songs_clustered.csv')
df_songs[['song_name','artist','id','html']] = df_songs[['song_name','artist','id','html']].astype(str)

# --- MAKE TRIMMED SONGS-DF
df_songs_trimmed = (
    df_songs
    .copy()
    # Only take selected rows and specific columns
    .loc[df_songs['cluster'].isin(cl_select),['cluster','artist','song_name','artist_genre','id']]
    .sort_values(['cluster','artist'])
    .reset_index()
    )

# --- DISPLAY TOTAL NUMBER OF SONGS
f'''
{df_songs_trimmed.shape[0]} songs total in active clusters.
'''

# --- DISPLAY TRIMMED SONGS-DF
st.dataframe(
    (df_songs_trimmed
     .drop(columns=['index','id'])
     .rename(columns={'cluster':'Cluster',
                      'artist':'Artist',
                      'song_name':'Song',
                      'artist_genre':'Genre'
                      }
             )
    ),
    # hide_index = True,
    width=1000,
    height=300
    )

# -----------------------------------------------------------------------------
# --- SELECT SINGLE SONG

# --- MAKE DF TO DISPLAY FOR SELECTBOX
df_selectsongs = (
    df_songs_trimmed['song_name'] +
    ' - ' +
    df_songs_trimmed['artist'] +
    ' | ' +
    df_songs_trimmed['artist_genre']
    )

# --- INITIALIZE SELECTBOX SESSION STATE
if 'song_selectbox1' not in st.session_state:
    st.session_state['song_selectbox1'] = 0

# --- FORMAT FUNCTION FOR SELECTBOX
def ffunc(sl):
    select = df_selectsongs.iloc[sl]
    return select

sl = st.selectbox(
    'Select a song for playback:',
    options = df_selectsongs.index,
    format_func = ffunc,
    key = 'song_selectbox1'
    )

# -----------------------------------------------------------------------------
# --- SPOTIFY PLAYER

# Get song ID for current selection
song_id = df_songs_trimmed.loc[sl,'id'].strip()

# Make URL to call embedded spotify player
src = f"""
		https://open.spotify.com/embed/track/
		{song_id}
		?utm_source=generator
     	"""
# Add iframe component with spotify player
st.components.v1.iframe(src,height=80)

st.divider()

# =============================================================================
# %% song comparison
# =============================================================================
'''
### Song Comparison

Auditive features of selected songs juxtaposed.
'''
# -----------------------------------------------------------------------------
# --- SELECT SONG TO COMPARE
    
if 'song_selectbox2' not in st.session_state:
    st.session_state['song_selectbox2'] = 1

df_selectsongs2 = df_selectsongs[df_selectsongs.index!=sl]

sl2 = st.selectbox(
    'Select a song to compare auditive features:',
    options = df_selectsongs2.index,
    format_func = ffunc,
    key = 'song_selectbox2'
    )

def update_selection(step=1):
    # Advance session state by 1 increment
    ind = st.session_state['song_selectbox2'] + step
    # Check if index is sl (which is not chooseable, because it's
    # the reference song)
    if ind == sl:
        ind += step
    # Clamp index in the index range of selectsongs2
    ind = np.clip(ind,
                  df_selectsongs2.index.min(),
                  df_selectsongs2.index.max()
                  )
    # Update session state
    st.session_state['song_selectbox2'] = ind
    return ind

col1, colm, col2 = st.columns([1,2,1])
# --- ADVANCE SONG SELECTION BY ONE STEP
# (Needs to be lambda-function because of the way streamlit executes functions
# and session state-updates)
with col1:
	st.button('Previous Song',
            on_click = lambda: update_selection(-1),
            use_container_width=True)
with col2:
    st.button('Next Song',
            on_click = lambda: update_selection(1),
            use_container_width=True)


# --- RETRIEVE ORIGINAL INDICES FROM TRIMMED SONGS-DF
ind1 = df_songs_trimmed.loc[sl,'index']
ind2 = df_songs_trimmed.loc[sl2,'index']

# --- MAKE NEW DF WITH SONGS TO COMPARE
df_songs_compare = df_songs.loc[[ind1,ind2],:]

# --- ONLY KEEP 0...1 FEATURES FOR PLOTTING
df2 = df_songs_compare.copy().set_index('song_name')[
    ['speechiness',
     'acousticness',
     'instrumentalness',
     'liveness',
     'valence',
     'danceability',
     'energy'
     ]
    ]

# -----------------------------------------------------------------------------
# --- PLOT RADAR CHART

# Initialize trace objects list
trace_objects = []

# Adaptive alpha value for coloring, depening on number of plotted genres
alpha = 0.7
# Set colors for the individual genres (in accordance with final presentation colors)
colors = [f'rgba(255, 171, 64, {alpha})', f'rgba(66, 133, 244, {alpha})']

# --- GO THROUGH ALL GENRES AND ADD A PLOT
for c, genre in enumerate(df2.index):
    # Append plot object to list
    trace_objects.append(
        # Create scatterpolar plot
        go.Scatterpolar(
            # Get audio-feature values for radial information
            r = df2.loc[genre,:],
            # Get column-names for labeling
            theta = df2.columns,
            # Name of the current plot as it will appear in the legend
            name=genre,
            # Add fill-color to the shapes
            fill='toself',
            fillcolor=colors[c],
            # Set marker-color and fontsize
            marker=dict(color=colors[c],size=2),
            # Set linewidth of shapes
            line=dict(width=2)
        )
    )

# Add figure-element
fig = go.Figure()

# Add the scatterpolar-elements to the figure
fig.add_traces(trace_objects)

# --- ADJUST APPEARANCE
fig.update_layout(
    # Add plot-title
    # title_text = 'Main genres Pop & Death Metal compared by audio features',
    # Set plot-size
    # 'None' to make figure conform to site width
    width = None,
    # Font-settings
    font=dict(
        color='white',
        family='Roboto',
        size=12
    ),
    # Background/Grid-Settings
    polar=dict(
        # Set background color
        bgcolor='rgba(0,0,0,0)',
        # Everything concerning radial elements...
        radialaxis=dict(
            # Toggle visibility
            visible=True,
            # Set size (should match max. values from data), comparable to ylim
            range=[0, 1],
            # Set line widths
            linewidth=0.5,
            gridwidth=0.5,
            # Hide labels at 0°-line
            showticklabels=False
        ),
        # Everything concerning angular elements...
        angularaxis=dict(
            # Set line widths
            linewidth=3,
            gridwidth=1
        ),
    ),
    # Set legend position
    legend=dict(
        x = 0,  # Set the x coordinate of the legend
        y = 1.3   # Set the y coordinate of the legend
    ),
    # Toggle legend visibility
    showlegend=True,
)

# Set background to transparent for exporting
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

st.plotly_chart(fig)

# =============================================================================
# %% explain musical features
# =============================================================================
# --- MAKE DICTIONARY OF MUSICAL FEATURES
features = dict(
    acousticness = "Confidence whether the track is acoustic.",
    danceability = "Describes how suitable a track is for dancing.",
    energy = "Represents a perceptual measure of intensity and activity.",
    valence = "Describes the musical positiveness conveyed by a track.",
    instrumentalness = "Predicts whether a track contains no vocals.",
    liveness = "Detects the presence of an audience in the recording.",
    speechiness = "Speechiness detects the presence of spoken words in a track."
    )

# --- SHOW EXPLAINER IN AN EXPANDER
with st.expander('See musical features explained'):
    # Make Dataframe from dictionary and display
	st.dataframe(
        pd.DataFrame.from_dict(features,
                               # needed, because index is of type string
                               orient='index',
                               # to avoid column being just named "value"
                               columns=['Meaning']
                               ),
        width=1000
        )

# =============================================================================
# %% display dataframe for numerical comparison
# =============================================================================

st.dataframe((df_songs_compare
              .drop(columns=['html','cluster','id','artist_genre'])
              .set_index('song_name')
              .transpose()
              ),
             width=1000,
             height = 540
             )

st.divider()

coll,colm,colr = st.columns([1.2,1,1])
with colm:
   st.image('streamlitApp/Moose_Logo_small.png')

# Don't add linebreak after \n\n -> Link will not be displayed properly
md = """
 	<center>
	<b>Made by:</b>\n\n[Patrick Hausmann](www.github.com/irnscvngr)
    """
st.markdown(md, unsafe_allow_html=True)

