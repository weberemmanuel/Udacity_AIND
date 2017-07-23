#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed July 10 13:41:32 2017

@author: eweber
"""
import time

def timencalls(n,f,*args):
    """
    timencalls: execute a function n times and return the avergage running time
    in seconds.
    n: number of calls
    f: function to execute
    args: variable argument to pass in to the function
    return: the average time in floating point of seconds

    """
    t1 = time.clock()
    for _ in range(n):
        f(*args)
    t2 = time.clock()
    return (t2-t1)/n;
