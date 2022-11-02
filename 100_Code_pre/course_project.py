import numpy as np
import pandas as pd
import folium
import math as m
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

    return m.sqrt(pow(node1_Longitude-node1_Latitude,2) + pow(node2_Longitude-node2_Latitude,2))

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
get_Dict()
end = time.time()
print (end - start)