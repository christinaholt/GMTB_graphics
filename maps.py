from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt


class general_map(object):
    def __init__(self,fig_title):
        self._fig_title=fig_title
        self.params = self.set_fig_params()

    def set_fig_params(self):
        params = {
                 'gh': {'250': {'int':  12, 'min': 888, 'max': 1122}, 
                         '500': {'int':   6, 'min': 498, 'max':  600},
                         '700': {'int':   3, 'min': 252, 'max':  324},
                         '850': {'int':   3, 'min': 102, 'max':  178},
                         'unit': 'dam'},
                 'tmp': {'250': {'int':   5, 'min': -75, 'max':  15},
                         '500': {'int':   5, 'min': -75, 'max':  15},
                         '700': {'int':   5, 'min': -45, 'max':  45},
                         '850': {'int':   5, 'min': -45, 'max':  45},
                         'unit': 'C'},
                 'vort':{'500': {'int':   2, 'min': -20, 'max':  20},
                         'unit': '10e-5 s-1'}, 
                 'vvel':{'700': {'int':   5, 'min': -23, 'max':  38},
                         'unit': '-Pa/s*10'}, 
                 'wind':{'250': {'int':  20, 'min':  30, 'max': 220}, 
                         'unit': 'kt'},
                 'rh'  :{'850': {'int':  10, 'min':   0, 'max': 105},
                         'unit': '%'} 
                 }
        return params

    def draw_map(self):
        # Make figure
        lon=self.lon
        lat=self.lat
        fp=self.params 
        m=self.m
        plt.figure(figsize=(15,12))

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

    #### Change ALL THIS STUFF!!! ###
    def save_figure(self):
        filename="test.png"
        plt.savefig('./figs/%s' % filename)
        plt.close()


    def fill_field(self):
        data=self.field.values
        m=self.m
        fp=self.params
        data=self.field.values/10.
        x, y = m(self.lon,self.lat)
        min=fp[self.myvar][str(self.level)]['min']
        max=fp[self.myvar][str(self.level)]['max']
        int=fp[self.myvar][str(self.level)]['int']

        clevs = np.arange(min,max,int)
        cs = m.contourf(x,y,data,clevs,cmap=plt.cm.jet)
        cbar=plt.colorbar(cs,orientation='vertical',shrink=0.8)


    def contour_field(self):
        m=self.m
        fp=self.params
        data=self.field.values/10.
        x, y = m(self.lon,self.lat)
        min=fp[self.myvar][str(self.level)]['min']
        max=fp[self.myvar][str(self.level)]['max']
        int=fp[self.myvar][str(self.level)]['int']

        clevs = np.arange(min,max,int)
        cc = m.contour(x,y,data,clevs, colors='k')
        plt.clabel(cc, fontsize=10, inline=1, fmt= '%4.0f')


    def wind_field(self):
        m=self.m
        fp=self.params
        u=self.u.values
        v=self.v.values
        
        # Mask for winds
        maskarray = np.ones(u.shape)
        maskarray[::4,::4] = 0
       
        mu = np.ma.masked_array(u, mask=maskarray) 
        mv = np.ma.masked_array(v, mask=maskarray) 
        x, y = m(self.lon,self.lat)

        self.barbs = m.barbs(x, y, mu, mv, barbcolor='k' )

    def plot_title(self):
         field=self.field
         fp=self.params
         date = str(field['dataDate'])
         myvar = str(field['name'])
         atime = field.analDate.strftime('Analysis: %Y%m%d %H UTC')
         vtime = field.validDate.strftime('Valid: %Y%m%d %H UTC')

         level = str(self.level)
         punit = str(field['pressureUnits'])
         vunit = fp[self.myvar]['unit']
         maptype = 'shaded'
         fcsthr=str(field['forecastTime'])
         #cycle=str(field['analysisTime'])
         plt.title('%s \nFcst Hr: %s' % (atime, fcsthr) , loc='left')
         plt.title('%s %s' % (level,punit), position=(0.5, 1.04), fontsize=18)
         plt.title('%s (%s, %s)' % (myvar,vunit,maptype)
               , loc = 'right')
         plt.xlabel('%s' % (vtime), fontsize=18, labelpad=40)

    def display_map(self):
        plt.show()

    def run(self):
        self.draw_map()
        self.fill_field()
        self.contour_field()
        self.wind_field()
        self.plot_title()
#        self.display_map()
        self.save_figure()


class global_map(general_map):
    def __init__(self,field,lat,lon,date,hour,myvar,level,fig_title,area_flag=None,ncep_grid=None,
                 resolution=None, winds=None, plot_wind=False):
        super(global_map,self).__init__(fig_title)

        self.field=field
        self.lat, self.lon = field.latlons()
        self.myvar=myvar
        self.level=level
        self.u = winds[0]
        self.v = winds[1]
        
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
















