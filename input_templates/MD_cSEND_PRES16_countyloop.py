#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 11:07:44 2020
script to define constants for file read-in and computation as below
@author: dinos
"""

my_apportionment = "cSEND"    #type of district boundaries to calculate - eg US congressional, state senate, house etc.
my_electionproxy = "PRES16"           #pick the election to use as a statewide proxy for partisan voting for districted seats

my_electionproxy_alternate = "USS"
#my_electiondatafile = "./PA-shapefiles-master/PA_VTDs.json"   #PATH to the election data
my_electiondatafile ='./shapefiles_multistate/MD-shapefiles-master/MD_precincts/MD_precincts_csen_buf.json'
#json file bc had to de-island :-(
state = "MD"
#maxsplitlist=[80, 60, 50, 45, 43]
maxsplitlist=[42, 40, 38, 36, 34]
cutedgemaxlist  = [2,2,2,1.2,1.2]
poptol=0.06
