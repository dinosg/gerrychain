#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 11:11:15 2020
python version of Matlab strcmp()
@author: dpg
"""

def strcmp(stringarray, teststr):
    zz = []
    if len(stringarray) > 1:
        for nn in range(len(stringarray)):
            if stringarray[nn] is teststr:
                zz.append(True)
            else:
                zz.append(False)
    elif len(stringarray) == 1 :
        if stringarray is teststr:
            zz.append(True)
        else:
            zz.append(False)
    else:
        zz = []
    return zz

def strcmp_int(stringarray, teststr):
    """
    
    integer version of Matlab strcmp, returns integer indices where teststr found in stringarray
    
    """
    

    zz = []
    if len(stringarray) > 1:
        for nn in range(len(stringarray)):
            if stringarray[nn] is teststr:
                zz.append(nn)
              
    elif len(stringarray) == 1 :
        if stringarray is teststr:
            zz.append(0)
        else:
            zz=[]
    else:
        zz = []
    return zz

def strfilter_logical(stringarray, logicalindex):
    """
    

    Parameters
    ----------
    stringarray : string
        DESCRIPTION.
    logicalindex : logical
        DESCRIPTION.

    Returns stringarray filtered by logicalindex
    -------
    TYPE
        stromg.

    """
    resultstr = []
    if len(stringarray) != len(logicalindex):
        print("error: logical index not same length as string\n")
        return []
    else:
        for n in range(len(stringarray)):
            if logicalindex[n]:
                resultstr.append(stringarray[n])
        return resultstr
    
def strfilter(stringarray, index):
    """

    Parameters
    ----------
    sringarray : string
        DESCRIPTION.
    index : list of integers or tuple
        DESCRIPTION.

    Returns
    -------
    stringarray filtered by integer (locational) index
    
    """

    resultstr = [stringarray[nn] for nn in index]
#    for nn in index:   #this code does the same thing...
#        resultstr.append(stringarray[nn])
    return resultstr
        