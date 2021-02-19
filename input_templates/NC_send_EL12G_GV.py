#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 11:07:44 2020
script to define constants for file read-in and computation as below
@author: dinos
"""

my_apportionment = "SEND"    #type of district boundaries to calculate - eg US congressional, state senate, house etc.
my_electionproxy = "EL12G_GV_"           #pick the election to use as a statewide proxy for partisan voting for districted seats
my_electiondatafile = "./shapefiles_multistate/NC-shapefiles-master/NC_VTD/NC_VTD_buf_SEND.shp"   #PATH to the election data

state = "NC"
my_electionproxy_alternate="EL12G_GV_"
maxsplitlist=[80, 50  , 30, 25, 23, 21,20]
cutedgemaxlist  = [2,2, 2, 1.2, 1.2, 1.2,1.2]
poptol=0.06
