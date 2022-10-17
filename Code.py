import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely import wkt
import sys
from heapq import heapify,heappush,heappop

streets = pd.read_csv('calles_de_medellin_con_acoso.csv', sep =';')
polygon = pd.read_csv('poligono_de_medellin.csv', sep =';')

mean_Risk = streets['harassmentRisk'].mean()
map_Med = dict()

streets['harassmentRisk']=streets['harassmentRisk'].fillna(mean_Risk)

def weight(a,b):
    return a*b

for i in streets.index:
    if streets['origin'][i] in map_Med:
        map_Med.get(streets['origin'][i])[streets['destination'][i]]=(weight(streets['length'][i],streets['harassmentRisk'][i]),streets['length'][i],streets['oneway'][i],streets['harassmentRisk'][i],streets['geometry'][i])
    else:
        map_Med[streets['origin'][i]]= dict({streets['destination'][i]:(weight(streets['length'][i],streets['harassmentRisk'][i]),streets['length'][i],streets['oneway'][i],streets['harassmentRisk'][i],streets['geometry'][i])})
    if streets['oneway'][i]==False:
        if streets['destination'][i] in map_Med:
            map_Med.get(streets['destination'][i])[streets['origin'][i]]=(weight(streets['length'][i],streets['harassmentRisk'][i]),streets['length'][i],streets['oneway'][i],streets['harassmentRisk'][i],streets['geometry'][i])
        else:
            map_Med[streets['destination'][i]]= dict({streets['origin'][i]:(weight(streets['length'][i],streets['harassmentRisk'][i]),streets['length'][i],streets['oneway'][i],streets['harassmentRisk'][i],streets['geometry'][i])})
            

def dijsktra(graph,origin,destination):
    inf = sys.maxsize
    node_data = dict()
    
    for clave in graph:
        node_data[clave]= dict({'cost':inf,'pred':[]})
    node_data[origin]['cost']=0
    visited=[]
    temp = origin
                    
    for i in range(len(graph)-1):
        visited_all_nodes=0
        if temp not in visited:
            if len(graph[temp])==1 and ((next(iter(graph[temp]))) in visited) and (len(all_pred)!=0): 
                if temp in all_pred:
                    all_pred.remove(temp)
                temp1=all_pred.pop()
                visited.append(temp)
                visited.remove(temp1)
                temp= temp1
            visited.append(temp)
            min_heap=[]
            for j in graph[temp]:
                if j in visited:
                    visited_all_nodes=visited_all_nodes+1
                else:
                    cost = node_data[temp]['cost']+graph[temp][j][0]
                    if cost<node_data[j]['cost']:
                        node_data[j]['cost']=cost
                        node_data[j]['pred']=node_data[temp]['pred']+[temp]
                        all_pred=node_data[j]['pred']
                    heappush(min_heap,(node_data[j]['cost'],j))

        if visited_all_nodes==len(graph[temp]) and( len(all_pred)!=0):
            if temp in all_pred:
                all_pred.remove(temp)
            temp1=all_pred.pop()
            visited.append(temp)
            visited.remove(temp1)
            temp= temp1
            min_heap.clear()  
            
        heapify(min_heap)
        if len(min_heap)!=0:
            temp=min_heap[0][1]
        if temp==destination:
            break
            
    print("shortest distance: "+str(node_data[destination]['cost']))
    print("shortest path: "+str(all_pred+[destination]))
    return all_pred+[destination]

path=dijsktra(map_Med,'(-75.7161351, 6.3424055)','(-75.7025278, 6.3425976)')
geometry_path_list=[]
j=1
for i in path:
    if i!=path[-1]:
        geometry_path_list.append([map_Med[i][str(ruta[j])][4]])
        j=j+1
geometry_path= pd.DataFrame(geometry_path_list)
geometry_path[0] = geometry_path[0].apply(wkt.loads)
geometry_path = gpd.GeoDataFrame(geometry_path)
geometry_path = geometry_path.set_geometry(0)
polygon = pd.read_csv('poligono_de_medellin.csv',sep=';')
polygon['geometry'] = polygon['geometry'].apply(wkt.loads)
polygon = gpd.GeoDataFrame(polygon)
fig, ax = plt.subplots(figsize=(12,8))
polygon.plot(ax=ax, facecolor='grey')
geometry_path.plot(ax=ax, linewidth=1, edgecolor='blue')
plt.tight_layout()
