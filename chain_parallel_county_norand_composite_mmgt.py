#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 16:47:51 2020
Parallel version of chain run set up for Pennsylvania.
Some nice stuff added to DataFrame structure to add congressional district labels in order of actual increasing congressional district No.
@author: dinos
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 16:55:12 2020
uses recom proposal
@author: dpg
"""
#from multiprocessing import Pool
from multiprocessing import set_start_method, freeze_support
#from multiprocessing import Pool
from multiprocessing import get_context

import matplotlib.pyplot as plt
import time
from gerrychain import (GeographicPartition, Partition, Graph, MarkovChain_xtendedmmgt,
                        proposals, updaters, constraints, accept, Election)
from gerrychain.proposals import recom
from gerrychain.tree import recursive_tree_part
from functools import partial
from gerrychain.constraints import single_flip_contiguous, contiguous

import pandas
import pandas as pd
import numpy as np
from gerrychain.metrics import mean_median, efficiency_gap, polsby_popper
from get_districtlabels import get_labels, get_labels_comp
from get_electioninfo import get_elections
import random
import os 
from total_splits import total_splits
import district_list as dl
import conditional_dump as cd

def multichain_run(i1, graph, chainlength, my_apportionment, poptol, my_electionproxy, composite, rsw, rmm, reg, rpp, datastruct, state, splitno, maxsplits, cutedgemax):
    hi_mm = -.02#spit out maps for anything with efficiency gap over this
    #cutedgemax=1.2 #factor above initial partition, cut edges allowed 
    random.seed(os.urandom(10)*i1) 
#    poptol = 0.03  #min population deviation
    elections, composite = get_elections(state)
    
    if "TOTPOP" in graph._node[0]:
        popkey = "TOTPOP"
    elif "PERSONS" in graph._node[0]:
        popkey = "PERSONS"
    else:
        popkey = []
        print("woops no popkey in file, look @ graph_PA._node[0] to figure out what the keyword for population is\n")
#CONFIGURE UPDATERS
#We want to set up updaters for everything we want to compute for each plan in the ensemble.


# Population updater, for computing how close to equality the district
# populations are. "TOTPOP" is the population column from our shapefile.
    my_updaters = {"population": updaters.Tally(popkey, alias="population")}
    contiguous_parts = lambda p: contiguous(p)

# Election updaters, for computing election results using the vote totals
# from our shapefile.
    election_updaters = {election.name: election for election in elections}
    my_updaters.update(election_updaters)


#INITIAL PARTITION
    initial_partition = GeographicPartition(graph, assignment=my_apportionment, updaters=my_updaters)
    
    #this block obtains the Congressional District Labels and converts to string labels, cds
    ideal_population = sum(list(initial_partition["population"].values())) / len(initial_partition)
    cds = get_labels_comp(initial_partition, composite) #get congressional district labels

    nparts = len(initial_partition)
    print(nparts)
    #ranpart = recursive_tree_part(graph, range(nparts), ideal_population, popkey,poptol - .01,node_repeats=1)
    #randpartition = GeographicPartition(graph,assignment = ranpart, updaters = my_updaters)
    

    pop_constraint = constraints.within_percent_of_ideal_population(initial_partition, poptol)
    proposal = partial(recom,
                   pop_col=popkey,
                   pop_target=ideal_population,
                   epsilon=poptol,
                   node_repeats=2
                  )

    compactness_bound = constraints.UpperBound(
    lambda p: len(p["cut_edges"]),
    cutedgemax*len(initial_partition["cut_edges"])
    )
    chain = MarkovChain_xtendedmmgt(
    proposal=proposal,
    constraints=[ contiguous_parts,
        pop_constraint,
        compactness_bound],
    accept=accept.always_accept,
    initial_state= initial_partition, #randpartition,
    total_steps=chainlength,
    my_electionproxy = my_electionproxy,
    maxsplits = maxsplits
    )
    for part in chain:
        if (part.good == 1) or (part.good == -1):
            datax = np.zeros((nparts,1))  #nparts = ndistricts
            rsw_tmp = 0
            rmm_tmp = 0
            reg_tmp = 0
            
            
            for compelection in composite:
                rsw_tmp += part.state[compelection].wins("Democratic")
                rmm_tmp += mean_median(part.state[compelection])
                reg_tmp += efficiency_gap(part.state[compelection])
                datax += pandas.DataFrame(sorted(part.state[compelection].percents("Democratic" )), index=cds)
                
    
            rsw_tmp = rsw_tmp/len(composite) #now get average per election instead of sum over all elections
            rmm_tmp = rmm_tmp/len(composite)
            reg_tmp = reg_tmp/len(composite)
            
            datax = datax.transpose() / len(composite)
    #        rpp.append(np.mean(pd.Series(polsby_popper(part.state))))  #depends on geometry of the partition only not on vote outcomes
            rsw.append(rsw_tmp)
            rmm.append(rmm_tmp)
            reg.append(reg_tmp)
            datastruct = pandas.concat([datastruct, datax])
            splitno.append(total_splits(part.state))   #splits don't depend on individual election results, only on partition so not in loop
            cd.cd_gt(part.state,hi_mm,rmm_tmp ,state, my_apportionment,my_electionproxy, i1, '_cdgt')
            if (part.good == -1) or (part.good == 1):
                mmval = mean_median(part.state[my_electionproxy])
                print('worker ', i1, 'mm valued = ' , mmval)
                cd.mm_gt(part.state,hi_mm-.3, state, my_apportionment,my_electionproxy, i1, '_mmgt')
            if i1 == 1:
                print(i1, ' finished chain step ', part.counter)
            #cd.eg_zero(part,zero_eg, state, my_apportionment, my_electionproxy, i1)
    return i1, rsw, rmm, reg, rpp, datastruct, splitno           

#MAIN PROGRAM HERE:
    #few key lines for making parallel pool not mess up (freeze_support() and __spec__ definition)
if __name__ == '__main__':
    freeze_support()
    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
    dontfeedin = 0 #if set=0, feeds in data, otherwise skip
    poolsize=40
    chainlength=15000
    corrlength=50
    #maxsplits=210

 
    
      
        #    set_start_method("spawn")
        #    set_start_method("spawn")
    #my_apportionment = "ASM"    #type of district boundaries to calculate - eg US congressional, state senate, house etc.
    #my_electionproxy = "SEN16"           #pick the election to use as a statewide proxy for partisan voting for districted seats
    #my_electionproxy_alternate ="USS12"  #alternate name, see 'elections' variable below
    #my_electiondatafile = "./PA-shapefiles-master/PA_VTDs.json"   #PATH to the election data
    #my_electiondatafile  = "./shapefiles_multistate/WI-shapefiles-master/WI_wards_12_16/WI_ltsb_corrected_final.json"
    
    #state = "WI"
    proposaltype = "recom"
    #exec(open("input_templates/PA_HDIST_SEN12_assignment_y.py").read()) 
    #exec(open("input_templates/PA_SEND_SEN12_countyloop.py").read()) 
    
    #exec(open("input_templates/PA_CD_2011_SEN12.py").read()) 
    #exec(open("input_templates/MI_SENDIST_PRES16.py").read()) 
    #exec(open("input_templates/PA_CD_2011_SEN12.py").read()) 
    #exec(open("input_templates/PA_REMEDIAL_SEN12.py").read()) 
#    exec(open("input_templates/PA_CD_2011_SEN12_countyloop.py").read()) 
   # exec(open("input_templates/PA_SEND_SEN12_countyloop.py").read()) 
    #exec(open("input_templates/PA_districtr17shrinkmm-006.py").read()) 
    exec(open("input_templates/PA_districtr17shrink1.py").read()) 
    countysp = 'xsplitsrand ' +str(maxsplits)  #labels for graphs and output filenames
    normalize=''
    elections, composite = get_elections(state)
    #read in data file here:
   
    if 'dontfeedin' in globals():
        if dontfeedin == 0 or not( 'graph_PA' in globals()):
            if ".json" in my_electiondatafile:
                graph_PA = Graph.from_json(my_electiondatafile)
            else:
                graph_PA = Graph.from_file(my_electiondatafile)
    else:
        if ".json" in my_electiondatafile:
            graph_PA = Graph.from_json(my_electiondatafile)
        else:
            graph_PA = Graph.from_file(my_electiondatafile)
   
    
    #SETUP initial_partition & get initial DataFrame here - redundant but needed to setup datastruct
    #in parallel - 0th point resu, then append to it
    # 
    if 'poptol' not in globals():
        poptol = 0.05
    if "TOTPOP" in graph_PA._node[0]:
        popkey = "TOTPOP"
    elif "PERSONS" in graph_PA._node[0]:
        popkey = "PERSONS"
    else:
        popkey = []
        print("woops no popkey in file, look @ graph_PA._node[0] to figure out what the keyword for population is\n")
    #CONFIGURE UPDATERS
    #We want to set up updaters for everything we want to compute for each plan in the ensemble.
    
    
    # Population updater, for computing how close to equality the district
    # populations are. "TOTPOP" is the population column from our shapefile.
    
    my_updaters = {"population": updaters.Tally(popkey, alias="population")}
    
    election_updaters = {election.name: election for election in elections}
    my_updaters.update(election_updaters)
    
    initial_partition = GeographicPartition(graph_PA, assignment=my_apportionment, updaters=my_updaters)
    num_districts = len(initial_partition)
    cds = get_labels_comp(initial_partition, composite) #get congressional district labels
    #RUNNING THE CHAIN
    ideal_population = sum(list(initial_partition["population"].values())) / len(initial_partition)
    t0=time.time()
    
    # This will take about 10 minutes.
    #setup variables
    rsw = [[0 for x in range(1)] for x in range(poolsize)] #  np.zeros([poolsize, chainlength])
    rmm = [[0 for x in range(1)] for x in range(poolsize)] # np.zeros([poolsize, chainlength])
    reg = [[0 for x in range(1)] for x in range(poolsize)] # np.zeros([poolsize, chainlength])
    rpp = [[0 for x in range(1)] for x in range(poolsize)] # np.zeros([poolsize, chainlength])
    splitno = [[0 for x in range(1)] for x in range(poolsize)] 
    data1 = np.zeros((1,num_districts))
    for compelection in composite:
        data1  += initial_partition[compelection].percents("Democratic") 

    data1 = data1/len(composite)
    data1 = pd.DataFrame(sorted(list(data1)), columns=cds)
    datastruct = []
    #setup parallel list of DataFrames
    for nn in range(poolsize):
        datastruct.append(data1)
    ctx = get_context("spawn")
    p = ctx.Pool(poolsize)
    print('starting parallel runs\n')
    updated_vals = p.starmap(multichain_run, [(i1, graph_PA, chainlength, my_apportionment, poptol, my_electionproxy, composite,
                                               rsw[i1], rmm[i1], reg[i1], rpp[i1], datastruct[i1], state, splitno[i1], maxsplits, cutedgemax) for i1 in range(poolsize)])
    
    for i1, rsw_updated, rmm_updated, reg_updated, rpp_updated, datastruct_updated, splitno_updated in updated_vals:
        rsw[i1] = rsw_updated
        rmm[i1] = rmm_updated
        reg[i1] = reg_updated
        rpp[i1] = rpp_updated
        datastruct[i1] = datastruct_updated
        splitno[i1] = splitno_updated
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
    
    iter1 = range(corrlength-1,corrlength+chainlength-1,corrlength)   #since the correlation length is 200, only collect every 200th point
    reg_clean = []
    rmm_clean = []
    rsw_clean = []
    rpp_clean = []
    splitno_clean = []
    for nn in range(poolsize):
        for kk in iter1: 
            reg_clean.append(reg[nn][kk]) 
            rmm_clean.append(rmm[nn][kk]) 
            rsw_clean.append(rsw[nn][kk])
    #        rpp_clean.append(rpp[nn][kk])
            splitno_clean.append(splitno[nn][kk])
                 
    #data1 = data1.transpose()
    #data1 = pandas.DataFrame((initial_partition["SEN12"].percents("Democratic") ))
    t1=time.time()
    print( (t1-t0)/60, " min runtime\n")
    exec(open("condense_datastruct.py").read()) 
    # RUN condense_datastruct.py after this to unpack the data structure and plot it