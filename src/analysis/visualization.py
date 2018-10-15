import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from src.analysis.data_into_graph import Graph

graph = Graph()
graph.construct_graph()

chosen_range = graph.actors[:1]
actors = []
movies = []
for actor_obj in chosen_range:
    actor_mov = actor_obj.movie_name[:80]
    for i in range(len(actor_mov)):
        actors.append(actor_obj.name + " : " + str(actor_obj.age))
    for m in actor_mov:
        tag = m
        if m in graph.helper_set:
            m_obj = graph.helper_set[m]
            tag = tag + " : " + str(m_obj.gross)
        movies.append(tag)



# Build a dataframe with actor-movie connections
df = pd.DataFrame({'from': actors, 'to': movies})
df

# Build your graph
G = nx.from_pandas_edgelist(df, 'from', 'to')

# Plot it
nx.draw(G, with_labels=True, node_color="skyblue")
plt.show()

