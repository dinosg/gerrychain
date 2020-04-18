#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 17:19:46 2020
returns the labels for election districts in order of how well the democratic party did in the_election
for example, in PA in the 2012 senate election, Congressional districts from low to high dem result were
9, 10, 5, 4, 3, 18, ...

where the_election is "SEN12"
@author: dinos
"""
from strcmp_matlab import strfilter
def get_labels(initial_partition, the_election):

    ipl=list(initial_partition["population"]) #extract the original congressional district Nos. in order listed
    subject = initial_partition[the_election].percents("Democratic") #get the vote % in order appearing in partition
    sortindex = sorted(range(len(subject)), key=subject.__getitem__) #get the index when you shuffle it through vote%-ordered sort
    congressdistrictlabels = strfilter(ipl, sortindex) #apply the index to district # labels in order appearing in partition
    #data.columns = congressdistrictlabels  #this step uses the original congressional district Nos RESHUFFLED by rank ordered vote%
    cds = []  #convert to string labels
    for nn in congressdistrictlabels:
        cds.append(str(nn))
    
    return cds