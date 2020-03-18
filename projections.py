import networkx as nx

# # WEEK 0

# Getting the data, it consisted in three steps:
# 1. Getting the playlists that spotify gives us directly from user Spotify and those that are in categories (are all created by spotify)
# 2. Creating a vocabulary from the names of the playlists in 1. and performing playlists search queries from the bag of words (the first results are playlists from spotify)
# 3. Iterating 2. (creating new bag of words of the new playlists) until we had too many playlists
#
# This can be found in `playlists_features.py`

# # WEEK 1

# We have taken the Spotify playlists created by Spotify and build a huge bipartite network of artists and playlist, where artist and playlist are connected if there is a song of that artist in the playlist. We kept the largest connected component.

from networkx.algorithms import bipartite

spotify = nx.read_gpickle('data/network_bipartite.gpkl')



# +
from networkx.algorithms import bipartite

spotify = nx.read_gpickle('data/network_bipartite.gpkl')
spotify_big_connected = spotify.subgraph(next(nx.connected_components(spotify)))
playlists, artists = bipartite.sets(spotify_big_connected)
artists_projection = bipartite.weighted_projected_graph(spotify_big_connected, artists)
artists_projection = nx.read_gpickle('./data/artists_projection.gpkl')

playlists_projection = bipartite.weighted_projected_graph(spotify_big_connected, playlists)
nx.write_gpickle(playlists_projection, 'data/playlists_projection.gpkl')
nx.write_gpickle(artists_projection, 'data/artists_projection.gpkl')

import pandas as pd
playlists = pd.read_pickle('data/final_spotify_playlists.pkl')

def get_nearest(projection, id_playlist):
    neighbors = playlists_projection.neighbors(id_playlist)
    tal = [(projection[id_playlist][id_n]['weight'],id_n,playlists.loc[id_n]) for id_n in neighbors]
    return sorted(tal, reverse=True)

get_nearest(playlists_projection, '37i9dQZF1DXbHcQpOiXk1D')


