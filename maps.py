from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt


class general_map:
    def __init__(self,fig_title):
        self._fig_title=fig_title
    
    def draw_map(self):
               # Make figure
        lon=self.lon
        lat=self.lat
        m=self.m
        plt.figure(figsize=(12,8))
        #m =Basemap(projection='stere',lon_0=center[0],lat_0=center[1],lat_ts=center[2],\
        #            llcrnrlat=center[3],urcrnrlat=center[4],\
        #            llcrnrlon=center[5],urcrnrlon=center[6],\
        #            rsphere=6371200.,resolution='l',area_thresh=10000)
        x, y = m(lon,lat)

        # Draw political boundaries
        m.drawcoastlines()
        m.drawstates()
        m.drawcountries()
        m.drawmapboundary()
        m.drawlsmask(ocean_color='0.8',land_color='white')

        # Draw lat/lon grid
        parallels = np.arange(-90.,90,10.)
        m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
        meridians = np.arange(0.,360.,20.)
        m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)
        data=self.field.values
#        lons, lats = np.meshgrid(self.lon, self.lat)
        x, y = m(*np.meshgrid(self.lon, self.lat))
        cs = plt.pcolormesh(x,y,data,shading='flat',cmap=plt.cm.jet)
        plt.colorbar(cs,orientation='vertical')
        plt.title('Example 2')
#        plt.show()

    #### Change ALL THIS STUFF!!! ###
    def save_figure(self):
        filename="test.png"
       # plt.title('%s UTC %s' % (VT, day2.strftime('%Y-%m-%d')), fontsize=44)
        plt.savefig('./figs/%s' % filename, bbox_inches='tight')
        plt.close()


    def draw_field(self):
        data=self.field.values
        m=self.m
        x, y = m(self.lon,self.lat)
        cs = plt.pcolormesh(x,y,data,shading='flat',cmap=plt.cm.jet)
        plt.colorbar(cs,orientation='vertical')
        plt.title('Example 2')
        plt.show()

    def plot_title(self):
        # plt.title('%s at %s %s hr fcst from %s cycle' % 
        # (field.name,field.level,field.pressureUnits,fcsthr,cycle))
        pass
    def display_map(self):
        pass

    def run(self):
        self.draw_map()
#        self.draw_field()
#        self.plot_title()
#        self.display_map()
        self.save_figure()


class global_map(general_map):
    def __init__(self,field,lat,lon,date,hour,myvar,fig_title,area_flag=None,ncep_grid=None,resolution=None):
        #super(global_map).__init__(self,fig_title)

        self.field=field
        self.lat, self.lon = field.latlons()
        if area_flag == None or area_flag == 'glob':
            self.m=Basemap(projection='mill',lat_ts=10,llcrnrlon=-180,
                urcrnrlon=180,llcrnrlat=-90,urcrnrlat=90,
                resolution='c')

        elif area_flag == 'nh':
            self.m=Basemap(projection='mill',lat_ts=10,llcrnrlon=-180,
                urcrnrlon=180,llcrnrlat=0,urcrnrlat=90,
                resolution='c')

        elif area_flag == 'sh':
            self.m=Basemap(projection='mill',lat_ts=10,llcrnrlon=-180,
                urcrnrlon=180,llcrnrlat=-90,urcrnrlat=0,
                resolution='c')

class conus_map(general_map):
    def __init__(self,ncep_map=None):
        if ncep_map == None or ncep_map == 130 or ncep_map == 236:
            self.ll_lon = 126.138 # Lower left corner longitude
            self.ll_lat = 16.281 # Lower left corner latitude
            self.ur_lon = 57.383 # Upper right corner longitude
            self.ur_lat = 55.481 # Upper right corner latitude
            self.rad_ear = (6378137.00,6356752.3142) # Radius of earth 
            self.area_thre = 1000 # Don't draw bdys smaller than this area
            self.proj = 'lcc' # Projection
            self.res = 'i' # Resolution of boundary data


        self.m = Basemap(llcrnrlon=self.ll_lon, llcrnrlat=self.ll_lat,
            urcrnrlon=self.ur_lon, urcrnrlat=self.ur_lat,
            rsphere=self.rad_ear,
            resolution=self.res,area_thresh=self.area_thre,projection=self.proj,
            lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)
















