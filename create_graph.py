import pandas as pd
import numpy as np

songs = pd.read_pickle('data/songs.pkl')

songs['artist']=songs['artists'].apply(lambda x: x[0][1])

# +
# songs[songs['name'].apply(lambda x: 'where is the love' in x.lower())]
# -

len(songs['artist'].unique())

import networkx as nx
from networkx.algorithms import bipartite

spotify = nx.Graph()

playlists = pd.read_pickle('data/final_spotify_playlists.pkl')

spotify = nx.Graph()

len(playlists.index)

spotify.add_nodes_from(playlists.index, bipartite=0)

spotify.add_nodes_from(songs['artist'].unique(), bipartite=1)

for artist, group in songs[['artist','playlists']].groupby('artist'):
    for playlists in group['playlists'].values:
        for playlist in playlists:
            spotify.add_edge(artist, playlist)

artists_playlist = pd.Series(dict_artists)

top_nodes = {n for n, d in spotify.nodes(data=True) if d['bipartite']==0}
bottom_nodes = set(spotify) - top_nodes

len(top_nodes)

spotify

spotify.remove_nodes_from(list(nx.isolates(spotify)))

nx.readwrite.write_gpickle(spotify, 'data/network_bipartite.gpkl')


