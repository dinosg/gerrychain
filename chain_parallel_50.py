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
from multiprocessing import set_start_method, freeze_support
#from multiprocessing import Pool
from multiprocessing import get_context

import matplotlib.pyplot as plt
import time
from gerrychain import (GeographicPartition, Partition, Graph, MarkovChain,
                        proposals, updaters, constraints, accept, Election)
from gerrychain.proposals import recom
from gerrychain.tree import recursive_tree_part
from functools import partial

import pandas
import numpy as np
import pandas as pd
from gerrychain.metrics import mean_median, efficiency_gap, polsby_popper
from get_districtlabels import get_labels
from norm_50 import norm_data
from get_electioninfo import get_elections
import random
import os 
import conditional_dump as cd
 
def multichain_run(i1, graph, chainlength, my_apportionment, poptol, my_electionproxy, my_electionproxy_alternate, rsw, rmm, reg, rpp, datastruct, state):
    
    random.seed(os.urandom(10)*i1) 
    hi_eg = 0.035
  #  poptol = 0.02  #min % population deviation per district
    elections, composite = get_elections(state)

    if "TOTPOP" in graph._node[0]:
        popkey = "TOTPOP"
    elif "PERSONS" in graph._node[0]:
        popkey = "PERSONS"
    else:
            popkey = []
            print("woops no popkey in file, look @ graph._node[0] to figure out what the keyword for population is\n")
#CONFIGURE UPDATERS
#We want to set up updaters for everything we want to compute for each plan in the ensemble.


# Population updater, for computing how close to equality the district
# populations are. "TOTPOP" is the population column from our shapefile.
    my_updaters = {"population": updaters.Tally(popkey, alias="population")}


# Election updaters, for computing election results using the vote totals
# from our shapefile.
    election_updaters = {election.name: election for election in elections}
    my_updaters.update(election_updaters)


#INITIAL PARTITION
    initial_partition, graph, my_updaters = norm_data(graph, my_updaters, my_apportionment, my_electionproxy, my_electionproxy_alternate, state)
    
    #this block obtains the Congressional District Labels and converts to string labels, cds
    
    cds = get_labels(initial_partition, my_electionproxy) #get congressional district labels
    nparts = len(initial_partition)
    ideal_population = sum(list(initial_partition["population"].values())) / len(initial_partition)
    ranpart = recursive_tree_part(graph, range(nparts), ideal_population, popkey,poptol-0.01,node_repeats=1)
    randpartition = GeographicPartition(graph,assignment = ranpart, updaters = my_updaters)
    
        
    pop_constraint = constraints.within_percent_of_ideal_population(initial_partition, poptol)
    proposal = partial(recom,
                   pop_col=popkey,
                   pop_target=ideal_population,
                   epsilon=poptol,
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
    initial_state=randpartition,
    total_steps=chainlength
    )
    for part in chain:
        rsw.append(part[my_electionproxy].wins("Democratic"))
        rmm.append(mean_median(part[my_electionproxy]))
        reg.append(efficiency_gap(part[my_electionproxy]))
  #      rpp.append(np.mean(pd.Series(polsby_popper(part))))  #depends on geometry of the partition only not on vote outcomes
        datax = pandas.DataFrame(sorted(part[my_electionproxy].percents("Democratic" )), index=cds)
        datax = datax.transpose()
    #    data1 = pandas.concat([data1, pandas.DataFrame(part["SEN12"].percents("Democratic" ))],axis=1)
        datastruct = pandas.concat([datastruct, datax])
        cd.eg_gt(part,hi_eg, state, my_apportionment,my_electionproxy, i1)
    return i1, rsw, rmm, reg, rpp, datastruct 
          
#MAIN PROGRAM HERE:
    #few key lines for making parallel pool not mess up (freeze_support() and __spec__ definition)
if __name__ == '__main__':
    freeze_support()
    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
    dontfeedin = 1  #if set=0, feeds in data, otherwise skip
    poolsize=40
    chainlength=1000
    normalize=' normalized'
