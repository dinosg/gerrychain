#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 11:07:44 2020
script to define constants for file read-in and computation as below
@author: dinos
"""

my_apportionment = "SEND"    #type of district boundaries to calculate - eg US congressional, state senate, house etc.
my_electionproxy = "SEN16"           #pick the election to use as a statewide proxy for partisan voting for districted seats

my_electionproxy_alternate = "USS"
#my_electiondatafile = "./PA-shapefiles-master/PA_VTDs.json"   #PATH to the election data
my_electiondatafile ="./shapefiles_multistate/OH_precincts/ohio_precincts_a.json"
state = "OH"
poptol =0.06
