#!/usr/bin/env python
# coding: utf-8
# %% [markdown]
# This script gets pd.Series of spotify playlists indexed by ID and such that the value is the name of the list, finds all songs inside all playlists

# %%
import pandas as pd
import numpy as np


# %%
import re
with open('cred.txt','r') as file:
    cred = [l.replace("\n", "") for l in file.readlines()]


# %%
cred

# %%
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
cred = SpotifyClientCredentials(client_id=cred[0], client_secret=cred[1])
sp = spotipy.Spotify(client_credentials_manager=cred)


# %%

# %%
all_lists = pd.read_pickle('data/final_spotify_playlists.pkl')


# %%
filtered = all_lists.copy()


# %%
filtered = filtered[-filtered.apply(lambda x: 'this is' in x.lower())]


# %%
filtered = filtered[-filtered.apply(lambda x: 'composer' in x.lower())]


# %%
filtered = filtered[-filtered.apply(lambda x: 'written by' in x.lower())]


# %%
# try some new music!!
# filtered[filtered.apply(lambda x: 'instrumental' in x.lower())]
# filtered[filtered.apply(lambda x: 'mute' in x.lower())]


# %%
artists = pd.Series()
names = pd.Series()
popularity = pd.Series()
playlist = pd.Series()


# %% [markdown]
# this takes a few hours

# %%
starting_value = 0

# %%
for index, id_playlist in enumerate(filtered.index[starting_value:]):
    print(len(filtered.index)-starting_value-index)
    tracks_obj = None
    i=0
    while tracks_obj==None or tracks_obj['next']:
        try:
            tracks_obj = sp.playlist_tracks(id_playlist, limit=100, offset=i*100)        
            for t in tracks_obj['items']:
                if 'track' in t.keys() and t['track'] and 'id' in t['track'].keys():
                    id_song = t['track']['id']
                    try:
                        playlist[id_song].append(id_playlist)
                    except:
                        playlist[id_song] = [id_playlist]
                    artists[id_song]=list(map(lambda a: (a['name'],a['id']),t['track']['artists']))
                    popularity[id_song]=t['track']['popularity']
                    names[id_song]=t['track']['name']
            i+=1
        except:
            print('NOT DONE {}'.format(id_playlist))
            tracks_obj = {}
            tracks_obj['next'] = False


# %%

# %%
songs = pd.DataFrame({'playlists':playlist,'artists':artists, 'popularity':popularity, 'name':names}, index=playlist.index)


# %%
songs.index.name='id'


# %%
songs.to_pickle('songs.pkl')


# %%
songs.head()


# %%
# songs['playlists'].apply(lambda x: len(x)).mean()


# %%




