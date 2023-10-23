import pandas as pd
import numpy as np
import pickle
import os

# Plotting Packages
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns

mpl.rcParams['figure.dpi'] = 300
savefig_options = dict(format="png", dpi=300, bbox_inches="tight")
plt.rcParams.update({'font.size': 14})

from math import log, exp, tan, cos, pi, atan, ceil

def findcenters(edges):
    lat_edges, lon_edges, speed_edges, course_edges = edges
    
    lat_dim = len(lat_edges) - 1
    lon_dim = len(lon_edges) - 1
    speed_dim = len(speed_edges) - 1
    course_dim = len(course_edges) - 1
    
    lat_centers = [round((lat_edges[i]+lat_edges[i+1])/2,3) for i in range(len(lat_edges)-1)] 
    lon_centers = [round((lon_edges[i]+lon_edges[i+1])/2,3) for i in range(len(lon_edges)-1)] 
    speed_centers = [round((speed_edges[i]+speed_edges[i+1])/2,3) for i in range(len(speed_edges)-1)] 
    course_centers = [round((course_edges[i]+course_edges[i+1])/2,3) for i in range(len(course_edges)-1)]
    
    return lat_centers,lon_centers,speed_centers,course_centers

def get_static_map_bounds(lat, lng, zoom, sx, sy):
    # lat, lng - center
    # sx, sy - map size in pixels

    # 256 pixels - initial map size for zoom factor 0
    sz = 256 * 2 ** zoom

    #resolution in degrees per pixel
    res_lat = cos(lat * pi / 180.) * 360. / sz
    res_lng = 360./sz

    d_lat = res_lat * sy / 2
    d_lng = res_lng * sx / 2

    return ((lat-d_lat, lng-d_lng), (lat+d_lat, lng+d_lng))

def getPositionalBoundaries(edges, zoom=8):
    
    lat_centers, lon_centers, speed_centers, course_centers = findcenters(edges)

    lat_center = lat_centers[int(len(lat_centers) / 2)] 
    lon_center = lon_centers[int(len(lon_centers) / 2)] 

    SW_corner, NE_corner = get_static_map_bounds(lat_center, lon_center, zoom, 640, 640)
    lat_min, lon_min = SW_corner
    lat_max, lon_max = NE_corner
    
    return lat_min, lat_max, lon_min, lon_max

def forceAspect(ax,aspect=1):
    im = ax.get_images()
    extent =  im[0].get_extent()
    ax.set_aspect(abs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspect)

def plotMapBackground(ax, edges):
    
    lat_min, lat_max, lon_min, lon_max = getPositionalBoundaries(edges, zoom=8)
    if edges[0][0]==54.5:
        img = mpimg.imread('plots/Bornholm.png')
    elif edges[0][0]==54.4:
        img = mpimg.imread('plots/Sjælland.png')
    elif edges[0][0]==56:
        img = mpimg.imread('plots/Anholt.png')
    
    ax.imshow(img, extent=[lon_min, lon_max, lat_min, lat_max])
    
    forceAspect(ax,aspect=1)
    ax.set_xlim([lon_min, lon_max])
    ax.set_ylim([lat_min, lat_max])
    ax.set_xlabel('Longitude')
    ax.set_xlabel('Latitude')
    
    return ax
    
def plotTrack(data, speed, ax, color=None, lsty='solid', insertSpeed=False):

    seq_len = data.shape[0]

    lat = data[:,0]
    lon = data[:,1]

    points = np.array([lon, lat]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    
    cmap=plt.get_cmap('inferno') #Black is start, yellow is end
    if color is None:
        colors=[cmap(float(ii)/(seq_len-1)) for ii in range(seq_len-1)]  
    else:
        colors = [color]*(seq_len-1)
                       
    for ii in range(0,seq_len-1):
        segii=segments[ii]
        lii, = ax.plot(segii[:,0],segii[:,1],color=colors[ii],linestyle=lsty)           
        lii.set_solid_capstyle('round')
    
    if color is not None:
        ax.scatter(lon[0],lat[0],color='k')
    
    if insertSpeed:
        ins = ax.inset_axes([0.05,0.6,0.35,0.4])
        ins.plot(speed)
        
    return ax

def convertCourseToTrig(course):

    trig = np.concatenate([np.expand_dims(np.sin(np.deg2rad(course)),axis=1), np.expand_dims(np.cos(np.deg2rad(course)),axis=1)],axis=1)
    
    return trig
    
def convertTrigToCourse(Trig):
    
    ### Trig[:,0] = sin, Trig[:,1] = cos
    
    course = np.rad2deg(np.arctan2(Trig[:,0], Trig[:,1]))
    course[course < 0] = course[course < 0]+360
    
    return course



        

    