#DEFINE CONSTANTS:
    dontfeedin = 0  #if set=0, feeds in data, otherwise skip
    
    exec(open("input_templates/PA_REMEDIAL_SEN12.py").read())  
   # my_electionproxy_alternate = my_electionproxy
    #for PA data:
    
    
    elections, composite = get_elections(state)
    
    
    if 'dontfeedin' in globals():
        if dontfeedin == 0 or not( 'graph' in globals()):
            if ".json" in my_electiondatafile:
                graph = Graph.from_json(my_electiondatafile)
            else:
                graph = Graph.from_file(my_electiondatafile)
    else:
        if ".json" in my_electiondatafile:
            graph = Graph.from_json(my_electiondatafile)
        else:
            graph = Graph.from_file(my_electiondatafile)
         
    if 'poptol' not in globals():
        poptol = 0.03
    if "TOTPOP" in graph._node[0]:
        popkey = "TOTPOP"
    elif "PERSONS" in graph._node[0]:
        popkey = "PERSONS"
    else:
        popkey = []
        print("woops no popkey in file, look @ graph._node[0] to figure out what the keyword for population is\n")
    #CONFIGURE UPDATERS
    #We want to set up updaters for everything we want to compute for each plan in the ensemble.
    
    
    # Population updater, for computing how close to equality the district
    # populations are. "TOTPOP" is the population column from our shapefile.
    my_updaters = {"population": updaters.Tally(popkey, alias="population")}
    
    election_updaters = {election.name: election for election in elections}
    my_updaters.update(election_updaters)
    
    #run chain ONCE to clean up graph and use primary election assignment name...
    #INITIAL PARTITION
    initial_partition = GeographicPartition(graph, assignment=my_apportionment, updaters=my_updaters)
    # initial_partition, graph, my_updaters = norm_data(graph, my_updaters, my_apportionment, my_electionproxy, my_electionproxy_alternate)
    # cds = get_labels(initial_partition, my_electionproxy) #get congressional district labels
    #RUNNING THE CHAIN
    ideal_population = sum(list(initial_partition["population"].values())) / len(initial_partition)
    
    # We use functools.partial to bind the extra parameters (pop_col, pop_target, epsilon, node_repeats)
    # of the recom proposal.
    
    
    t0=time.time()
    #now can do initial_partition and know my_electionproxy will be OK, won't need alternate
    initial_partition, graph, my_updaters = norm_data(graph, my_updaters, my_apportionment, poptol, my_electionproxy, my_electionproxy_alternate, state)
    cds = get_labels(initial_partition, my_electionproxy) #get congressional district labels
    # This will take about 10 minutes.
    #setup variables
    rsw = [[0 for x in range(1)] for x in range(poolsize)] #  np.zeros([poolsize, chainlength])
    rmm = [[0 for x in range(1)] for x in range(poolsize)] # np.zeros([poolsize, chainlength])
    reg = [[0 for x in range(1)] for x in range(poolsize)] # np.zeros([poolsize, chainlength])
    rpp = [[0 for x in range(1)] for x in range(poolsize)] # np.zeros([poolsize, chainlength])
    data1 = pandas.DataFrame(sorted(initial_partition[my_electionproxy ].percents("Democratic") ), index=cds)
    data1 = data1.transpose()
    datastruct = []
    #setup parallel list of DataFrames
    for nn in range(poolsize):
        datastruct.append(data1)
    
    #key defs for setting up parallel pool HERE:
    ctx = get_context("spawn")
    p = ctx.Pool(poolsize)
    updated_vals = p.starmap(multichain_run, [(i1, graph, chainlength, my_apportionment, my_electionproxy, my_electionproxy_alternate,
                                               rsw[i1], rmm[i1], reg[i1],rpp[i1], datastruct[i1], state) for i1 in range(poolsize)])
    
    for i1, rsw_updated, rmm_updated, reg_updated, datastruct_updated in updated_vals:
        rsw[i1] = rsw_updated
        rmm[i1] = rmm_updated
        reg[i1] = reg_updated
        rpp[i1] = rpp_updated
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
        junk = rpp[nn].pop(0)
    
    iter1 = range(100-1,100+chainlength-1,100)   #since the correlation length is 200, only collect every 200th point
    reg_clean = []
    rmm_clean = []
    rsw_clean = []
    rpp_clean = []
    for nn in range(poolsize):
        for kk in iter1: 
            reg_clean.append(reg[nn][kk]) 
            rmm_clean.append(rmm[nn][kk]) 
            rsw_clean.append(rsw[nn][kk])    
  #          rpp_clean.append(rpp[nn][kk])
                 
    #data1 = data1.transpose()
    #data1 = pandas.DataFrame((initial_partition["SEN12"].percents("Democratic") ))
    t1=time.time()
    exec(open("condense_datastruct.py").read())    #run condense_datastruct.py as a script using this namespace
    # RUN condense_datastruct.py after this to unpack the data structure and plot it