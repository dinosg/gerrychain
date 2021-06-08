#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 11:04:28 2021

reads in base .shp file df, whose filename specified in 'template_name'

reads in new external district assginments, whose filename = ex_dist_name

merges into base .shp geodataframe and 

Do this as script not function
@author: dinos
"""


import geopandas
import pandas as pd
from shapely.ops import unary_union
import numpy as np
from gerrychain import (GeographicPartition, Partition, Graph, MarkovChain, MarkovChain_xtended_polish,
                        proposals, updaters, constraints, accept, Election)
import matplotlib.pyplot as plt
from gerrychain import (GeographicPartition, Partition, Graph, MarkovChain,
                        proposals, updaters, constraints, accept, Election)
from gerrychain.proposals import (recom, propose_random_flip)
from functools import partial
from gerrychain.constraints import single_flip_contiguous, contiguous
from gerrychain.accept import always_accept
import pandas
from gerrychain.metrics import mean_median, efficiency_gap
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
import os


if ex_dist_name != '':
    mergecol2 = "GEOID10"
    mergecol1 = geotag
    getdir = os.getcwd()   #figure out what directory we're in
    getdir = getdir.split('/') #split the working directory by /'s to get depth of hierarchy levels
    levelinhierarchy = getdir.index('redistricting') #find out which level the 'redistricting' directory is at
    prefixa = ''
    for ik in range(len(getdir) - levelinhierarchy - 1):
        prefixa = prefixa + '../'
    
    ex_dist= pd.read_csv(prefixa + 'redist_data/example_districts/' + ex_dist_name, dtype=str)
    
    
    
    my_apportionment = my_apportionment[0:10]  #truncate to 1sst 10 chars b/c that's what df.to_file() does to field label
    print('my_apportionment = ', my_apportionment)
    if len(ex_dist.columns) == 3:
        ex_dist.columns  = ['Index', mergecol2, my_apportionment]
    
    elif len(ex_dist.columns) == 2:
        ex_dist.columns  = ['GEOID10', my_apportionment]
    else:
        print('screw up, wrong # columns in ex_dist')
        
    df=df.merge(ex_dist, left_on= mergecol1, right_on = mergecol2)
    
    #df.to_file('testhd200.shp')
    #graph_PA = Graph.from_file('testhd200.shp')
    #graph_PA = Graph.from_geodataframe(df)

graph_PA = Graph.from_geodataframe(df)
if state == "WI20":
    exec(open("/home/dinos/Documents/MATLAB/test_work/redistricting/shapefiles_multistate/WI-shapefiles-master/WI_2020_wards/WI_island_fix.py").read()) 
 

   