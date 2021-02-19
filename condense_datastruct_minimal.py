#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 12:41:33 2020
reduce datastruct to a new, condesed subarray containing the uncorrelated data 
since every data is from a new random, uncorrelated matrix we're taking all the data points - no skipping
@author: dinos
"""
import time
import matplotlib.pyplot as plt
import pandas as pd
import backup_chain as bc


data_condensed = pd.DataFrame([]) #null dataframe to start
threadcount = len(datastruct) #depth of datastruct list object
skipno = 1  # basically, don't skip b/c
for ii in range(threadcount):
    data_x = datastruct[ii]
    data_x.columns = cds
    sx = data_x.shape
    sx0 = sx[0]  #this is the # of iterations per dataframe... loop thru these skipping every 100- 200
    data_x.index = range(sx0)
 #   indexer = range(skipno-1, sx0+ skipno-1, skipno)  #collect data from these rows
    indexer = range(sx0)
    for kk in indexer:
        if rsw[ii][kk] > -1:   #skip over workers that timed out
            data_condensed= pd.concat([data_condensed,data_x[kk:kk+1]])
if 'postfix' not in globals():
    postfix = ''      
outname = "redist_data/" + state + "_" + my_apportionment + "_" + my_electionproxy + "x" + \
    str(chainlength)+ "x" + str(poolsize) + normalize + postfix
bc.save1(outname,data_condensed, reg_clean, rmm_clean, rsw_clean, reg, rmm, rsw)
print(t1-t0, "seconds\n")       
plt.figure()
fig, ax = plt.subplots(figsize=(8, 6))

# Draw 50% line
ax.axhline(0.5, color="#cccccc")

# Draw boxplot
#data1.boxplot(ax=ax, positions=range(len(data1.columns)))
data_condensed.boxplot(positions=range(len(data_condensed.columns)))
# Draw initial plan's Democratic vote %s (.iloc[0] gives the first row)
plt.plot(sorted(data1.iloc[0]), "ro")

# Annotate
titlestr = state + " " + my_apportionment + "  x" + str(chainlength) + " x" + str(poolsize) + normalize
ax.set_title(titlestr)
ax.set_ylabel("Democratic vote % " + my_electionproxy)
ax.set_xlabel("Sorted districts")
ax.set_ylim(0, 1)
ax.set_yticks([0, 0.25, 0.5, 0.75, 1])

plt.show()
