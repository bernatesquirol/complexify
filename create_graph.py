import pandas as pd
import numpy as np

songs = pd.read_pickle('data/songs.pkl')

songs['artist']=songs['artists'].apply(lambda x: x[0][1])

# +
# songs[songs['name'].apply(lambda x: 'where is the love' in x.lower())]
# -

# # Creating the graph

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


spotify.remove_nodes_from(list(nx.isolates(spotify)))

# +
# nx.readwrite.write_gpickle(spotify, 'data/network_bipartite.gpkl')
# -

# # Adding features to the graph

# +
# import pandas as pd
# import numpy as np
# import networkx as nx

# spotify = nx.readwrite.read_gpickle('data/network_bipartite.gpkl')


# +
# artists = dict(np.vstack(songs.artists.values))
# artists = pd.Series({v: k for k, v in artists.items()})

# +
# dict_labels = {}
# for n, d in spotify.nodes(data=True):
#     print(n)
#     if d['bipartite']==0:
#         dict_labels[n] = playlists[n]
#     else:
#         dict_labels[n] = artists[n]


# +
# nx.get_node_attributes(spotify, '37i9dQZF1DWT8aqnwgRt92')
# -

# # Proning the graph

# +
# spotify = nx.read_gpickle('data/network_bipartite.gpkl')
# -

def prune(spotify, playlists):
    spotify_small = spotify.copy()
    playlists_articulation = [i for i in nx.articulation_points(spotify) if i in playlists.index]
    spotify_small.remove_nodes_from(playlists_articulation)
    stay_nodes = list(nx.connected_components(spotify_small))[np.argmax([len(i) for i in nx.connected_components(spotify_small)])]
    return spotify_small.subgraph(stay_nodes)

# +
# G = prone(spotify, playlists)
