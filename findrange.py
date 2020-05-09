from kdtree import kdTree, kdTree_node
import pandas as pd
import numpy as np
import math

def latlngToGlobalXY(coords):
    radius = 6371.0
    dlon = math.pi*(coords[0]-lonMean)/180.0
    dlat = math.pi*(coords[1]-latMean)/180.0
    x = radius*dlon*math.cos(math.pi*latMean/180.0)
    y = radius*dlat
    return x,y


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

	xmin =  int(input("Enter min x: "))
	xmax = int(input("Enter max x: "))
	ymin = int(input("Enter min y: "))
	ymax = int(input("Enter max y: "))

	r = {'xmin':xmin ,'xmax':xmax, 'ymin':ymin, 'ymax': ymax}
	node = kdTree_node(xmax, ymin)
	results = kdt.range_search(kdt.root, r)

	x = [node.x for node in results]
	y = [node.y for node in results]
	
	print(pd.DataFrame({'x':x, 'y':y}))