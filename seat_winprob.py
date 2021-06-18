#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 20:05:14 2021
computes the probability of winning a (fractional) seat giving the election result
x_pc, which is a fraction, eg. 0.55 (equal 55% vote score) and standard deviation of
election returns from election to election, eg s = 0.05 is a 5% standard deviation
in election results

that is, if the election score = 0.55 and the std dev s = 0.05 then the win probabiilty
= 0.82, you've won 0.85 of a seat. if you're exactly on 0.5 then you win 0.5 seats

This avoids the 'quantization' of seats won in the seats - votes curve

@author: dpg
"""
from scipy.special import erf 
def seat_winprob(x_pc, s):
    F = 0.5*(1 + erf((x_pc-.5)/s/2**.5))
    return F