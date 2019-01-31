#USEFUL DEFINITIONS
#Maciek Wielgus 2019/01/30

import ehtim as eh
import numpy as np
import pandas as pd
#import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.transforms as mt
from matplotlib import rcParams

rcParams['text.usetex']=True
rcParams['font.family']='serif'
rcParams['ytick.minor.visible']=True
rcParams['xtick.minor.visible']=True
rcParams['ytick.right']=True
rcParams['xtick.top']=True
rcParams['xtick.direction']='in'
rcParams['ytick.direction']='in'
rcParams['xtick.major.width']=1.2
rcParams['xtick.minor.width']=1.2


def merge_two_dicts(x, y):
        z = x.copy()   # start with x's keys and values
        z.update(y)    # modifies z with y's keys and values & returns None
        return z
rgb = lambda x,y,z: (x/255.,y/255.,z/255.)
SMT2Z = {'ALMA': 'A', 'APEX': 'X', 'JCMT': 'J', 'LMT':'L', 'SMR':'R', 'SMA':'S', 'SMT':'Z', 'PV':'P','SPT':'Y'}
Z2SMT = {v: k for k, v in SMT2Z.items()}
AZ2SMT={'AA':'ALMA','AP':'APEX','AZ':'SMT','LM':'LMT','SP':'SPT','SM':'SMA','JC':'JCMT','SR':'SMAR','PV':'PV'}
palette_dict = {'ALMA-APEX':rgb(0,0,0),
            'JCMT-SMA':rgb(0,0,0),
            'SMT-LMT':rgb(51, 51, 255),
            'ALMA-LMT':rgb(0, 102, 153),
            'APEX-LMT':rgb(0, 102, 153),
            'SMT-SMA':rgb(204, 153, 0),
            'SMT-JCMT':rgb(204, 153, 0),
            'LMT-SMA':rgb(204, 0, 204),
            'JCMT-LMT':rgb(204, 0, 204),
            'ALMA-SMT':rgb(51, 204, 51),
            'APEX-SMT':rgb(51, 204, 51),
            'ALMA-SPT':rgb(255, 0, 0),
            'APEX-SPT':rgb(255, 0, 0),
            'ALMA-PV':rgb(51, 153, 255),
            'APEX-PV':rgb(51, 153, 255),
            'ALMA-SMA':rgb(204, 153, 255),
            'ALMA-JCMT':rgb(204, 153, 255),
            'APEX-SMA':rgb(204, 153, 255),
            'APEX-JCMT':rgb(204, 153, 255),#:rgb(133, 163, 41),
            'LMT-SPT':rgb(193, 166, 44),#'yellow',
            'LMT-PV':rgb(153, 102, 51),
            'SMA-SPT':rgb(139,0,0),#'darkred',
            'JCMT-SPT':rgb(139,0,0),#'darkred',
            'SMT-SPT':rgb(250,128,114),#'salmon', 
            'PV-SPT':rgb(139, 69, 19), #'saddlebrown'
            'PV-SMA':‎rgb(210, 180, 140),
            'JCMT-PV':‎rgb(210, 180, 140),
            'SMT-PV':rgb(179, 179, 0)}
palette_dict_inv = {k.split('-')[1]+'-'+k.split('-')[0] : v for k, v in palette_dict.items()}
baselines_palette = merge_two_dicts(palette_dict, palette_dict_inv)
#'PV-SMA':‎rgb(210, 180, 140),#'tan'
