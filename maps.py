from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt


class general_map:
    def __init__(self,fig_title):
        self._fig_title=fig_title
        set_fig_params()
   

    def set_fig_params():
        self.params = {
                 'hgt': {'250': {'int':  12, 'min': 960, 'max': 1110}, 
                         '500': {'int':   6, 'min': 498, 'max':  600},
                         '700': {'int':   6, 'min': 252, 'max':  324},
                         '850': {'int':   6, 'min': 102, 'max':  178},
                         'unit': 'dm'},
                 'tmp': {'500': {'int': 2.5, 'min': -75, 'max':  15},
                         '700': {'int': 2.5, 'min': -45, 'max':  45},
                         '850': {'int': 2.5, 'min': -45, 'max':  45},
                         'unit': 'C'},
                 'vort':{'500': {'int':   2, 'min': -20, 'max':  20},
                         'unit': '10e-5 s-1'}, 
                 'vvel':{'700': {'int':   5, 'min': -23, 'max':  38},
                         'unit': '-Pa/s*10'}, 
                 'wind':{'250': {'int':  20, 'min':   0, 'max': 220}, 
                         'unit': 'kt'},
                 'rh'  :{'850': {'int':  10, 'min':   0, 'max': 105},
                         'unit': '%'} 
                 }


    def draw_map(self):
               # Make figure
        lon=self.lon
        lat=self.lat
        fp=self.params 
        m=self.m
        plt.figure(figsize=(12,8))
        x, y = m(lon,lat)
        min=fp[self.myvar][str(sefl.level)]['min']
        max=fp[self.myvar][str(sefl.level)]['max']
        int=fp[self.myvar][str(sefl.level)]['int']

        print 

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
        data=self.field.values/10.
#        lons, lats = np.meshgrid(self.lon, self.lat)
#        x, y = m(*np.meshgrid(lon, lat))
#        x, y = m(self.lon, self.lat)
        clevs = np.arange(min,max,int)
        cs = m.contourf(x,y,data,clevs,cmap=plt.cm.jet)
#        cs.set_clim()
        cbar=plt.colorbar(cs,orientation='horizontal')
#        cbar.set_clim(9000,11000)
        cbar.set_ticks(np.arange(900,1200,24))
        cbar.set_ticklabels(np.arange(900,1200,24))
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
    def __init__(self,field,lat,lon,date,hour,myvar,level,fig_title,area_flag=None,ncep_grid=None,resolution=None):
        #super(global_map).__init__(self,fig_title)

        self.field=field
        self.lat, self.lon = field.latlons()
        self.myvar=myvar
        self.level=level
        if area_flag == None or area_flag == 'glob':
            self.m=Basemap(projection='mill',lat_ts=10,llcrnrlon=0,
                urcrnrlon=357.5,llcrnrlat=-90,urcrnrlat=90,
                resolution='c')

        elif area_flag == 'nh':
            self.m=Basemap(projection='mill',lat_ts=10,llcrnrlon=0,
                urcrnrlon=357.5,llcrnrlat=0,urcrnrlat=90,
                resolution='c')

        elif area_flag == 'sh':
            self.m=Basemap(projection='mill',lat_ts=10,llcrnrlon=0,
                urcrnrlon=357.5,llcrnrlat=-90,urcrnrlat=0,
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
















