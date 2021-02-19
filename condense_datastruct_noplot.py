#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 12:41:33 2020
reduce datastruct to a new, condesed subarray containing the uncorrelated data (around every 100 - 200 rows)
@author: dinos
"""
import time

import pandas as pd
import backup_chain as bc


data_condensed = pd.DataFrame([]) #null dataframe to start
threadcount = len(datastruct) #depth of datastruct list object
skipno = 100  #
for ii in range(threadcount):
    data_x = datastruct[ii]
    data_x.columns = cds
    sx = data_x.shape
    sx0 = sx[0]  #this is the # of iterations per dataframe... loop thru these skipping every 100- 200
    data_x.index = range(sx0)
    indexer = range(skipno, sx0+ skipno-1, skipno)  #collect data from these rows
    for kk in indexer:
        data_condensed= pd.concat([data_condensed,data_x[kk:kk+1]])
      
        
if 'postfix' not in globals():
    postfix = ''
outname = "redist_data/" + state + "_" + my_apportionment + "_" + my_electionproxy + "x" + str(chainlength)+ "x" + str(poolsize) + normalize + postfix
bc.save1(outname,data_condensed, reg_clean, rmm_clean, rsw_clean, reg, rmm, rsw)
print(t1-t0)