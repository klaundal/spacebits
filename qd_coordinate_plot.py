import matplotlib.pyplot as plt
import numpy as np
import apexpy
from mpl_toolkits.basemap import Basemap
from datetime import datetime

def setcolor(x, color):
     for m in x:
         for t in x[m][1]:
             t.set_color(color)

DATE = datetime(2015, 1, 1)

a = apexpy.Apex(date = DATE, refh = 0)

fig = plt.figure(figsize = (10, 10), facecolor = 'white')
latsteps = np.r_[-80:90:10]
lonsteps = np.r_[-150:181:30]
global_latstep = np.r_[-80:81:20]

latx = np.linspace(10, 80, 100)
lonx = np.linspace(-180, 180, 300)

# set up the axes and map projections
axes = {}
maps = {}

axes['north'] = fig.add_subplot(221)
axes['south'] = fig.add_subplot(222)
axes['globe'] = fig.add_subplot(212)

maps['north'] = Basemap(ax = axes['north'], width=12100000,height=12100000,
                        resolution='c',projection='stere',\
                        lat_ts=90,lat_0=90,lon_0=0)
maps['south'] = Basemap(ax = axes['south'], width=12100000,height=12100000,
                        resolution='c',projection='stere',\
                        lat_ts=-90,lat_0=-90,lon_0=0)
maps['globe'] = Basemap(ax = axes['globe'], projection='mill', llcrnrlat=-70, urcrnrlat=70,\
                        llcrnrlon=-180, urcrnrlon=180, lat_ts = 0,resolution='c')



for key in maps.keys():
    axes[key].set_axis_off()
    maps[key].fillcontinents(zorder = 0,  color = 'gainsboro', lake_color = 'gainsboro')

text = maps['globe'].drawparallels(np.r_[-80:80:20], color =   'silver', linewidth = 2, dashes = [1, 3]  , labels = [1, 0, 0, 0], labelstyle = '+/-')
setcolor(text, 'gray')
text = maps['globe'].drawmeridians(np.r_[-180:180:30], color = 'silver', linewidth = 2, dashes = [1, 3], labels = [0, 0, 0, 1], labelstyle = '+/-')
setcolor(text, 'gray')

for key in ['north', 'south']:
    maps[key].drawparallels(latsteps, color = 'silver', linewidth = 2, dashes = [1, 3])

text = maps['north'].drawmeridians(lonsteps, color = 'silver', linewidth = 2, dashes = [1, 3], labels = [1, 0, 1, 1], labelstyle = '+/-')
setcolor(text, 'gray')
text = maps['south'].drawmeridians(lonsteps, color = 'silver', linewidth = 2, dashes = [1, 3], labels = [0, 1, 1, 1], labelstyle = '+/-')
setcolor(text, 'gray')

fig.subplots_adjust(left = .1, right = 1-.1, wspace = .05, hspace = .03, bottom = .02, top = 1-0.02)


polar_lons = []
polar_lats = []

global_lons = []
global_lats = []

# qd
for lat in latsteps:
    polar_lats.append(np.ones_like(lonx) * lat)
    polar_lons.append(np.linspace(30 - 15 * np.cos(lat*np.pi/180), 360 + 15*np.cos(lat * np.pi/180), 300))

    gdlat, gdlon, error = a.qd2geo(np.ones_like(lonx) * lat, np.linspace(30 - 15 * np.cos(lat*np.pi/180), 360 + 15*np.cos(lat * np.pi/180), 300), 0)
    x, y = maps['north'](gdlon, gdlat)
    maps['north'].plot(x, y, color = 'darkred', linewidth = 2, latlon = False)
    
    # write latitude labels
    text_lat, text_lon, error = a.qd2geo(lat, 15., 0)
    text_x, text_y = maps['north'](text_lon, text_lat)
    if (text_x > maps['north'].xmin) and (text_x < maps['north'].xmax) & (text_y > maps['north'].ymin) & (text_y < maps['north'].ymax):
        print( text_x, text_y)
        axes['north'].text(text_x, text_y, r'$' + str(lat) + '^\circ$', size = 12, color = 'darkred', va = 'center', ha = 'center')


    gdlat, gdlon, error = a.qd2geo(-np.ones_like(lonx) * lat, np.linspace(30 - 15 * np.cos(lat*np.pi/180), 360 + 15*np.cos(lat * np.pi/180), 300), 0)
    x, y = maps['south'](gdlon, gdlat)
    maps['south'].plot(x, y, color = 'darkred', linewidth = 2, latlon = False)

    # write latitude labels
    text_lat, text_lon, error = a.qd2geo(-lat, 15., 0)
    text_x, text_y = maps['south'](text_lon, text_lat)
    if (text_x > maps['south'].xmin) and (text_x < maps['south'].xmax) & (text_y > maps['south'].ymin) & (text_y < maps['south'].ymax):
        print( text_x, text_y)
        axes['south'].text(text_x, text_y, r'$' + str(lat) + '^\circ$', size = 12, color = 'darkred', va = 'center', ha = 'center')

    global_lats.append(np.ones_like(lonx))
    global_lons.append(np.linspace(-180, 180, 300))

    gdlat, gdlon, error = a.qd2geo(np.ones_like(lonx)*lat, np.linspace(-180, 180, 300), 0)
    x, y = maps['globe'](gdlon, gdlat)
    if lat not in [80, -80]:
        iii = np.argsort(x)
        x = x[iii]
        y = y[iii]

    maps['globe'].plot(x, y, color = 'darkred', linewidth = 2, latlon = False)
    text_x = np.max(x)
    text_y = y[x == np.max(x)]
    if text_y < maps['globe'].ymin or text_y > maps['globe'].ymax:
        continue
    axes['globe'].text(maps['globe'].xmax + 1500000,  text_y, r'$' + str(lat) + '^\circ$', size = 12, color = 'darkred', va = 'center', ha = 'right')


