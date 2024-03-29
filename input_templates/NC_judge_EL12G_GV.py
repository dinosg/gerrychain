#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 11:07:44 2020
script to define constants for file read-in and computation as below
@author: dinos
"""

my_apportionment = "judge"    #type of district boundaries to calculate - eg US congressional, state senate, house etc.
my_electionproxy = "EL12G_GV_"           #pick the election to use as a statewide proxy for partisan voting for districted seats
my_electiondatafile = "./shapefiles_multistate/NC-shapefiles-master/NC_VTD/NC_VTDb.shp"   #PATH to the election data
#my_electiondatafile ="./shapefiles_multistate/WI-shapefiles-master/WI_wards_12_16/WI_ltsb_corrected_final.json"
state = "NC"
my_electionproxy_alternate="EL12G_GV_"
poptol=0.02
