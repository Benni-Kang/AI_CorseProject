import numpy as np
import pandas as pd
import folium
import math 
import os
import time

start = time.time()
path = os.getcwd()
df1 = pd.read_csv(path+".\\CaliforniaRoadNetwork_Edges.csv")
df2 = pd.read_csv(path+".\\CaliforniaRoadNetwork_Nodes.csv")

def Draw_map():
    m = folium.Map(
        location=[41.974556, -121.904167],
        zoom_start=7.5
        
    )
    for i in range(len(df2)):
            m.add_child(
            folium.CircleMarker(
                [df2["Latitude"][i],df2["Longitude"][i]],
                radius=2, # define how big you want the circle markers to be
                color='yellow',
                fill=True,
                fill_color='red',
                fill_opacity=1.5
        )
        )
    m.add_child(folium.LatLngPopup())
    m.save('Position Visualization.html')

def get_EuclideanDistance(node1,node2): 
    node1_Longitude = float(df2.loc[df2["NodeID"]==node1, :]["Longitude"])
    node1_Latitude = float(df2.loc[df2["NodeID"]==node1, :]["Latitude"])
   
    node2_Longitude = float(df2.loc[df2["NodeID"]==node2, :]["Longitude"])
    node2_Latitude = float(df2.loc[df2["NodeID"]==node2, :]["Latitude"])

    return math.sqrt(pow(node1_Longitude-node2_Longitude,2) + pow(node1_Latitude-node2_Latitude,2))

def get_Dict():
    graph_search = {}
    ##进入循环
    for i in range(len(df2)):
        next_node = []
        this_node = int(df2.loc[i,["NodeID"]])
        endnode = df1.loc[df1["StartNodeID"]==this_node, :]["EndNodeID"]
        for e in endnode:
            #groupby 找到所有的node 然后遍历每个node
            if e not in next_node:
                child_node = (e,get_EuclideanDistance(this_node,e))
                next_node.append(child_node)
        graph_search[this_node] = next_node
    return graph_search



def bfs(graph_to_search, initial_state, goal_state, verbose=False):
    # this is a list of a list because we need to eventually return
    # the entire PATH from the initial state to the goal state. So,
    # each element in this list represents a path from the the initial
    # state to one frontier node. We use the first element in each path
    # to represent the cost.
    frontiers = [[0, initial_state]]  # the frontier list only has the initial state, with a cost of 0.
    visited = []

    while len(frontiers) > 0:   # use while loop to iteratively perform search
        if verbose:  # print out detailed information in each iteration
            print('Frontiers (paths):')
            for x in frontiers:
                print('  -', x)
            print('Visited:', visited)
            print('\n')
        
        path = frontiers.pop(0)  # Get the first element in the list
        node = path[-1]  # Get the last node in this path
        
        if node in visited:  # check if we have expanded this node, if yes then skip this
            continue
            
        actions = graph_to_search[node] # get the possible actions
        for next_node, next_cost in actions:
            new_path = path.copy()
            new_path.append(next_node)
            new_path[0] = new_path[0] + next_cost
            
            if next_node in visited or new_path in frontiers:
                continue  # skip this node if it is already in the frontiers or the visited list.
            
            # check if we reached the goal state or not
            if next_node == goal_state:
                goal_path = new_path[1:]
                goal_cost = new_path[0]
                return goal_path, goal_cost  # if yes, we can return this path and its cost
            else:
                frontiers.append(new_path)  # add to the frontiers
        
        # after exploring all actions, we add this node to the visited list
        visited.append(node)

    return None
graph_search = get_Dict()
print(bfs(graph_search, 0, 1894, verbose=False))
print(bfs(graph_search, 4, 3115, verbose=False))
print(bfs(graph_search, 18, 9186, verbose=False))
print(bfs(graph_search, 25, 15061, verbose=False))
print(bfs(graph_search, 33, 21040, verbose=False))

