#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 16:55:12 2020
normalizes PARTITIONS by 50% rep-dem, not individual VTD's and applies corrections to dataframe w/ election results
but does NOT apply normalization to other measures (wins, efficiency gap, mean-median)
uses recom proposal
@author: dpg
"""

import matplotlib.pyplot as plt
import backup_chain as bc
from gerrychain import (GeographicPartition, Partition, Graph, MarkovChain,
                       proposals, updaters, constraints, accept, Election)
from gerrychain.proposals import (recom, propose_random_flip)
from gerrychain.constraints import single_flip_contiguous
from functools import partial
import pandas
from gerrychain.metrics import mean_median, efficiency_gap, polsby_popper
from strcmp_matlab import strfilter
import time
from norm_50 import norm_data
from get_districtlabels import get_labels
from get_electioninfo import get_elections
from gerrychain.tree import recursive_tree_part
from norm_50_partition import norm_data_part 
import numpy as np
import pandas as pd


#SET CONSTANTS HERE:
#dontfeedin = 1  #if set=0, feeds in data, otherwise skip
my_apportionment = "CD_2011"  #"CD_2011"    #type of district boundaries to calculate - eg US congressional, state senate, house etc.
my_electionproxy = "SEN12"           #pick the election to use as a statewide proxy for partisan voting for districted seats

#my_electiondatafile = "./shapefiles_multistate/TX_vtds/TX_vtds_x.shp"  #"./PA-shapefiles-master/PA_VTDs.json"   #PATH to the election data
#my_electiondatafile  = "./shapefiles_multistate/WI-shapefiles-master/WI_wards_12_16/WI_ltsb_corrected_final.json"
my_electiondatafile = "./PA-shapefiles-master/PA_VTDs.json"   #PATH to the election data
markovchainlength = 1000  #length of Markov chain
proposaltype = "recom"
state = "PA"
if 'poptol' not in globals():
        poptol = 0.03
elections, composite = get_elections(state)
if 'dontfeedin' in globals():
    if dontfeedin == 0 or not( 'graph_PA' in globals()):
        if ".json" in my_electiondatafile:
            graph_PA = Graph.from_json(my_electiondatafile)
        else:
            graph_PA = Graph.from_file(my_electiondatafile)
else:
    print("reading in data:\n")
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
my_updaters = {"population": updaters.Tally(popkey, alias="population")}

# Election updaters, for computing election results using the vote totals
# from our shapefile.
election_updaters = {election.name: election for election in elections}
my_updaters.update(election_updaters)


#INITIAL PARTITION


initial_partition = GeographicPartition(graph_PA, assignment=my_apportionment, updaters=my_updaters)
fdem, frep = norm_data_part(initial_partition, my_electionproxy)
cds = get_labels(initial_partition, my_electionproxy) #get congressional district labels
#SETUP MARKOV CHAIN PROPOSAL W RECOM
# The ReCom proposal needs to know the ideal population for the districts so that
# we can improve speed by bailing early on unbalanced partitions.
#ideal_population = sum(initial_partition["population"].values()) / len(initial_partition)
ideal_population = sum(list(initial_partition["population"].values())) / len(initial_partition)

# We use functools.partial to bind the extra parameters (pop_col, pop_target, epsilon, node_repeats)
# of the recom proposal.
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
ranpart = recursive_tree_part(graph_PA, range(nparts), ideal_population, popkey,poptol,node_repeats=1)
randpartition = GeographicPartition(graph_PA,assignment = ranpart, updaters = my_updaters)
exec(open("partition_clean.py").read()) 
chain = MarkovChain(
    proposal=proposal,
    constraints=[
        pop_constraint,
        compactness_bound
    ],
    accept=accept.always_accept,
    initial_state=randpartition,
    total_steps=markovchainlength
)

t0=time.time()
#now can do initial_partition and know my_electionproxy will be OK, won't need alternate



#CONFIGURE MARKOV CHAIN

# This will take about 10 minutes.

# This will take about 10 minutes.
rsw = []
rmm = []
reg = []
rpp = []
data0 = fdem*pandas.DataFrame(sorted(initial_partition[my_electionproxy].percents("Democratic") ), index = cds)
data1 = fdem*pandas.DataFrame(sorted(randpartition[my_electionproxy].percents("Democratic") ), index = cds)
data0 = data0.transpose()
data1=data1.transpose()
#data1.columns = congressdistrictlabels
#data1 = data1.transpose()
#data1 = pandas.DataFrame((initial_partition[my_electionproxy].percents("Democratic") ))
for part in chain:
    rsw.append(part[my_electionproxy].wins("Democratic"))
    rmm.append(mean_median(part[my_electionproxy]))
    reg.append(efficiency_gap(part[my_electionproxy]))
#    rpp.append(np.mean(pd.Series(polsby_popper(part))))  #depends on geometry of the partition only not on vote outcomes
    datax = fdem*pandas.DataFrame(sorted(part[my_electionproxy].percents("Democratic" )), index=cds)
    datax = datax.transpose()
#    data1 = pandas.concat([data1, pandas.DataFrame(part[my_electionproxy].percents("Democratic" ))],axis=1)
    data1 = pandas.concat([data1, datax])


fig, ax = plt.subplots(figsize=(8, 6))

# Draw 50% line
ax.axhline(0.5, color="#cccccc")

# Draw boxplot
data1.boxplot(ax=ax, positions=range(len(data1.columns)),showfliers=False)

# Draw initial plan's Democratic vote %s (.iloc[0] gives the first row)
plt.plot(data0.iloc[0], "ro")

# Annotate
ax.set_title("Comparing the 2011 plan to an ensemble")
ax.set_ylabel("Democratic vote % (Senate 2012)")
ax.set_xlabel("Sorted districts")
ax.set_ylim(0, 1)
ax.set_yticks([0, 0.25, 0.5, 0.75, 1])

plt.show()
# NORMALIZE AND REDO at 50% per each party



 
t1=time.time()
outname = "redist_data/" + state + "_" + my_apportionment + "_" + my_electionproxy + "x" + str(markovchainlength) + postfix
bc.save(outname,data1, reg, rmm, rsw, rpp)
