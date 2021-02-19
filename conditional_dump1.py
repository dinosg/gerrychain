#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 09:32:53 2020

scripts for dumping VTD assignments to a file when certain conditions are met

eg_gt... dumps to a file when the efficiency gap > hi_eg. This dumps out a map that's apportioned favorably
for dems'

eg_zero dumps to a file when the abs value of efficiency gap < zero_eg, that is, a fair map

eg_lt dumps to a file when efficiency gap < lo_eg, that is favorable to republicans
 

eg_gt_x  does the same thing but for partitions returned by chain_xtended, which has a little diff structure
@author: dpg
"""
from gerrychain.metrics import mean_median, efficiency_gap
import district_list as dl

def eg_gt_x(part,hi_eg, state, my_apportionment,my_electionproxy, i1):
    if efficiency_gap(part.state[my_electionproxy]) > hi_eg:
        eg_val = round(efficiency_gap(part.state[my_electionproxy]),3)
        fname = 'redist_data/example_districts/' + state + '_' + my_apportionment + '_' + \
        my_electionproxy +'_gt_' + str(i1)+ '_' + str(eg_val)
        dl.part_dump(part.state, fname) #dump out the district assignment data + GEOID10 tags etc. to file
    return
                     
                      
                      
    
def eg_zero_x(part,zero_eg, state, my_apportionment,my_electionproxy, i1):
    if abs(efficiency_gap(part.state[my_electionproxy])) < zero_eg:
        eg_val = round(efficiency_gap(part.state[my_electionproxy]),3)
        fname = 'redist_data/example_districts/' + state + '_' + my_apportionment + '_' + \
        my_electionproxy +'_eq_' + str(i1)+ '_' + str(eg_val)
        dl.part_dump(part.state, fname) #dump out the district assignment data + GEOID10 tags etc. to file
    return
            
    
def eg_lt_x(part,lo_eg, state, my_apportionment, my_electionproxy,i1):
     if efficiency_gap(part.state[my_electionproxy]) < lo_eg:
         eg_val = round(efficiency_gap(part.state[my_electionproxy]),3)
         fname = 'redist_data/example_districts/' + state + '_' + my_apportionment + '_' + \
         my_electionproxy +'_lt_' + str(i1)+ '_' + str(eg_val)
         dl.part_dump(part.state, fname) #dump out the district assignment data + GEOID10 tags etc. to file
     return
 
def eg_gt(part,hi_eg, state, my_apportionment,my_electionproxy, i1):
    if efficiency_gap(part[my_electionproxy]) > hi_eg:
        eg_val = round(efficiency_gap(part[my_electionproxy]),3)
        fname = 'redist_data/example_districts/' + state + '_' + my_apportionment + '_' + \
        my_electionproxy +'_gt_' + str(i1)+ '_' + str(eg_val)
        dl.part_dump(part, fname) #dump out the district assignment data + GEOID10 tags etc. to file
    return
                     
                      
                      
    
def eg_zero(part,zero_eg, state, my_apportionment,my_electionproxy, i1):
    if abs(efficiency_gap(part[my_electionproxy])) < zero_eg:
        eg_val = round(efficiency_gap(part[my_electionproxy]),3)
        fname = 'redist_data/example_districts/' + state + '_' + my_apportionment + '_' + \
        my_electionproxy +'_eq_' + str(i1)+ '_' + str(eg_val)
        dl.part_dump(part, fname) #dump out the district assignment data + GEOID10 tags etc. to file
    return
            
    
def eg_lt(part,lo_eg, state, my_apportionment, my_electionproxy,i1):
     if efficiency_gap(part[my_electionproxy]) < lo_eg:
         eg_val = round(efficiency_gap(part[my_electionproxy]),3)
         fname = 'redist_data/example_districts/' + state + '_' + my_apportionment + '_' + \
         my_electionproxy +'_lt_' + str(i1)+ '_' + str(eg_val)
         dl.part_dump(part, fname) #dump out the district assignment data + GEOID10 tags etc. to file
     return
                       