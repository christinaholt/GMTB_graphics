import pygrib
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import datetime

# Multipanel plot - subplot(rcp)


plt.figure()
grib='four04e.2012070412.hwrfprs.d1.0p25.f048.grb2'
grbs=pygrib.open(grib)


# Plot a 2-D Field: prmsl (Pressure reduced to MSL)

grb = grbs.select(name="Pressure reduced to MSL")[0]
PRMSL=grb.values
lat,lon = grb.latlons()

date=str(grb['dataDate'])
hour=str(grb['hour'])
fcsthr=str(grb[u'forecastTime'])

cycle= date.join(hour)



m = Basemap(projection='lcc',lat_1=45., lat_2=55, 
           lat_0=np.median(lat),lon_0=np.median(lon),\
           rsphere=(6378137.00,6356752.3142),\
           llcrnrlon=lon.min(),urcrnrlon=lon.max(), \
           llcrnrlat=lat.min(),urcrnrlat=lat.max(), \
           area_thresh=500.)

m.drawcoastlines()
#m.drawparallels(np.arrange(lat.min(),lat.max(),20))
#m.drawmeridians(np.arrange(lon.min(),lon.max(),60))
m.drawmapboundary()

x, y = m(lon,lat)

cs = m.pcolormesh(x,y,PRMSL,shading='flat',cmap=plt.cm.jet)

plt.colorbar(cs,orientation='vertical')
plt.title('MSLP for 04E %s hr fcst from %s cycle' % (fcsthr,cycle))
plt.show()


