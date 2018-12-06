#PLOTTING AMP vs UVDIST FROM UVFITS IN EHT STYLE
#Maciek Wielgus 2018/12/05

#import sys
#sys.path.insert(0,'/home/maciek/EHTplots/EHTplots/')
from plot_amp_uvdist import *
import matplotlib
del matplotlib.font_manager.weight_dict['roman']
matplotlib.font_manager._rebuild()
import warnings
warnings.filterwarnings('ignore')

#data to use
pathf = '/data/2017-april/ce/er5/postproc-hops-lo/3.+netcal/3601/hops_3601_M87+netcal.uvfits'

###################################
#SOME USEFULL FIGURE SETTINGS
###################################
figsize=(6,4) #size of the figure
fontsize=15
ticks_fontsize=14
line_width=0.5 #errorbar line thickness
capsize=2 #errorbar cap size
legend=False
label=True
fontname='Latin Modern Roman'
fontname2='Helvetica'
mark_edge_color=[0,0,0,0.5] #color of the marker edge, last digit is transparency alpha
line_color=[0,0,0,1] #color of error bar, last digit is transparency alpha
size_dots_primary=6*1.3 #size of markers for primary baselines  
size_dots_redundant=6*1. #size of markers for redundant baselines
mark_edge_width=0.5 #edge of markers
xlim=[-0.4,9] #x axis range
ylim=[0.005,2]#y axis range
yscale='log'
debias=True #plot debiased amplitudes
snr_cut=0. #make an snr threshold
bars_on=1. #multiplier for errorbar length, 0 for no errorbars
ticks_in_style=False #Katie's style of ticks with labels inside the figure
#savefig='my_pretty_figure.pdf' #name / path to save the figure

plot_amp_uvdist(pathf,savefig='',fontsize=fontsize,ticks_fontsize=ticks_fontsize,line_width=line_width,capsize=capsize,
               legend=legend,fontname=fontname,mark_edge_color=mark_edge_color,
               line_color=line_color, size_dots_primary=size_dots_primary,
               size_dots_redundant=size_dots_redundant,mark_edge_width=mark_edge_width,
               xlim=xlim,ylim=ylim,yscale=yscale,debias=debias,snr_cut=snr_cut,bars_on=bars_on,
               ticks_in_style=ticks_in_style, figsize=figsize)