#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 16:55:12 2020
uses recom proposal
@author: dpg

"""

import matplotlib.pyplot as plt
from gerrychain import (GeographicPartition, Partition, Graph, MarkovChain,
                        proposals, updaters, constraints, accept, Election)
from gerrychain.proposals import (recom, propose_random_flip)
from functools import partial
from gerrychain.constraints import single_flip_contiguous
from gerrychain.accept import always_accept
import pandas
from gerrychain.metrics import mean_median, efficiency_gap, polsby_popper
from strcmp_matlab import strfilter
import time
from norm_50 import norm_data
from get_districtlabels import get_labels, get_labels_comp
from get_electioninfo import get_elections
from gerrychain.tree import recursive_tree_part
import backup_chain as bc
import conditional_dump as cd
import numpy as np
import pandas as pd
#SET CONSTANTS HERE:
hi_eg = 0.945  #spit out maps for anything with efficiency gap over this
dontfeedin = 1  #if set=0, feeds in data, otherwise skip

markovchainlength = 5000  #length of Markov chain
proposaltype = "recom"
#exec(open("input_templates/WI_SEN_SEN16.py").read()) 
#exec(open("input_templates/PA_CD_2011_SEN12.py").read()) 

#exec(open("input_templates/MI_HDIST_PRES16.py").read()) 

#
#exec(open("input_templates/WI_SEN_SEN16.py").read()) 
#exec(open("input_templates/PA_CD_2011_SEN12.py").read())
#exec(open("input_templates/PA_CD_2011_SEN12.py").read())  
exec(open("input_templates/WI_SEN_SEN16_countyloop.py").read()) #read in input template
#exec(open("input_templates/NC_judge_EL12G_GV.py").read()) 
elections, composite = get_elections(state)

if 'poptol' not in globals():
        poptol = 0.03

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
     
t0=time.time()
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
## for TX and PA:
#my_updaters = {"population": updaters.Tally("TOTPOP", alias="population")}

##for WI:
my_updaters = {"population": updaters.Tally(popkey, alias="population")}

# Election updaters, for computing election results using the vote totals
# from our shapefile.
election_updaters = {election.name: election for election in elections}
my_updaters.update(election_updaters)


#INITIAL PARTITION
#initial_partition, graph_PA, my_updaters = norm_data(graph_PA, my_updaters, "CD_2011", "SEN12", "USS12")
initial_partition = GeographicPartition(graph_PA, assignment=my_apportionment, updaters=my_updaters)
cds = get_labels_comp(initial_partition,composite) #get congressional district labels

#SETUP MARKOV CHAIN PROPOSAL W RECOM
# The ReCom proposal needs to know the ideal population for the districts so that
# we can improve speed by bailing early on unbalanced partitions.
#ideal_population = sum(initial_partition["population"].values()) / len(initial_partition)
num_districts = len(initial_partition)  #the # of districts
ideal_population = sum(list(initial_partition["population"].values())) / num_districts

# We use functools.partial to bind the extra parameters (pop_col, pop_target, epsilon, node_repeats)
# of the recom proposal.
#TX & PA:

#WI:
if "recom" in proposaltype:
    proposal = partial(recom,
                       pop_col=popkey,
                       pop_target=ideal_population,
                       epsilon=poptol,
                       node_repeats=2
                      )

#CONSTRAINTS
    compactness_bound = constraints.UpperBound(
        lambda p: len(p["cut_edges"]),
        2*len(initial_partition["cut_edges"])
        )
    
    pop_constraint = constraints.within_percent_of_ideal_population(initial_partition, poptol)
    nparts = len(initial_partition)
    
#CONFIGURE MARKOV CHAIN
    ranpart = recursive_tree_part(graph_PA, range(nparts), ideal_population, popkey, poptol/2,node_repeats=1)
    
    randpartition = GeographicPartition(graph_PA,assignment = ranpart, updaters = my_updaters)
   # exec(open("partition_clean.py").read()) 
    chain = MarkovChain(
        proposal=proposal,
        constraints=[
            pop_constraint,
            compactness_bound
        ],
        accept=accept.always_accept,
        initial_state= randpartition,        #initial_state=initial_partition,
        total_steps=markovchainlength
    )
else:  #random flip
    nparts = len(initial_partition)
    ranpart = recursive_tree_part(graph_PA, range(nparts), ideal_population, popkey,poptol-0.02,node_repeats=1)
    randpartition = GeographicPartition(graph_PA,assignment = ranpart, updaters = my_updaters)
    chain = MarkovChain(
        proposal=propose_random_flip,
        constraints=[single_flip_contiguous],
        accept=always_accept,
        initial_state=randpartition,
        total_steps=markovchainlength
    )
"""
#this version shows a progress bar (maybe)
data = pandas.datarame(
    sorted(partition["SEN12"].percents("Democratic"))
    for partition in chain.with_progress_bar()
)
"""
# This will take about 10 minutes.

# This will take about 10 minutes.
rsw = []
rmm = []
reg = []
rpp = []
data1 = np.zeros((1,num_districts))
for compelection in composite:
    data1  += initial_partition[compelection].percents("Democratic") 

data1 = data1/len(composite)


data1 = pd.DataFrame(np.sort(data1).transpose(), columns=cds)


#loop over each markov chain iteration
for part in chain:
    #reset each counter before looping over each election in composite
    datax = np.zeros((num_districts,1))
    rsw_tmp = 0
    rmm_tmp = 0
    reg_tmp = 0
    for compelection in composite:
        rsw_tmp += part[compelection].wins("Democratic")
        rmm_tmp += mean_median(part[compelection])
        reg_tmp += efficiency_gap(part[compelection])
        datax += pandas.DataFrame(sorted(part[compelection].percents("Democratic" )), index=cds)
        
    rsw_tmp = rsw_tmp/len(composite) #now get average per election instead of sum over all elections
    rmm_tmp = rmm_tmp/len(composite)
    reg_tmp = reg_tmp/len(composite)
    datax = datax.transpose() / len(composite)
 #   rpp.append(np.mean(pd.Series(polsby_popper(part))))  #depends on geometry of the partition only not on vote outcomes
    rsw.append(rsw_tmp)
    rmm.append(rmm_tmp)
    reg.append(reg_tmp)
    
    #datax = datax.transpose()

    data1 = pandas.concat([data1, datax])
    #
    #this line checks to see if efficiency gap fills some criteria, if so dump assignments & identifiers to file
    #cd.eg_gt(part,hi_eg, state, my_apportionment,my_electionproxy, 0)


fig, ax = plt.subplots(figsize=(8, 6))

# Draw 50% line
ax.axhline(0.5, color="#cccccc")

# Draw boxplot
data1.boxplot(ax=ax, positions=range(len(data1.columns)))

# Draw initial plan's Democratic vote %s (.iloc[0] gives the first row)
plt.plot(np.array(data1.iloc[0]), "ro")

# Annotate
titlestr = state + " " + my_apportionment + "  x" + str(markovchainlength)
ax.set_title(titlestr)
ax.set_ylabel("Democratic vote % " + my_electionproxy)
ax.set_xlabel("Sorted districts")
ax.set_ylim(0, 1)
ax.set_yticks([0, 0.25, 0.5, 0.75, 1])

plt.show()
# NORMALIZE AND REDO at 50% per each party



 
t1=time.time()
print((t1 - t0)/60 ," min runtime\n")
outname = "redist_data/" + state + "_" + my_apportionment + "_" + my_electionproxy + "x" + str(markovchainlength)
bc.save(outname,data1, reg, rmm, rsw, rpp)

