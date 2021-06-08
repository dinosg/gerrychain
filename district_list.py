#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 11:04:01 2020
takes a partion 'part'  and creates a list qlist with the index of VTDs and column of assignments. Converts to DataFrame
and writes to file
@author: dpg
"""
import numpy as np
import pandas as pd
import geopandas
from gerrychain import Graph
import pickle as pk
import os
"""
nn = part.graph.number_of_nodes()
qlist = np.zeros([nn,2]) #for PA w 9256 vtds
aa = part.assignment  #gets the assignment from the partition
aap = aa.parts   #gets the frozen set containing the sub-frozen set of VTDs for each district
c=0
for k in aap: #loop thru each district frozen set
    kl0 = list(aap[k])
    for zz in kl0:
        #print(zz,k)
        qlist[c,:] = [zz,k]
        c=c+1
        
qlistp = pd.DataFrame(qlist)
qlistp.columns = ["VTD","District Assignment"]
qlistp.to_csv("PA_test.csv")
"""

""" 
#to plot and output the part as a map you need to do something a little more complicated
#read in a shapefile into a Graph dataframe:
shapefilepath = ''  #whatever the path is    
df = geopandas.read_file(shapefilepath)
df.to_crs({"init": "epsg:26986"}, inplace=True)

junkplot, df1 = part.plot(df, figsize=(10,10), cmap="tab20")
df1.to_file('filename.shp')   #writes out plot to filename

"""

def part_dump(part, filepath, metricinfo=None):
    """
    
    writes out csv file with data as dataframe so you can match up to map using GEOID10 as join field
    Parameters
    ----------
    part : partition
        DESCRIPTION.
    filepath : string with filename/ path
        DESCRIPTION.

    Returns
    -------
    None.
   

    

  
    nn = part.graph.number_of_nodes()
    qlist = np.zeros([nn,2]) #for PA w 9256 vtds
    aa = part.assignment  #gets the assignment from the partition
    aap = aa.parts   #gets the frozen set containing the sub-frozen set of VTDs for each district
    c=0
    for k in aap: #loop thru each district frozen set
        kl0 = list(aap[k])
        for zz in kl0:
            #print(zz,k)
            qlist[c,:] = [zz,k]
            c=c+1
            
    qlistp = pd.DataFrame(qlist)
    qlistp.columns = ["VTD","District Assignment"]
    qlistp.to_csv(filepath)
    return
"""
   
    s1 = part.assignment.to_series()
    geofield = ''
    if hasattr(part.graph, 'data'):    #the case if data was read in from .shp file... this field exists
       
        part0 = part.graph.data #extract the DataFrame with all the information
        cols = part0.columns
    
    elif hasattr(part.graph,'_node'):  #the case if data was read in from .json, no data field
        aaa = part.graph._node
        part0 = pd.DataFrame(aaa).transpose() #create the DataFrame from the dict info in .graph._node
        cols = part0.columns
    try:
        #1st figure out what the unique VTD identifier is... not always "GEOID10" unfortunately, depends on state
        
        if 'GEOID20' in cols:
            geofield = 'GEOID20'
        elif 'GEOID10' in cols:
            geofield = 'GEOID10'
        elif 'JOINDID' in cols:
            geofield = 'JOINID'
        elif 'loc_prec' in cols:
            geofield = 'loc_prec'
        elif 'PCTCODE' in cols:
            geofield = 'PCTCODE'
        elif "VTD_1" in cols:
            geofield = "VTD_1"
        elif "VTD_Key" in cols:
            geofield = "VTD_Key"
        elif "VTD2016_x" in cols:
            geofield = "VTD2016_x"
        elif "VTDST" in cols:
            geofield = "VTDST"
        elif "CNTYVTD" in cols:
            geofield = "CNTYVTD"
        elif "DsslvID" in cols:
            geofield = "DsslvID"
        elif "EDRD_2012" in cols:
            geofield = "EDRD_2012"
        elif "full_text" in cols:
            geofield = "full_text"
        elif "PRECODE" in cols:
            geofield = "PRECODE"
        elif "CODE" in cols:
            geofield = "CODE"
        elif "PRECINCT" in cols:
            geofield = "PRECINCT"
        elif "Precinct" in cols:
            geofield = "Precinct"
        elif "NAME10" in cols:
            geofield = "NAME10"
        elif "Name" in cols:
            geofield = "Name"
        elif "NAME" in cols:
            geofield = "NAME"
        
        else:
            print("No match to geofield column names\n")
        
        #get the output filename right in this so everything with respect to 'redistricting' directory
        #regardless of how far below the path is where the program is run
        getdir = os.getcwd()   #figure out what directory we're in
        getdir = getdir.split('/') #split the working directory by /'s to get depth of hierarchy levels
        levelinhierarchy = getdir.index('redistricting') #find out which level the 'redistricting' directory is at
        prefixa = ''
        for ik in range(len(getdir) - levelinhierarchy - 1):
            prefixa = prefixa + '../'
        df = pd.DataFrame(part0[geofield])
        df["assignment"]= s1
        print('output to file ', prefixa+filepath, '\n')
        
        
    except:
        print("no graph data in this partition\n")
        df = pd.DataFrame(s1)
    df.to_csv(prefixa+filepath, index=False)
    if metricinfo != None :
        fp1 = str.replace(prefixa+filepath, 'txt','dat')
        pk.dump(metricinfo, open(fp1, "wb"))
    return df


def part_plot(df, part, filepath):
    """
    
  df = geopandas dataframe, need to read in original file in this format
  part = whatever partition you want to plot
  filepath = name of .shp file you want to save resulting partition with segments to
    ----------
  PLOTS the part as a segmented map
        

    Returns
    -------
    None.

    """
#df needs to be read in this way: df = geopandas.read_file(shapefilepath)
    df.to_crs({"init": "epsg:26986"}, inplace=True)
    
    junkplot, df1 = part.plot(df, figsize=(10,10), cmap="tab20")
    if filepath != []:
        df1.to_file(filepath, index=False)   #writes out plot to filename
    
    return

        
        