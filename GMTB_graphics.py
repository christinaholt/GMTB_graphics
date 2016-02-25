#! /anaconda/bin python



import pygrib
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os,sys,shutil
import maps

def get_ua_field(fn,var,lev,levtype,anlTime=None,fcstHr=None):
    # Get the required grib field given a file name
    # fn: filename, var: variable to plot, lev: level
    # to plot in hPa, levtype: type of level in grib file
    # anlTime: optional analysis time 
    # for a sanity check, fcstHr: option forecast hour
    # in case a file contains multiples and not in fn. 

    grib=fn
    grbs=pygrib.open(fn)
    grb = grbs.select(shortName=var,typeOfLevel=levtype,
          level=lev)[0]
     
    return grb

def main():
 

    global grib, fcsthr, field, lat, lon, date, hour, cycle, outmap, myvar
    # Set input file name
    inputdir='/scratch4/BMC/gmtb/jhender/NCEPDEV/stmp4/Judy.K.Henderson/prtutornems'
    filename='pgrbl024.gfs.2016012200.grib2'
    grib=inputdir'/'filename 
    # Set forecast hour
    fcsthr=None
    
    # Get the variable from file
    field=get_ua_field(grib,"gh",250,"isobaricInhPa")
    # Get lat lon info from file
    lat,lon = field.latlons()
     
    date = str(field['dataDate'])
    hour = str(field['hour'])
    myvar = str(field['name'])
    if fcsthr is None: fcsthr=str(field['forecastTime'])
    
    cycle= date.join(hour)
    
    outmap='glob'
    
    mymap=maps.global_map(field,lat,lon,date,hour,myvar,'test.png',area_flag=outmap) 
    mymap.run()
    # draw a global map
    
     
    
    #cs = m.pcolormesh(x,y,PRMSL,shading='flat',cmap=plt.cm.jet)
    
    
main()    
