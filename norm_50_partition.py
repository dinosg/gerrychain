#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Monday apr 27 16:11:05 2020

obtains normalization factors fdem, frep from PARTITION

but doesn't normalize anything, just gets factors

@author: dinos
"""
 
def norm_data_part(thepartition, proxy_election ):
    
    normfac = 0.5  #could set this to something else if you wanted but 50%-50% split is default
    
    aa = thepartition[proxy_election]  #eg initial_partition["SEN12"] or whatever the proxy for partisanship is
    totd = 0
    totr = 0
    
    for kk in aa.totals_for_party["Democratic"]:
        totd += aa.totals_for_party["Democratic"][kk]
        
    for kk in aa.totals_for_party["Republican"]:
        totr += aa.totals_for_party["Republican"][kk]
    
    tot_votes = totd + totr
    
    pc_dem = totd/tot_votes  #% dem and rep vote shares
    pc_rep = totr/tot_votes
    
    fdem = normfac/pc_dem
    frep = normfac/pc_rep
    
    return fdem, frep
    
