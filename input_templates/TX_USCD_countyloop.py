#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 16:12:32 2020

@author: dinos
"""

maxsplitlist=[100,90,80, 70, 60, 55, 50 ]
cutedgemaxlist  = [2,2,2,1.2,1.2,1.2, 1.2, 1.2]



my_apportionment = "USCD"    #type of district boundaries to calculate - eg US congressional, state senate, house etc.
my_electionproxy = "SEN12"           #pick the election to use as a statewide proxy for partisan voting for districted seats
my_electionproxy_alternate = "SEN12"
#my_electiondatafile = "./PA-shapefiles-master/PA_VTDs.json"   #PATH to the election data
#my_electiondatafile ="./shapefiles_multistate/WI-shapefiles-master/WI_wards_12_16/WI_ltsb_corrected_final.json"
my_electiondatafile ="./shapefiles_multistate/TX_vtds/TX_vtds_x.shp"
state = "TX"
poptol =0.03
