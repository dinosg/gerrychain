#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 16:11:05 2020
normalizes election return data so both republican & dem votes are equalized
-and =
creates initial partition with that normalization
the_election = "SEN12" for example input

however if assignment is made thru graph data (eg. b/c chain has not been run yet) then the election
names are something else, like USS12D and USS12R  (for this example) so annoyingly, USS12 has to be passed
here and fixed up
the_assignment = "CD_2011" is example input because you have to rebuilt the initial_partition after normalizing
@author: dinos
"""
from gerrychain import GeographicPartition
def norm_data(thegraph, my_updaters, the_assignment, the_election, graph_election):
    
    normfac = 0.5  #could set this to something else if you wanted but 50%-50% split is default
    
    #if my_updaters vote returns are float, then you have to make fixes there, else do it in graph data
    if type(my_updaters[the_election].tallies["Democratic"].data) == float: 
        zd = 0
        zr = 0
        for zz in my_updaters[the_election].tallies["Democratic"].data:
            zd += my_updaters[the_election].tallies["Democratic"].data[zz]
            zr += my_updaters[the_election].tallies["Republican"].data[zz]
        
        ztot = zd+zr
        fdem = normfac *ztot/zd
        frep = normfac * ztot/zr
        
        for zz in my_updaters[the_election].tallies["Democratic"].data:
        	my_updaters[the_election].tallies["Democratic"].data[zz]  *= fdem
        for zz in my_updaters[the_election].tallies["Republican"].data:
        	my_updaters[the_election].tallies["Republican"].data[zz]  *= frep
    
    else:
        
        zd = 0
        zr = 0
        graph_elec_r = graph_election + "R"
        graph_elec_d = graph_election + "D"
        for zz in thegraph._node:
            zd += thegraph._node[zz][graph_elec_d] 
            zr += thegraph._node[zz][graph_elec_r] 
        
        ztot = zd+zr
        fdem = normfac *ztot/zd
        frep = normfac * ztot/zr
        
        for zz in thegraph._node:
            thegraph._node[zz][graph_elec_d] *= fdem
            thegraph._node[zz][graph_elec_r] *= frep
        
    initial_partition = GeographicPartition(thegraph, assignment=the_assignment, updaters=my_updaters)
    return initial_partition, thegraph, my_updaters
