import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely import wkt
import sys
import heapq
from collections import deque
import time

streets = pd.read_csv('calles_de_medellin_con_acoso.csv', sep =';')
polygon = pd.read_csv('poligono_de_medellin.csv', sep =';')

mean_Risk = streets['harassmentRisk'].mean()
map_Med = dict()

streets['harassmentRisk']=streets['harassmentRisk'].fillna(mean_Risk)


def weight(a,b):
    return a*b
def graph(map_Med):
    for i in streets.index:
        if streets['origin'][i] in map_Med:
            map_Med.get(streets['origin'][i]).append((streets['destination'][i],(streets['harassmentRisk'][i],streets['length'][i],weight(streets['length'][i],streets['harassmentRisk'][i])),streets['geometry'][i],(streets['length'][i],streets['harassmentRisk'][i])))
        else:
            map_Med[streets['origin'][i]]= [(streets['destination'][i],(streets['harassmentRisk'][i],streets['length'][i],weight(streets['length'][i],streets['harassmentRisk'][i])),streets['geometry'][i],(streets['length'][i],streets['harassmentRisk'][i]))]
        if streets['oneway'][i]==False:
            if streets['destination'][i] in map_Med:
                map_Med.get(streets['destination'][i]).append((streets['origin'][i],(streets['harassmentRisk'][i],streets['length'][i],weight(streets['length'][i],streets['harassmentRisk'][i])),streets['geometry'][i],(streets['length'][i],streets['harassmentRisk'][i])))
            else:
                map_Med[streets['destination'][i]]= [(streets['origin'][i],(streets['harassmentRisk'][i],streets['length'][i],weight(streets['length'][i],streets['harassmentRisk'][i])),streets['geometry'][i],(streets['length'][i],streets['harassmentRisk'][i]))]
    return map_Med


def dijkstra(graph,start,finish):
    distances = {vertex: [float('inf'),list()] for vertex in graph}
    distances[start][0]= 0
    distances2 ={vertex: [float('inf'),list()] for vertex in graph}
    distances3 = {vertex: [float('inf'),list()] for vertex in graph}
    pq = [(0,start)]
    paths= deque()
    node_data=dict()
    inicio1= time.time()
    while len(pq)>0 :
        try:
            current_distance, current_vertex = heapq.heappop(pq)
            if current_distance > distances[current_vertex][0]:
                continue
        
            for neightbor, weight,xd,x2 in graph[current_vertex]: 
                weight1= weight[0]
                distance1 = current_distance+weight1
                
                if distance1<distances[neightbor][0]:
                    distances[neightbor][0]=distance1
                    distances[neightbor][1].append(current_vertex)
                    heapq.heappush(pq,(distance1,neightbor)) 
                    if neightbor not in  node_data:
                        node_data[neightbor]=[distance1,current_vertex]
                    else:
                        node_data.get(neightbor)[1]= current_vertex
                        node_data.get(neightbor)[0]= distance1
        except KeyError:
            continue
        if current_vertex== finish:
            continue
    current_vertex= finish
    path1= deque()
    path1.appendleft(current_vertex)

    while current_vertex!= start:
        path1.appendleft(node_data.get(current_vertex)[1])
        current_vertex=node_data.get(current_vertex)[1]
    paths.append(path1)
    node_data.clear()
    final1= time.time()
    print("time 1="+str(final1-inicio1))
    pq2 = [(0,start)]
    inicio2=time.time()
    while len(pq2)>0 :
        try:
            current_distance, current_vertex = heapq.heappop(pq2)
            if current_distance > distances2[current_vertex][0]:
                continue
        
            for neightbor, weight,xd,x2 in graph[current_vertex]: 
                weight2= weight[1]
                distance2 = current_distance+weight2
                
                if distance2<distances2[neightbor][0]:
                    distances2[neightbor][0]=distance2
                    distances2[neightbor][1].append(current_vertex)
                    heapq.heappush(pq2,(distance2,neightbor)) 
                    if neightbor not in  node_data:
                        node_data[neightbor]=[distance2,current_vertex]
                    else:
                        node_data.get(neightbor)[1]= current_vertex
                        node_data.get(neightbor)[0]= distance2
        except KeyError:
            continue
        if current_vertex== finish:
            continue
        
    path2= deque()
    current_vertex= finish
    while current_vertex!= start:
        path2.appendleft(node_data.get(current_vertex)[1])
        current_vertex=node_data.get(current_vertex)[1]
    paths.append(path2)
    
    node_data.clear()
    final2= time.time()
    print("time2="+ str(final2-inicio2))
    pq3 = [(0,start)]
    inicio3= time.time()
    while len(pq3)>0 :
        try:
            current_distance, current_vertex = heapq.heappop(pq3)
            if current_distance > distances3[current_vertex][0]:
                continue
        
            for neightbor, weight,xd,x2 in graph[current_vertex]: 
                weight3= weight[2]
                distance3 = current_distance+weight3
                
                if distance3<distances3[neightbor][0]:
                    distances3[neightbor][0]=distance3
                    distances3[neightbor][1].append(current_vertex)
                    heapq.heappush(pq3,(distance3,neightbor)) 
                    if neightbor not in  node_data:
                        node_data[neightbor]=[distance3,current_vertex]
                    else:
                        node_data.get(neightbor)[1]= current_vertex
                        node_data.get(neightbor)[0]= distance3
        except KeyError:
            continue
        if current_vertex== finish:
            continue
    path3= deque()
    current_vertex= finish
    while current_vertex!= start:
        path3.appendleft(node_data.get(current_vertex)[1])
        current_vertex=node_data.get(current_vertex)[1]
    paths.append(path3)
    final3= time.time()
    print("tiempo3="+str(final3-inicio3))
    return paths
        
