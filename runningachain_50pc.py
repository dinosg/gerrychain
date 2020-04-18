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
from gerrychain.constraints import single_flip_contiguous
from functools import partial
import pandas
from gerrychain.metrics import mean_median, efficiency_gap
from strcmp_matlab import strfilter
import time
from norm_50 import norm_data
from get_districtlabels import get_labels



#SET CONSTANTS HERE:

my_apportionment = "CD_2011"    #type of district boundaries to calculate - eg US congressional, state senate, house etc.
my_electionproxy = "SEN12"           #pick the election to use as a statewide proxy for partisan voting for districted seats
my_electionproxy_alternate ="USS12"  #alternate name, see 'elections' variable below
my_electiondatafile = "./PA-shapefiles-master/PA_VTDs.json"   #PATH to the election data
markovchainlength = 1000  #length of Markov chain
proposaltype = "recom"



if ".json" in my_electiondatafile:
    graph_PA = Graph.from_json(my_electiondatafile)
else:
    graph_PA = Graph.from_file(my_electiondatafile)
    
t0=time.time()
elections = [
    Election("SEN10", {"Democratic": "SEN10D", "Republican": "SEN10R"}),
    Election("SEN12", {"Democratic": "USS12D", "Republican": "USS12R"}),
    Election("SEN16", {"Democratic": "T16SEND", "Republican": "T16SENR"}),
    Election("PRES12", {"Democratic": "PRES12D", "Republican": "PRES12R"}),
    Election("PRES16", {"Democratic": "T16PRESD", "Republican": "T16PRESR"})
]

#CONFIGURE UPDATERS
#We want to set up updaters for everything we want to compute for each plan in the ensemble.


# Population updater, for computing how close to equality the district
# populations are. "TOTPOP" is the population column from our shapefile.
my_updaters = {"population": updaters.Tally("TOTPOP", alias="population")}

# Election updaters, for computing election results using the vote totals
# from our shapefile.
election_updaters = {election.name: election for election in elections}
my_updaters.update(election_updaters)


#INITIAL PARTITION
initial_partition, graph_PA, my_updaters = norm_data(graph_PA, my_updaters, "CD_2011", my_electionproxy, my_electionproxy_alternate)
#initial_partition = GeographicPartition(graph_PA, assignment="CD_2011", updaters=my_updaters)
cds = get_labels(initial_partition, my_electionproxy) #get congressional district labels

#SETUP MARKOV CHAIN PROPOSAL W RECOM
# The ReCom proposal needs to know the ideal population for the districts so that
# we can improve speed by bailing early on unbalanced partitions.
#ideal_population = sum(initial_partition["population"].values()) / len(initial_partition)
ideal_population = sum(list(initial_partition["population"].values())) / len(initial_partition)

# We use functools.partial to bind the extra parameters (pop_col, pop_target, epsilon, node_repeats)
# of the recom proposal.
proposal = partial(recom,
                   pop_col="TOTPOP",
                   pop_target=ideal_population,
                   epsilon=0.02,
                   node_repeats=2
                  )


#CONSTRAINTS
compactness_bound = constraints.UpperBound(
    lambda p: len(p["cut_edges"]),
    2*len(initial_partition["cut_edges"])
)

pop_constraint = constraints.within_percent_of_ideal_population(initial_partition, 0.02)


#CONFIGURE MARKOV CHAIN

chain = MarkovChain(
    proposal=proposal,
    constraints=[
        pop_constraint,
        compactness_bound
    ],
    accept=accept.always_accept,
    initial_state=initial_partition,
    total_steps=markovchainlength

# This will take about 10 minutes.
cds = get_labels(initial_partition, my_electionproxy)
# This will take about 10 minutes.
rsw = []
rmm = []
reg = []
data1 = pandas.DataFrame(sorted(initial_partition[my_electionproxy].percents("Democratic") ), index = cds)

data1=data1.transpose()
#data1.columns = congressdistrictlabels
#data1 = data1.transpose()
#data1 = pandas.DataFrame((initial_partition[my_electionproxy].percents("Democratic") ))
for part in chain:
    rsw.append(part[my_electionproxy].wins("Democratic"))
    rmm.append(mean_median(part[my_electionproxy]))
    reg.append(efficiency_gap(part[my_electionproxy]))
    datax = pandas.DataFrame(sorted(part[my_electionproxy].percents("Democratic" )), index=cds)
    datax = datax.transpose()
#    data1 = pandas.concat([data1, pandas.DataFrame(part[my_electionproxy].percents("Democratic" ))],axis=1)
    data1 = pandas.concat([data1, datax])


fig, ax = plt.subplots(figsize=(8, 6))

# Draw 50% line
ax.axhline(0.5, color="#cccccc")

# Draw boxplot
data1.boxplot(ax=ax, positions=range(len(data1.columns)))

# Draw initial plan's Democratic vote %s (.iloc[0] gives the first row)
plt.plot(data1.iloc[0], "ro")

# Annotate
ax.set_title("Comparing the 2011 plan to an ensemble")
ax.set_ylabel("Democratic vote % (Senate 2012)")
ax.set_xlabel("Sorted districts")
ax.set_ylim(0, 1)
ax.set_yticks([0, 0.25, 0.5, 0.75, 1])

plt.show()
# NORMALIZE AND REDO at 50% per each party



 
t1=time.time()
