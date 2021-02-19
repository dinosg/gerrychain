#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 11:07:44 2020
script to define constants for file read-in and computation as below
@author: dinos
"""

my_apportionment = "CD_2011"    #type of district boundaries to calculate - eg US congressional, state senate, house etc.
my_electionproxy = "SEN12"           #pick the election to use as a statewide proxy for partisan voting for districted seats
my_electiondatafile = "./PA-shapefiles-master/PA_VTDs/PA_VTD_PLANS.shp"   #PATH to the election data
#my_electiondatafile = "./PA-shapefiles-master/PA_VTDs.json"   #PATH to the election data
#my_electiondatafile ="./shapefiles_multistate/WI-shapefiles-master/WI_wards_12_16/WI_ltsb_corrected_final.json"
state = "PA"
my_electionproxy_alternate="USS12"
maxsplitlist=[ 70, 50, 30, 20, 17]
cutedgemaxlist  = [2,2,2,1.2,1.2]
poptol=0.02

