#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 16:47:51 2020

@author: dinos

this version normalizes initial partition to 50% dem /republican

Some nice stuff added to DataFrame structure to add congressional district labels in order of actual increasing congressional district No.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

Created on Tue Mar 24 16:55:12 2020
uses recom proposal
@author: dpg
"""
from multiprocessing import Pool
import matplotlib.pyplot as plt
import time
from gerrychain import (GeographicPartition, Partition, Graph, MarkovChain,
                        proposals, updaters, constraints, accept, Election)
from gerrychain.proposals import recom
from functools import partial
from strcmp_matlab import strfilter
import pandas
import numpy as np
from gerrychain.metrics import mean_median, efficiency_gap
from get_districtlabels import get_labels
from norm_50 import norm_data
 
def multichain_run(i1, graph, chainlength, my_apportionment, my_electionproxy, my_electionproxy_alternate, rsw, rmm, reg, datastruct):
    
    elections = [
    Election("SEN10", {"Democratic": "SEN10D", "Republican": "SEN10R"}),
    Election("SEN12", {"Democratic": "USS12D", "Republican": "USS12R"}),
    Election("SEN16", {"Democratic": "T16SEND", "Republican": "T16SENR"}),
    Election("PRES12", {"Democratic": "PRES12D", "Republican": "PRES12R"}),
    Election("PRES16", {"Democratic": "T16PRESD", "Republican": "T16PRESR"})
    ]
    my_updaters = {"population": updaters.Tally("TOTPOP", alias="population")}

# Election updaters, for computing election results using the vote totals
# from our shapefile.
    election_updaters = {election.name: election for election in elections}
    my_updaters.update(election_updaters)


#INITIAL PARTITION
    initial_partition, graph, my_updaters = norm_data(graph, my_updaters, my_apportionment, my_electionproxy, my_electionproxy_alternate)
    
    #this block obtains the Congressional District Labels and converts to string labels, cds
    
    cds = get_labels(initial_partition, my_electionproxy) #get congressional district labels
    ideal_population = sum(list(initial_partition["population"].values())) / len(initial_partition)
        
    pop_constraint = constraints.within_percent_of_ideal_population(initial_partition, 0.02)
    proposal = partial(recom,
                   pop_col="TOTPOP",
                   pop_target=ideal_population,
                   epsilon=0.02,
                   node_repeats=2
                  )

    compactness_bound = constraints.UpperBound(
    lambda p: len(p["cut_edges"]),
    2*len(initial_partition["cut_edges"])
    )
    chain = MarkovChain(
    proposal=proposal,
    constraints=[
        pop_constraint,
        compactness_bound],
    accept=accept.always_accept,
    initial_state=initial_partition,
    total_steps=chainlength
    )
    for part in chain:
        rsw.append(part[my_electionproxy].wins("Democratic"))
        rmm.append(mean_median(part[my_electionproxy]))
        reg.append(efficiency_gap(part[my_electionproxy]))
        datax = pandas.DataFrame(sorted(part[my_electionproxy].percents("Democratic" )), index=cds)
        datax = datax.transpose()
    #    data1 = pandas.concat([data1, pandas.DataFrame(part["SEN12"].percents("Democratic" ))],axis=1)
        datastruct = pandas.concat([datastruct, datax])
    return i1, rsw, rmm, reg, datastruct           


#DEFINE CONSTANTS:
poolsize=40
chainlength=100

my_apportionment = "CD_2011"    #type of district boundaries to calculate - eg US congressional, state senate, house etc.
my_electionproxy = "SEN12"           #pick the election to use as a statewide proxy for partisan voting for districted seats
my_electionproxy_alternate ="USS12"  #alternate name, see 'elections' variable below
my_electiondatafile = "./PA-shapefiles-master/PA_VTDs.json"   #PATH to the election data

proposaltype = "recom"



if ".json" in my_electiondatafile:
    graph_PA = Graph.from_json(my_electiondatafile)
else:
    graph_PA = Graph.from_file(my_electiondatafile)
    

elections = [
    Election("SEN10", {"Democratic": "SEN10D", "Republican": "SEN10R"}),
    Election("SEN12", {"Democratic": "USS12D", "Republican": "USS12R"}),
    Election("SEN16", {"Democratic": "T16SEND", "Republican": "T16SENR"}),
    Election("PRES12", {"Democratic": "PRES12D", "Republican": "PRES12R"}),
    Election("PRES16", {"Democratic": "T16PRESD", "Republican": "T16PRESR"})
]
#SETUP initial_partition & get initial DataFrame here - redundant but needed to setup datastruct
#in parallel - 0th point resu, then append to it
# 
my_updaters = {"population": updaters.Tally("TOTPOP", alias="population")}
election_updaters = {election.name: election for election in elections}
my_updaters.update(election_updaters)

initial_partition, graph_PA, my_updaters = norm_data(graph_PA, my_updaters, my_apportionment, my_electionproxy, my_electionproxy_alternate)
cds = get_labels(initial_partition, my_electionproxy) #get congressional district labels
#RUNNING THE CHAIN

t0=time.time()

# This will take about 10 minutes.
#setup variables
rsw = [[0 for x in range(1)] for x in range(poolsize)] #  np.zeros([poolsize, chainlength])
rmm = [[0 for x in range(1)] for x in range(poolsize)] # np.zeros([poolsize, chainlength])
reg = [[0 for x in range(1)] for x in range(poolsize)] # np.zeros([poolsize, chainlength])
data1 = pandas.DataFrame(sorted(initial_partition[my_electionproxy ].percents("Democratic") ), index=cds)
data1 = data1.transpose()
datastruct = []
#setup parallel list of DataFrames
for nn in range(poolsize):
    datastruct.append(data1)


p = Pool(poolsize)
updated_vals = p.starmap(multichain_run, [(i1, graph_PA, chainlength, my_apportionment, my_electionproxy, my_electionproxy_alternate,
                                           rsw[i1], rmm[i1], reg[i1], datastruct[i1]) for i1 in range(poolsize)])

for i1, rsw_updated, rmm_updated, reg_updated, datastruct_updated in updated_vals:
    rsw[i1] = rsw_updated
    rmm[i1] = rmm_updated
    reg[i1] = reg_updated
    datastruct[i1] = datastruct_updated
#clean up data
rsw_bak= rsw.copy()   #just to be on the safe side

reg_bak = reg.copy()

rmm_bak = rmm.copy()
datastruct_bak = datastruct.copy()
for nn in range(poolsize): #clean up since 1st value in each list is a junk '0'
    junk = rsw[nn].pop(0)
    junk = reg[nn].pop(0)
    junk = rmm[nn].pop(0)

iter1 = range(100-1,100+chainlength-1,100)   #since the correlation length is 200, only collect every 200th point
reg_clean = []
rmm_clean = []
rsw_clean = []
for nn in range(poolsize):
    for kk in iter1: 
        reg_clean.append(reg[nn][kk]) 
        rmm_clean.append(rmm[nn][kk]) 
        rsw_clean.append(rsw[nn][kk])           
             
#data1 = data1.transpose()
#data1 = pandas.DataFrame((initial_partition["SEN12"].percents("Democratic") ))
t1=time.time()
exec(open("condense_datastruct.py").read())    #run condense_datastruct.py as a script using this namespace
# RUN condense_datastruct.py after this to unpack the data structure and plot it