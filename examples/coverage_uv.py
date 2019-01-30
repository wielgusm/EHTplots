#PLOTTING AMP vs UVDIST FROM UVFITS IN EHT STYLE
#Maciek Wielgus 2018/12/05

#import sys
#sys.path.insert(0,'/home/maciek/EHTplots/EHTplots/')
from plot_coverage_uv import *
#trick to prevent weird bold roman fonts in python 3
#import matplotlib
#del matplotlib.font_manager.weight_dict['roman']
#matplotlib.font_manager._rebuild()

import warnings
warnings.filterwarnings('ignore')

#data to use
pathf = '/data/2017-april/ce/er5/postproc-hops-lo/3.+netcal/3601/hops_3601_M87+netcal.uvfits'

###################################
#SOME USEFULL FIGURE SETTINGS
###################################
figsize=(8,5.5) #size of the figure
fontsize=15
ticks_fontsize=14
legend=False
fontname='Latin Modern Roman'
fontname2='Helvetica'
line_width=0.5
mark_edge_color=[0,0,0,0.5] #color of the marker edge, last digit is transparency alpha
size_dots_primary=50 #size of markers for primary baselines  
size_dots_redundant=50#size of markers for redundant baselines
mark_edge_width=0.5 #edge of markers
xlim=[10,-10] #x axis range
ylim=[-10,10]#y axis range
circ_label=True
grid_alpha=0.0

snr_cut=0. #make an snr threshold
ticks_in_style=False #Katie's style of ticks with labels inside the figure
#savefig='my_pretty_figure.pdf' #name / path to save the figure


plot_coverage_uv(pathf,fontsize=fontsize,ticks_fontsize=ticks_fontsize, line_width=line_width,
            legend=legend,fontname=fontname,mark_edge_color=mark_edge_color,
            size_dots_primary=size_dots_primary, size_dots_redundant=size_dots_redundant,
            mark_edge_width=0.5, xlim=xlim, ylim=ylim,circ_label=circ_label,
            ticks_in_style=ticks_in_style,figsize=figsize,snr_cut=snr_cut,grid_alpha=grid_alpha,savefig='')