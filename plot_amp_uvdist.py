import ehtim as eh
import numpy as np
import pandas as pd
#import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

###################################
#SOME ASSUMPTIONS
###################################
fontsize=14 
ticks_fontsize=10
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
debias=True #plot debiased amplitudes
snr_cut=0. #make an snr threshold
bars_on=1. #multiplier for errorbar length, 0 for no errorbars
#savefig='my_pretty_plot.pdf' #path / name to save the plot

def plot_amp_uvdist(pathf,fontsize=14,ticks_fontsize=10, line_width=0.5,
            capsize=2,legend=False,label=True,fontname='Latin Modern Roman',mark_edge_color=[0,0,0,0.5],
line_color=[0,0,0,1], size_dots_primary=6*1.3, size_dots_redundant=6*1.,
            mark_edge_width=0.5, xlim=[-0.4,9], ylim=[0.005,2],bars_on=1.,
            yscale='log',ticks_in_style=False,figsize=(6,4),debias=True,snr_cut=0,savefig='',fontweight='normal'):
    
    rgb = lambda x,y,z: (x/255.,y/255.,z/255.) 
    def merge_two_dicts(x, y):
        z = x.copy()   # start with x's keys and values
        z.update(y)    # modifies z with y's keys and values & returns None
        return z
    AZ2SMT={'AA':'ALMA','AP':'APEX','AZ':'SMT','LM':'LMT','SP':'SPT','SM':'SMA','JC':'JCMT','SR':'SMAR','PV':'IRAM30'}
    palette_dict = {'ALMA-APEX':rgb(0,0,0),
                    'JCMT-SMA':rgb(120,120,120),
                    'SMT-LMT':rgb(51, 51, 255),
                    'ALMA-LMT':rgb(0, 102, 153),
                    'APEX-LMT':rgb(0, 153, 51),
                    'SMT-SMA':rgb(204, 153, 0),
                    'SMT-JCMT':rgb(204, 0, 0),
                    'LMT-SMA':rgb(204, 0, 204),
                    'JCMT-LMT':rgb(51, 204, 204),
                    'ALMA-SMT':rgb(51, 204, 51),
                    'APEX-SMT':rgb(255, 153, 0),
                    'ALMA-SPT':rgb(255, 0, 0),
                    'APEX-SPT':rgb(153, 0, 255),
                    'ALMA-IRAM30':rgb(51, 153, 255),
                    'APEX-IRAM30':rgb(51, 153, 102),
                    'ALMA-SMA':rgb(204, 153, 255),
                    'ALMA-JCMT':rgb(102, 153, 0),
                    'APEX-SMA':rgb(107, 245, 61),
                    'APEX-JCMT':rgb(51, 51, 255),#:rgb(133, 163, 41),
                    'LMT-SPT':'yellow',
                    'LMT-IRAM30':rgb(153, 102, 51),
                    'SMA-SPT':'darkred',
                    'JCMT-SPT':'olivedrab',
                    'SMT-SPT':'salmon', 
                    'IRAM30-SPT':'saddlebrown',
                    'IRAM30-SMA':'tan',
                    'JCMT-IRAM30':rgb(255,0,0),
                    'SMT-IRAM30':rgb(179, 179, 0)}
    palette_dict_inv = {k.split('-')[1]+'-'+k.split('-')[0] : v for k, v in palette_dict.items()}
    #current_palette={**palette_dict, **palette_dict_inv}
    current_palette = merge_two_dicts(palette_dict, palette_dict_inv)
    #sns.set_style('white')
    #sns.set_style('ticks')
    #sns.set_style({"xtick.direction": "in","ytick.direction": "in"})
    del matplotlib.font_manager.weight_dict['roman']
    matplotlib.font_manager._rebuild()
    if type(pathf)==str:
        ###################################
        #LOAD DATA AND MAKE A DATAFRAME
        ###################################
        obs = eh.obsdata.load_uvfits(pathf)
        obs.add_scans()
        obs = obs.avg_coherent(inttime=0.,scan_avg=True)
        df = eh.statistics.dataframes.make_df(obs)
    else:
        df=pathf

    df['uvdist']=np.sqrt(df.u**2 + df.v**2)/1e6
    foo=df
    foo=foo[foo.snr>snr_cut]
    if debias:
        foo=foo[foo.snr>1.1]
        foo['ampdb']=np.sqrt(foo['amp']**2-foo['sigma']**2)
        foo['snrdb']=np.sqrt(foo['snr']**2-1)
    else:
        foo['ampdb']=foo['amp']
        foo['snrdb']=foo['snr']

    plt.figure(figsize=figsize)
    plt.rcParams["font.weight"] = "normal"
    plt.rcParams["axes.labelweight"] = "normal"
    #primary baselines
    for base in sorted(list(foo.baseline.unique())):      
        basefull = AZ2SMT[base[:2]]+'-'+AZ2SMT[base[3:]]
        if ('JCMT' not in basefull) and (('APEX' not in basefull) or ('ALMA' in basefull)):
            plt.errorbar(foo[foo.baseline==base].uvdist/1e3,foo[foo.baseline==base].ampdb,
                         bars_on*foo[foo.baseline==base].sigma,fmt='o',ms=size_dots_primary,
                         color=current_palette[basefull],label=basefull,elinewidth=line_width,
                        capsize=capsize,mec=mark_edge_color,ecolor=line_color,mew=mark_edge_width)
    #redundant baselines       
    for base in sorted(list(foo.baseline.unique())):      
        basefull = AZ2SMT[base[:2]]+'-'+AZ2SMT[base[3:]]
        if ('JCMT' in basefull) or (('APEX' in basefull) and ('ALMA' not in basefull)) :
            plt.errorbar(foo[foo.baseline==base].uvdist/1e3,foo[foo.baseline==base].ampdb,
                         bars_on*foo[foo.baseline==base].sigma,fmt='d',ms=size_dots_redundant,
                         color=current_palette[basefull],label=basefull,elinewidth=line_width,
                        capsize=capsize,mec=mark_edge_color,ecolor=line_color,mew=mark_edge_width)   
    plt.yscale(yscale)
    plt.xlabel('uv distance (G$\lambda$)',fontsize=fontsize,fontname=fontname,fontweight=fontweight)
    plt.ylabel('Correlated Flux Density (Jy)',fontsize=fontsize,fontname=fontname,fontweight=fontweight)
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.tick_params(axis='both', which='both',direction="in", labelsize=fontsize,top=True,right=True)
    #plt.tick_params(axis="y",direction="in")
    #plt.tick_params(axis="x",direction="in")
    plt.xticks(fontname=fontname,fontsize=ticks_fontsize,fontweight=fontweight)
    plt.yticks(fontname=fontname,fontsize=ticks_fontsize,fontweight=fontweight)
    plt.minorticks_on()
    if ticks_in_style:
        plt.tick_params(axis="y",direction="in", pad=-28)
        plt.tick_params(axis="x",direction="in", pad=-16)
    if legend:
        plt.legend(bbox_to_anchor=(1.0, 1.0))
    if savefig!='':
        plt.savefig(savefig,bbox_inches='tight') 
    plt.show()