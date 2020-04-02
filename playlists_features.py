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
dict_cat = {}
# for country in 'AD AE AR AT AU BE BG BH BO BR CA CH CL CO CR CY CZ DE DK DO DZ EC EE EG ES FI FR GB GR GT HK HN HU ID IE IL IN IS IT JO KW LB LI LT LU LV MA MC MT MX MY NI NL NO NZ OM PA PE PH PL PS PT PY QA RO SA SE SG SK SV TH TN TR TW US UY VN ZA'.split(' '):

for cat in sp.categories(limit=50)['categories']['items']:
    try:
        playlists = sp.category_playlists(cat['id'], limit=50)['playlists']['items']
        for p in playlists:
            dict_cat[p['id']] = cat['id']
    except:
        pass

# %%
# pd.Series(dict_cat).to_csv('dict_list.csv')

# %%
dict_cat = {}
for country in 'AD AE AR AT AU BE BG BH BO BR CA CH CL CO CR CY CZ DE DK DO DZ EC EE EG ES FI FR GB GR GT HK HN HU ID IE IL IN IS IT JO KW LB LI LT LU LV MA MC MT MX MY NI NL NO NZ OM PA PE PH PL PS PT PY QA RO SA SE SG SK SV TH TN TR TW US UY VN ZA'.split(' '):
    for cat in sp.categories(limit=50)['categories']['items']:
        next_call = True
        index = 0
        while next_call:
            try:
                playlists = sp.category_playlists(cat['id'], country=country, limit=50, offset=index)['playlists']
                for cat in playlists['items']:
                    dict_cat[p['id']]=[cat['id']]
                next_call = playlists['next']
                index+=50
            except:
                pass

# %%
countries = 'AD AE AR AT AU BE BG BH BO BR CA CH CL CO CR CY CZ DE DK DO DZ EC EE EG ES FI FR GB GR GT HK HN HU ID IE IL IN IS IT JO KW LB LI LT LU LV MA MC MT MX MY NI NL NO NZ OM PA PE PH PL PS PT PY QA RO SA SE SG SK SV TH TN TR TW US UY VN ZA'.split(' ')

# %%
sp.category_playlists('chill', limit=50, country='GB')['playlists']['next']

# %%
sp.category_playlists('toplists', limit=50)

# %%
dict_cat

# %%
pl = {cat['id']: sp.category_playlists(cat['id'], limit=50) for cat in sp.categories(limit=50)['categories']['items']}

# %%
pl = { k:[[p['id'],p['name']]for p in v['playlists']['items']] for k, v in pl.items() }

# %%
del pl['toplists']

# %%
for v in pl.values():
    print(v)
    break

# %%
import itertools
playlists = list(itertools.chain(*pl.values()))

# %%
ids = [p[0] for p in playlists if len(p)>0]
names = [p[1] for p in playlists if len(p)>0]

# %%
# all_lists = pd.read_pickle('data/final_spotify_playlists.pkl')


# %%
all_lists = pd.Series(names, index=ids)

# %%
filtered = all_lists.copy()


# %%
def filter_name(x):
    return 'this is' in x.lower() or 'composer' in x.lower() or 'written by' in x.lower()


# %%
def filter_2(x):
    return 'españ' in x.lower() or 'Hot Hits' in x or 'today' in x.lower() or 'podcast' in x.lower() or 'book' in x.lower() or 'top' in x.lower() or 'new music' in x.lower() or 'made in' in x.lower() or '20' in x.lower() or 'greatest' in x.lower() or 'bpm' in x.lower() or 'the classical takeover' in x.lower() or 'spotify picks' in x.lower()


# %%
filtered = filtered[-filtered.apply(filter_name)]


# %%
filtered = filtered[-filtered.apply(filter_2)]


# %%
filtered.to_pickle('filtered_small.pkl')

# %%
# try some new music!!
# filtered[filtered.apply(lambda x: 'instrumental' in x.lower())]
# filtered[filtered.apply(lambda x: 'mute' in x.lower())]


# %%
voc = list(itertools.chain(*[x.split(' ') for x in filtered.values]))

# %%
playlists_added = {}
for word in voc:
    try:
        search = sp.search(q=word, type='playlist', limit=50)
        for p in search['playlists']['items']:
            new_p = {p['id']:p['name'] for p in search['playlists']['items'] if p['owner']['id']=='spotify' and not filter_name(p['name'])}
            playlists_added = {**playlists_added, **new_p}
    except:
        pass

# %%
len(playlists_added)

# %%
playlists_new = pd.Series(playlists_added)

# %%
playlists_new = playlists_new[~playlists_new.index.isin(all_lists.index)]

# %%
final_playlists = pd.concat([filtered,playlists_new])

# %%
final_playlists = final_playlists[~final_playlists.apply(filter_2)]

# %%
final_playlists.to_pickle('filtered_bigger.pkl')

# %%
artists = pd.Series()
names = pd.Series()
popularity = pd.Series()
playlist = pd.Series()


# %% [markdown]
# this takes a few hours

# %%
import tqdm

# %%
starting_value = 0

# %%
for index, id_playlist in enumerate(filtered.index):
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
# filtered[filtered.apply(lambda x: 'work' in x.lower())].head(50)

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




