import pandas as pd
import geopandas as gpd
import numpy as np
import math
import matplotlib.pyplot as plt
from kdtree import kdTree, kdTree_node
# Converts lat and lng coordinates to local x,y positions (around the mean)
# This is a first order approximation
def latlngToGlobalXY(coords):
    radius = 6371.0
    dlon = math.pi*(coords[0]-lonMean)/180.0
    dlat = math.pi*(coords[1]-latMean)/180.0
    x = radius*dlon*math.cos(math.pi*latMean/180.0)
    y = radius*dlat
    return x,y

def drawSubtree(node,s, ax):
    if node.left!=None:
        drawSubtree(node.left,s+1, ax)
        # Draw the current node as a line segment
    width = 8-s
    if node.split_along_x==True:
        if (width>0):
            ax.plot([node.x,node.x],[max(-5,node.ymin),min(node.ymax,5)],linewidth=width)
    else:
        if (width>0):
            ax.plot([max(-5,node.xmin),min(node.xmax,5)],[node.y,node.y],linewidth=width)
    
    if node.right!=None:
        drawSubtree(node.right,s+1, ax)
def draw(kdTree, ax):
    drawSubtree(kdTree.root,0, ax)

if __name__=='__main__':
    df_s = pd.read_json('estaciones.json', orient='columns')
    # Get positions (longitudes/latitudes)
    stations_positions = df_s[['lon','lat']].values.reshape(-1,2)
    # Average
    lonMean = np.average(stations_positions[:,0])
    latMean = np.average(stations_positions[:,1])
    # Converts into x,y around the average
    locs_bici = np.apply_along_axis(latlngToGlobalXY, 1, stations_positions)

    kdt = kdTree(locs_bici[:,0],locs_bici[:,1])
    # Plot the station positions and the number of slots

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(5,3))
    axes[0].scatter(locs_bici[:,0],locs_bici[:,1])
    plt.gca().set_aspect('equal', adjustable='box')
    plt.legend('Ecobici stations')
    

    draw(kdt, axes[1])
    plt.show()





