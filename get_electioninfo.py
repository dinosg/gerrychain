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
#PA data 
    if state == "PA":
        elections = [
            Election("SEN10", {"Democratic": "SEN10D", "Republican": "SEN10R"}),
            Election("SEN12", {"Democratic": "USS12D", "Republican": "USS12R"}),
            Election("SEN16", {"Democratic": "T16SEND", "Republican": "T16SENR"}),
            Election("PRES12", {"Democratic": "PRES12D", "Republican": "PRES12R"}),
            Election("PRES16", {"Democratic": "T16PRESD", "Republican": "T16PRESR"})
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
    
    elif state == "WI":
    #for WI data:
        elections = [         
            Election("SEN16", {"Democratic": "USSDEM16", "Republican": "USSREP16"}),
            Election("WAG14", {"Democratic": "WAGDEM14", "Republican": "WAGREP14R"}),
            Election("SEN12", {"Democratic": "USSDEM12", "Republican": "USSREP12"}),
            Election("GOV12", {"Democratic": "GOVDEM12", "Republican": "GOVREP12"}),
            Election("PRES12", {"Democratic": "PREDEM12", "Republican": "PREREP12"}),
            Election("PRES16", {"Democratic": "PREDEM16", "Republican": "PREREP16"})
        ]

    elif state == "MI":
    #for WI data:
        elections = [         
            Election("PRES16", {"Democratic": "PRES16D", "Republican": "PRES16R"})
        ]
    return elections