paths=dijkstra(graph(map_Med),'(-75.5778046, 6.2029412)','(-75.5762232, 6.266327)')

path1= paths[0]
path2= paths[1]
path3= paths[2]
geometry_path_list=[]
distance_1=0
distance_2=0
distance_3=0
risk_1=0
risk_2=0
risk_3=0
j=1
for i in path1:
    if i!=path1[-1]:
        for destination in map_Med.get(i):
            if destination[0]==path1[j]:
                geometry_path_list.append(destination[2])
                distance_1= distance_1+ destination[3][0]
                risk_1=risk_1+destination[3][1]
        j=j+1
risk_1= risk_1/j
geometry_path_list2=[]
j=1
for i in path2:
    if i!=path2[-1]:
        for destination in map_Med.get(i):
            if destination[0]==path2[j]:
                geometry_path_list2.append(destination[2])
                distance_2= distance_2+ destination[3][0]
                riesgo2=riesgo2+destination[3][1]
        j=j+1
riesgo2= riesgo2/j
geometry_path_list3=[]
j=1
for i in path3:
    if i!=path3[-1]:
        for destination in map_Med.get(i):
            if destination[0]==path3[j]:
                geometry_path_list3.append(destination[2])
                distance_3= distance_3+ destination[3][0]
                riesgo3=riesgo3+destination[3][1]
        j=j+1
riesgo3= riesgo3/j
print("La distancia del primer camino: "+str(distance_1))     
print("La distancia del segundo camino: "+str(distance_2))
print("La distancia del tercer camino: "+str(distance_3)) 
print("El riesgo del primer camino: "+str(riesgo1))     
print("El riesgo del segundo camino: "+str(riesgo2))
print("El riesgo del tercer camino: "+str(riesgo3)) 
geometry_path3= pd.DataFrame(geometry_path_list3)
geometry_path3[0] = geometry_path3[0].apply(wkt.loads)
geometry_path3 = gpd.GeoDataFrame(geometry_path3)
geometry_path3 = geometry_path3.set_geometry(0)  

geometry_path2= pd.DataFrame(geometry_path_list2)
geometry_path2[0] = geometry_path2[0].apply(wkt.loads)
geometry_path2 = gpd.GeoDataFrame(geometry_path2)
geometry_path2 = geometry_path2.set_geometry(0)        
        
geometry_path= pd.DataFrame(geometry_path_list)
geometry_path[0] = geometry_path[0].apply(wkt.loads)
geometry_path = gpd.GeoDataFrame(geometry_path)
geometry_path = geometry_path.set_geometry(0)

polygon = pd.read_csv('poligono_de_medellin.csv',sep=';')
polygon['geometry'] = polygon['geometry'].apply(wkt.loads)
polygon = gpd.GeoDataFrame(polygon)


fig, ax = plt.subplots(figsize=(12,8))
polygon.plot(ax=ax, facecolor='grey')
streets['geometry'] = streets['geometry'].apply(wkt.loads)
streets = gpd.GeoDataFrame(streets)
streets.plot(ax=ax, linewidth=1, edgecolor='dimgray')
geometry_path.plot(ax=ax, linewidth=1, edgecolor='blue')
geometry_path2.plot(ax=ax, linewidth=1, edgecolor='red')
geometry_path3.plot(ax=ax, linewidth=1, edgecolor='pink')

plt.tight_layout()
