#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 15:02:40 2020

sums the total # of county splits in a partition
which is the length of county_splits
@author: dpg
"""

from gerrychain import updaters
def total_splits(partition):
    #county_field  = 'COUNTYFP10'
    #county_field = "COUNTY"
    fieldlist = partition.graph.nodes[0].keys()   #get LIST OF FIELDS
    
    if 'COUNTYFP10' in fieldlist:
        county_field = 'COUNTYFP10'
    elif 'COUNTYFP20' in fieldlist:
        county_field = 'COUNTYFP20'
    elif 'CTYNAME' in fieldlist:
        county_field = 'CTYNAME'
    
    elif 'COUNTYFIPS' in fieldlist:
        county_field = 'COUNTYFIPS'
    
    elif 'COUNTYFP' in fieldlist:
        county_field = 'COUNTYFP'
    elif 'cnty_nm' in fieldlist:
        county_field = 'cnty_nm'
    elif 'county_nam' in fieldlist:
        county_field = 'county_nam'
    elif 'FIPS2' in fieldlist:
        county_field = 'FIPS2'
    elif 'COUNTY' in fieldlist:
        county_field = 'COUNTY'
    elif 'County' in fieldlist:
        county_field = 'County'
        
    elif 'CNTY_NAME' in fieldlist:
        county_field = 'CNTY_NAME'
    
    else:
        print("no county ID info in shapefile\n")
        return 10
    
    gg = updaters.county_splits(partition, county_field)
    gg_res = gg(partition)
    splitcount=0
    for x in gg_res:
        splitcount+= len(gg_res[x].contains) -1 #subtract 1 b/c there's 1 county listed if there are no splits
        
    return splitcount

#print(total_splits(initial_partition))