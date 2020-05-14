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
import backup_chain as bc
import matplotlib.pyplot as plt
import time
from gerrychain import (GeographicPartition, Partition, Graph, MarkovChain,
                        proposals, updaters, constraints, accept, Election)
from gerrychain.proposals import recom
from gerrychain.tree import recursive_tree_part
from functools import partial
from strcmp_matlab import strfilter
import pandas
import numpy as np
from gerrychain.metrics import mean_median, efficiency_gap
from get_districtlabels import get_labels
from get_electioninfo import get_elections
 
def multichain_run(i1, graph, chainlength, my_apportionment, my_electionproxy, my_electionproxy_alternate, rsw, rmm, reg, datastruct, state):
     
    poptol = 0.03  #min population deviation
    elections = get_elections(state)
    
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


# Election updaters, for computing election results using the vote totals
# from our shapefile.
    election_updaters = {election.name: election for election in elections}
    my_updaters.update(election_updaters)


#INITIAL PARTITION
    initial_partition = GeographicPartition(graph, assignment=my_apportionment, updaters=my_updaters)
    
    #this block obtains the Congressional District Labels and converts to string labels, cds
    ideal_population = sum(list(initial_partition["population"].values())) / len(initial_partition)
    cds = get_labels(initial_partition, my_electionproxy) #get congressional district labels

    nparts = len(initial_partition)
    ranpart = recursive_tree_part(graph, range(nparts), ideal_population, popkey,poptol - .01,node_repeats=1)
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
        datax = pandas.DataFrame(sorted(part[my_electionproxy].percents("Democratic" )), index=cds)
        datax = datax.transpose()
    #    data1 = pandas.concat([data1, pandas.DataFrame(part["SEN12"].percents("Democratic" ))],axis=1)
        datastruct = pandas.concat([datastruct, datax])
    return i1, rsw, rmm, reg, datastruct           

#MAIN PROGRAM HERE:
    #few key lines for making parallel pool not mess up (freeze_support() and __spec__ definition)
if __name__ == '__main__':
    freeze_support()
    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
    dontfeedin = 0  #if set=0, feeds in data, otherwise skip
    poolsize=40
    chainlength=4000
      
        #    set_start_method("spawn")
        #    set_start_method("spawn")
    #my_apportionment = "ASM"    #type of district boundaries to calculate - eg US congressional, state senate, house etc.
    #my_electionproxy = "SEN16"           #pick the election to use as a statewide proxy for partisan voting for districted seats
    #my_electionproxy_alternate ="USS12"  #alternate name, see 'elections' variable below
    #my_electiondatafile = "./PA-shapefiles-master/PA_VTDs.json"   #PATH to the election data
    #my_electiondatafile  = "./shapefiles_multistate/WI-shapefiles-master/WI_wards_12_16/WI_ltsb_corrected_final.json"
    
    #state = "WI"
    proposaltype = "recom"
    #exec(open("input_templates/PA_HDIST_SEN12.py").read()) 
    #exec(open("input_templates/PA_CD_2011_SEN12.py").read()) 
    exec(open("input_templates/WI_SEN_SEN16.py").read()) 
    elections = get_elections(state)
    #read in data file here:
    """
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
    """
    if ".json" in my_electiondatafile:
                graph_PA = Graph.from_json(my_electiondatafile)
    else:
                graph_PA = Graph.from_file(my_electiondatafile)
    #SETUP initial_partition & get initial DataFrame here - redundant but needed to setup datastruct
    #in parallel - 0th point resu, then append to it
    # 
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
    cds = get_labels(initial_partition, my_electionproxy) #get congressional district labels
    #RUNNING THE CHAIN
    ideal_population = sum(list(initial_partition["population"].values())) / len(initial_partition)
    t0=time.time()
    
    # This will take about 10 minutes.
    #setup variables
    rsw = [[0 for x in range(1)] for x in range(poolsize)] #  np.zeros([poolsize, chainlength])
    rmm = [[0 for x in range(1)] for x in range(poolsize)] # np.zeros([poolsize, chainlength])
    reg = [[0 for x in range(1)] for x in range(poolsize)] # np.zeros([poolsize, chainlength])
    data1 = pandas.DataFrame(sorted(initial_partition[my_electionproxy].percents("Democratic") ), index=cds)
    data1 = data1.transpose()
    datastruct = []
    #setup parallel list of DataFrames
    for nn in range(poolsize):
        datastruct.append(data1)
    ctx = get_context("spawn")
    p = ctx.Pool(poolsize)
        
    updated_vals = p.starmap(multichain_run, [(i1, graph_PA, chainlength, my_apportionment, my_electionproxy, my_electionproxy_alternate,
                                               rsw[i1], rmm[i1], reg[i1], datastruct[i1], state) for i1 in range(poolsize)])
    
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
    print( (t1-t0)/60, " min runtime\n")
    exec(open("condense_datastruct.py").read()) 
    # RUN condense_datastruct.py after this to unpack the data structure and plot it