for lon in lonsteps:



    gdlat, gdlon, error = a.qd2geo(np.linspace(10, 52, 50), np.ones(50)*lon, 0)
    x, y = maps['north'](gdlon, gdlat)
    maps['north'].plot(x, y, color = 'darkred', linewidth = 2, latlon = False)
    gdlat, gdlon, error = a.qd2geo(np.linspace(58, 80, 50), np.ones(50)*lon, 0)
    x, y = maps['north'](gdlon, gdlat)
    maps['north'].plot(x, y, color = 'darkred', linewidth = 2, latlon = False)

    # write longitude labels

    text_lat, text_lon, error = a.qd2geo(55, lon, 0)
    text_x, text_y = maps['north'](text_lon, text_lat)
    if (text_x > maps['north'].xmin) and (text_x < maps['north'].xmax) & (text_y > maps['north'].ymin) & (text_y < maps['north'].ymax):
        axes['north'].text(text_x, text_y, r'$' + str(lon) + '^\circ$', size = 12, color = 'darkred', va = 'center', ha = 'center')


    gdlat, gdlon, error = a.qd2geo(-np.linspace(10, 52, 50), np.ones(50)*lon, 0)
    x, y = maps['south'](gdlon, gdlat)
    maps['south'].plot(x, y, color = 'darkred', linewidth = 2, latlon = False)
    gdlat, gdlon, error = a.qd2geo(-np.linspace(58, 80, 50), np.ones(50)*lon, 0)
    x, y = maps['south'](gdlon, gdlat)
    maps['south'].plot(x, y, color = 'darkred', linewidth = 2, latlon = False)
    
    # write longitude labels
    text_lat, text_lon, error = a.qd2geo(-55, lon, 0)
    text_x, text_y = maps['south'](text_lon, text_lat)
    if (text_x > maps['south'].xmin) and (text_x < maps['south'].xmax) & (text_y > maps['south'].ymin) & (text_y < maps['south'].ymax):
        axes['south'].text(text_x, text_y, r'$' + str(lon) + '^\circ$', size = 12, color = 'darkred', va = 'center', ha = 'center')

    

    gdlat, gdlon, error = a.qd2geo(np.linspace(-80, 80, 200), np.ones(200)*lon, 0)  
    x, y = maps['globe'](gdlon, gdlat)
    iii = np.where((x >= maps['globe'].xmin) &
                   (x <= maps['globe'].xmax) &
                   (y >= maps['globe'].ymin) &
                   (y <= maps['globe'].ymax))[0]
    x = x[iii]
    y = y[iii]
    ds = (x[1:] - x[:-1])**2 + (y[1:] - y[:-1])**2

    iii = np.where(ds > 1e14)[0]
    if len(iii) > 0:
        xs = np.split(x, iii+1)
        ys = np.split(y, iii+1)
        for x_, y_ in zip(xs, ys):
            maps['globe'].plot(x_, y_, color = 'darkred', linewidth = 2, latlon = False)
    else:
        maps['globe'].plot(x, y, color = 'darkred', linewidth = 2, latlon = False)

    text_y = np.max(y)
    text_x = x[y == np.max(y)]
    axes['globe'].text(text_x, maps['globe'].ymax, r'$' + str(lon) + '^\circ$', size = 12, color = 'darkred', va = 'bottom', ha = 'center')




nlat, nlon, error = a.qd2geo(90, 0, 0)
slat, slon, error = a.qd2geo(-90, 0, 0)
maps['north'].scatter(nlon, nlat, marker = 'o', latlon = True, color = 'darkred', linewidth = 2)
maps['south'].scatter(slon, slat, marker = 'o', latlon = True, color = 'darkred', linewidth = 2)





plt.show()
