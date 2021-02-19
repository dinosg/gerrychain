#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 11:07:44 2020
script to define constants for file read-in and computation as below
@author: dinos
"""

my_apportionment = "SEND"    #type of district boundaries to calculate - eg US congressional, state senate, house etc.
my_electionproxy = "PRES16"           #pick the election to use as a statewide proxy for partisan voting for districted seats

my_electionproxy_alternate = "USS"
#my_electiondatafile = "./PA-shapefiles-master/PA_VTDs.json"   #PATH to the election data
my_electiondatafile ='./shapefiles_multistate/MA-shapefiles-master/MA_precincts_12_16/MA_precincts12_16_county_buffered.json'
#json file bc had to de-island :-(
state = "MA"
maxsplitlist=[60, 50, 40, 30, 25]
cutedgemaxlist  = [2,2,1.2,1.2,1.2]
poptol=0.06
