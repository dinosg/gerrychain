#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 14:07:36 2020
return the Elections object based on what state you're trying to get info on.'
This needs to be updated as you look @ more states, add to it. can include more attorney general races, you name it
@author: dpg
"""
from gerrychain import Election

def get_elections(state):
    composite = ''  #empty in case
#PA data 
    if state == "PA":
        elections = [
            Election("SEN18", {"Democratic": "G18DemSen", "Republican": "G18RepSen"}),
            Election("GOV18", {"Democratic": "G18DemGov", "Republican": "G18RepGov"}),
            Election("SEN10", {"Democratic": "SEN10D", "Republican": "SEN10R"}),
            Election("SEN12", {"Democratic": "USS12D", "Republican": "USS12R"}),
            Election("SEN16", {"Democratic": "T16SEND", "Republican": "T16SENR"}),
            Election("PRES12", {"Democratic": "PRES12D", "Republican": "PRES12R"}),
            Election("PRES16", {"Democratic": "T16PRESD", "Republican": "T16PRESR"}),
            Election("GOV10", {"Democratic": "GOV10D", "Republican": "GOV10R"}),
            Election("GOV14", {"Democratic": "F2014GOVD", "Republican": "F2014GOVR"}),
            Election("ATG12", {"Democratic": "ATG12D", "Republican": "ATG12R"}),
            Election("ATG16", {"Democratic": "T16ATGD", "Republican": "T16ATGR"})
        ]
        composite = ['SEN10', 'SEN12', 'SEN16', 'PRES12', 'PRES16', 'GOV10', 'GOV14', 'ATG12', 'ATG16', 'SEN18','GOV18']
       
    elif state == "TX":
    
    #for TX data
        
        elections = [         
            Election("SEN14", {"Democratic": "SEN14D", "Republican": "SEN14R"}),
            Election("SEN12", {"Democratic": "SEN12D", "Republican": "SEN12R"}),
            Election("GOV14", {"Democratic": "GOV14D", "Republican": "GOV14R"}),
            Election("PRES12", {"Democratic": "PRES12D", "Republican": "PRES12R"}),
            Election("PRES16", {"Democratic": "PRES16D", "Republican": "PRES16R"})
        ]
        composite = ['SEN14', 'SEN12', 'PRES12', 'PRES16', 'GOV14']
    
    elif state == "OH":
    
    #for TX data
        
        elections = [         
            Election("SEN16", {"Democratic": "SEN16D", "Republican": "SEN16R"}),
            Election("PRES16", {"Democratic": "PRES16D", "Republican": "PRES16R"})
        ]
        composite = ['SEN16', 'PRES16']
    elif state == "WI":
    #for WI data:
        elections = [         
            Election("SEN16", {"Democratic": "USSDEM16", "Republican": "USSREP16"}),
            Election("WAG14", {"Democratic": "WAGDEM14", "Republican": "WAGREP14"}),
            Election("SEN12", {"Democratic": "USSDEM12", "Republican": "USSREP12"}),
            Election("GOV14", {"Democratic": "GOVDEM14", "Republican": "GOVREP14"}),
            Election("GOV12", {"Democratic": "GOVDEM12", "Republican": "GOVREP12"}),
            Election("SOS14", {"Democratic": "SOSDEM14", "Republican": "SOSREP14"}),
            Election("PRES12", {"Democratic": "PREDEM12", "Republican": "PREREP12"}),
            Election("PRES16", {"Democratic": "PREDEM16", "Republican": "PREREP16"})
        ]
        composite = ['SEN16', 'SEN12', 'PRES12', 'PRES16', 'GOV14','GOV12','WAG14', 'SOS14']

    elif state == "WI20":
    #for WI data:
        elections = [         
            Election("SEN16", {"Democratic": "SEN16D", "Republican": "SEN16R"}),
            Election("AG14", {"Democratic": "AG14D", "Republican": "AG14R"}),
            Election("AG18", {"Democratic": "AG18D", "Republican": "AG18R"}),
            Election("SEN12", {"Democratic": "SEN12D", "Republican": "SEN12R"}),
            Election("GOV14", {"Democratic": "GOV14D", "Republican": "GOV14R"}),
            Election("GOV12", {"Democratic": "GOV12D", "Republican": "GOV12R"}),
            Election("SOS14", {"Democratic": "SOS14D", "Republican": "SOS14R"}),
            Election("PRES12", {"Democratic": "PRES12D", "Republican": "PRES12R"}),
            Election("PRES16", {"Democratic": "PRES16D", "Republican": "PRES16R"}),
            Election("GOV18", {"Democratic": "GOV18D", "Republican": "GOV18R"}),
            Election("SEN18", {"Democratic": "SEN18D", "Republican": "SEN18R"})
            ]
        composite = ['SEN16', 'SEN12', 'PRES12', 'PRES16', 'GOV14','GOV12','AG14', 'SOS14', 
                   'GOV18', 'SEN18', 'AG18'] 
    elif state    == "GA":
        elections = [         
            Election("PRES16", {"Democratic": "PRES16D", "Republican": "PRES16R"}),
            Election("SEN16", {"Democratic": "SEN16D", "Republican": "SEN16R"})
        ]
        composite = ['PRES16', 'SEN16']
    elif state == "MI":
    #for WI data:
        elections = [         
            Election("PRES16", {"Democratic": "PRES16D", "Republican": "PRES16R"})
        ]
        composite = ['PRES16']
    elif state == "NC":
#for WI data:
        elections = [         
            Election("EL12G_PR_", {"Democratic": "EL12G_PR_D", "Republican": "EL12G_PR_R"}),
            Election("EL16G_PR_", {"Democratic": "EL16G_PR_D", "Republican": "EL16G_PR_R"}),
            Election("EL16G_US", {"Democratic": "EL16G_US_1", "Republican": "EL16G_USS_"}),
            Election("EL16G_GV_", {"Democratic": "EL16G_GV_D", "Republican": "EL16G_GV_R"}),
            Election("EL12G_GV_", {"Democratic": "EL12G_GV_D", "Republican": "EL12G_GV_R"}),
            Election("EL14G_US", {"Democratic": "EL14G_US_1", "Republican": "EL14G_USS_"})
        ]
        composite = ["EL12G_PR_","EL16G_PR_","EL16G_US","EL16G_GV_","EL12G_GV_","EL14G_US"]
    elif state == "FL":
        elections = [         
            Election("SEN16", {"Democratic": "Dem_2016_s", "Republican": "Rep_2016_s"}),
            Election("PRES16", {"Democratic": "Dem_2016_p", "Republican": "Rep_2016_p"})
        ]
        composite = ["SEN16","PRES16"]   
 
    elif state == "MA":
        elections = [         
            Election("SEN14", {"Democratic": "SEN14D", "Republican": "SEN14R"}),
            Election("SEN12", {"Democratic": "SEN12D", "Republican": "SEN12R"}),
            Election("SEN13", {"Democratic": "SEN13D", "Republican": "SEN13R"}),
            Election("SEN18", {"Democratic": "SEN18D", "Republican": "SEN18R"}),
            Election("GOV14", {"Democratic": "GOV14D", "Republican": "GOV14R"}),
            Election("GOV18", {"Democratic": "GOV18D", "Republican": "GOV18R"}),
            Election("PRES16", {"Democratic": "PRES16D", "Republican": "PRES16R"}),
            Election("PRES12", {"Democratic": "PRES12D", "Republican": "PRES12R"})
        ]
        composite = ["SEN14","PRES16", "SEN12", "SEN13", "PRES12", "GOV14", "GOV18","SEN18"]
    elif state == "MD":
        elections = [         
            Election("SEN18", {"Democratic": "SEN18D", "Republican": "SEN18R"}),
            Election("SEN12", {"Democratic": "SEN12D", "Republican": "SEN12R"}),
            Election("SEN16", {"Democratic": "SEN16D", "Republican": "SEN16R"}),
            Election("GOV18", {"Democratic": "GOV18D", "Republican": "GOV18R"}),
            Election("AG18", {"Democratic": "AG18D", "Republican": "AG18R"}),
            Election("GOV14", {"Democratic": "GOV14D", "Republican": "GOV14R"}),
            Election("AG14", {"Democratic": "AG14D", "Republican": "AG14R"}),
            Election("PRES16", {"Democratic": "PRES16D", "Republican": "PRES16R"}),
            Election("PRES12", {"Democratic": "PRES12D", "Republican": "PRES12R"})
        ]
        composite = ["SEN12","SEN16", "SEN18","PRES16","PRES12","GOV18","GOV14","AG18","AG14"]
    return elections, composite

def get_elections_simple(state):
    composite = ''  #empty in case
#PA data 
    if state == "PA":
        elections = [
            Election("SEN18", {"Democratic": "G18DemSen", "Republican": "G18RepSen"}),
            Election("GOV18", {"Democratic": "G18DemGov", "Republican": "G18RepGov"}),
            Election("SEN10", {"Democratic": "SEN10D", "Republican": "SEN10R"}),
            Election("SEN12", {"Democratic": "USS12D", "Republican": "USS12R"}),
            Election("SEN16", {"Democratic": "T16SEND", "Republican": "T16SENR"}),
            Election("PRES12", {"Democratic": "PRES12D", "Republican": "PRES12R"}),
            Election("PRES16", {"Democratic": "T16PRESD", "Republican": "T16PRESR"}),
            Election("GOV10", {"Democratic": "GOV10D", "Republican": "GOV10R"}),
            Election("GOV14", {"Democratic": "F2014GOVD", "Republican": "F2014GOVR"}),
            Election("ATG12", {"Democratic": "ATG12D", "Republican": "ATG12R"}),
            Election("ATG16", {"Democratic": "T16ATGD", "Republican": "T16ATGR"})
        ]
        composite = ['SEN10', 'SEN12', 'SEN16', 'PRES12', 'PRES16', 'GOV10', 'GOV14', 'ATG12', 'ATG16', 
                     'SEN18','GOV18']
    elif state == "MD":
        elections = [         
            Election("SEN18", {"Democratic": "SEN18D", "Republican": "SEN18R"}),
            Election("SEN12", {"Democratic": "SEN12D", "Republican": "SEN12R"}),
            Election("SEN16", {"Democratic": "SEN16D", "Republican": "SEN16R"}),
            Election("GOV18", {"Democratic": "GOV18D", "Republican": "GOV18R"}),
            Election("AG18", {"Democratic": "AG18D", "Republican": "AG18R"}),
            Election("GOV14", {"Democratic": "GOV14D", "Republican": "GOV14R"}),
            Election("AG14", {"Democratic": "AG14D", "Republican": "AG14R"}),
            Election("PRES16", {"Democratic": "PRES16D", "Republican": "PRES16R"}),
            Election("PRES12", {"Democratic": "PRES12D", "Republican": "PRES12R"})
        ]   
    elif state == "TX":
    
    #for TX data
        
        elections = [         
            Election("SEN14", {"Democratic": "SEN14D", "Republican": "SEN14R"}),
            Election("SEN12", {"Democratic": "SEN12D", "Republican": "SEN12R"}),
            Election("GOV14", {"Democratic": "GOV14D", "Republican": "GOV14R"}),
            Election("PRES12", {"Democratic": "PRES12D", "Republican": "PRES12R"}),
            Election("PRES16", {"Democratic": "T16PRESD", "Republican": "T16PRESR"})
        ]
        composite = ['SEN14', 'SEN12', 'PRES12', 'PRES16', 'GOV14']
    
    elif state == "WI":
    #for WI data:
        elections = [         
            Election("SEN16", {"Democratic": "USSDEM16", "Republican": "USSREP16"}),
            Election("WAG14", {"Democratic": "WAGDEM14", "Republican": "WAGREP14R"}),
            Election("SEN12", {"Democratic": "USSDEM12", "Republican": "USSREP12"}),
            Election("GOV14", {"Democratic": "GOVDEM14", "Republican": "GOVREP14"}),
            Election("GOV12", {"Democratic": "GOVDEM12", "Republican": "GOVREP12"}),
            Election("SOS14", {"Democratic": "SOSDEM14", "Republican": "SOSREP14"}),
            Election("PRES12", {"Democratic": "PREDEM12", "Republican": "PREREP12"}),
            Election("PRES16", {"Democratic": "PREDEM16", "Republican": "PREREP16"})
        ]
        composite = ['SEN16', 'SEN12', 'PRES12', 'PRES16', 'GOV14','GOV12','WAG14', 'SOS14']
    elif state == "WI20":
    #for WI data:
        elections = [         
            Election("SEN16", {"Democratic": "SEN16D", "Republican": "SEN16R"}),
            Election("AG14", {"Democratic": "AG14D", "Republican": "AG14R"}),
            Election("AG18", {"Democratic": "AG18D", "Republican": "AG18R"}),
            Election("SEN12", {"Democratic": "SEN12D", "Republican": "SEN12R"}),
            Election("GOV14", {"Democratic": "GOV14D", "Republican": "GOV14R"}),
            Election("GOV12", {"Democratic": "GOV12D", "Republican": "GOV12R"}),
            Election("SOS14", {"Democratic": "SOS14D", "Republican": "SOS14R"}),
            Election("PRES12", {"Democratic": "PRES12D", "Republican": "PRES12R"}),
            Election("PRES16", {"Democratic": "PRES16D", "Republican": "PRES16R"}),
            Election("GOV18", {"Democratic": "GOV18D", "Republican": "GOV18R"}),
            Election("SEN18", {"Democratic": "SEN18D", "Republican": "SEN18R"})
            ]
        composite = ['SEN16', 'SEN12', 'PRES12', 'PRES16', 'GOV14','GOV12','AG14', 'SOS14', 
                   'GOV18', 'SEN18', 'AG18']
    elif state == "MI":
    #for WI data:
        elections = [         
            Election("PRES16", {"Democratic": "PRES16D", "Republican": "PRES16R"})
        ]
        composite = ['PRES16']
    elif state == "NC":
#for WI data:
        elections = [         
            Election("EL12G_PR_", {"Democratic": "EL12G_PR_D", "Republican": "EL12G_PR_R"}),
            Election("EL16G_PR_", {"Democratic": "EL16G_PR_D", "Republican": "EL16G_PR_R"}),
            Election("EL16G_US", {"Democratic": "EL16G_US_1", "Republican": "EL16G_USS_"}),
            Election("EL16G_GV_", {"Democratic": "EL16G_GV_D", "Republican": "EL16G_GV_R"}),
            Election("EL12G_GV_", {"Democratic": "EL12G_GV_D", "Republican": "EL12G_GV_R"}),
            Election("EL14G_US", {"Democratic": "EL14G_US_1", "Republican": "EL14G_USS_"})
        ]
        composite = ["EL12G_PR_","EL16G_PR_","EL16G_US","EL16G_GV_","EL12G_GV_","EL14G_US"]
    elif state == "FL":
        elections = [         
            Election("SEN16", {"Democratic": "Dem_2016_s", "Republican": "Rep_2016_s"}),
            Election("PRES16", {"Democratic": "Dem_2016_p", "Republican": "Rep_2016_p"})
        ]
        composite = ["SEN16","PRES16"]      
        
    elif state == "MA":
        elections = [         
            Election("SEN14", {"Democratic": "SEN14D", "Republican": "SEN14R"}),
            Election("SEN12", {"Democratic": "SEN12D", "Republican": "SEN12R"}),
            Election("SEN13", {"Democratic": "SEN13D", "Republican": "SEN13R"}),
            Election("PRES16", {"Democratic": "PRES16D", "Republican": "PRES16R"}),
            Election("PRES12", {"Democratic": "PRES12D", "Republican": "PRES12R"})
        ]
        composite = ["SEN14","PRES16", "SEN12", "SEN13"]
    return elections , composite