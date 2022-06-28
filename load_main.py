#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for loading all main modues for analysis, including local code.
Created on Sat  27 Jun 2020

@author: Caterina Mogno c.mogno@ed.ac.uk
"""

#load main libraries
import xarray as xr
import numpy as np
import pandas as pd

#load local code
import sys
sys.path.append('/exports/csce/datastore/geos/users/s1878599/phd_work/')
import warnings
warnings.filterwarnings('ignore')


# Define WRF-Chem outputs data path
#dpath='/geos/d21/s1878599/IGP'
#print('WRFchem outputs data path is: dpath='+dpath)