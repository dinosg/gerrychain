#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 11:07:44 2020
script to define constants for file read-in and computation as below
@author: dinos
"""

my_apportionment = "SENDIST"    #type of district boundaries to calculate - eg US congressional, state senate, house etc.
my_electionproxy = "SEN16"           #pick the election to use as a statewide proxy for partisan voting for districted seats

my_electionproxy_alternate = "SEN16"
#my_electiondatafile = "./PA-shapefiles-master/PA_VTDs.json"   #PATH to the election data
my_electiondatafile ="./shapefiles_multistate/FL-shapefiles-master/ramsay_shapefilesFL/vtd_alldata_send/vtd_alldata_send.shp"
state = "FL"
#for Ramsay's file on vtds including pop (but no election results)
maxsplitlist=[120,110, 100]
cutedgemaxlist  = [2,2,2]
poptol =0.06

