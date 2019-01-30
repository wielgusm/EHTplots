#PLOTTING COVERAGE IN UV PLANE IN EHT STYLE
#Maciek Wielgus 2018/12/06

import ehtim as eh
import numpy as np
import pandas as pd
#import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.transforms as mt
from matplotlib import rcParams

###################################
#SOME ASSUMPTIONS
###################################
figsize=(8,5.5) #size of the figure
#fontsize=15
#ticks_fontsize=14
rcParams['text.usetex']=True
rcParams['font.family']='sans-serif'
rcParams['font.sans-serif']='Latin Modern Roman'
# axes and tickmarks
rcParams['axes.labelsize']=15
#rcParams['axes.labelweight']=600
rcParams['axes.linewidth']=1.5
rcParams['xtick.labelsize']=14
rcParams['xtick.top']=True
rcParams['xtick.direction']='in'
rcParams['xtick.major.width']=1.2
rcParams['xtick.minor.width']=1.2
rcParams['xtick.minor.visible']=True
rcParams['ytick.labelsize']=14
rcParams['ytick.right']=True
rcParams['ytick.direction']='in'
rcParams['ytick.major.width']=1.2
rcParams['ytick.minor.width']=1.2
rcParams['ytick.minor.visible']=True
# points and lines
rcParams['lines.linewidth']=2.0
rcParams['lines.markeredgewidth']=0.5
rcParams['lines.markersize']=5
# points and lines
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
snr_cut=0. #make an snr threshold
ticks_in_style=False #Katie's style of ticks with labels inside the figure
#savefig='my_pretty_figure.pdf' #name / path to save the figure
grid_alpha=0.0
small_labelsize=14

def plot_coverage_uv(pathf,fontsize=15,ticks_fontsize=14, line_width=0.5,
            legend=False,label=True,fontname='Latin Modern Roman',mark_edge_color=[0,0,0,0.5],
            size_dots_primary=30, size_dots_redundant=30,
            mark_edge_width=0.5, xlim=[10,-10], ylim=[-10,10],
            yscale='log',ticks_in_style=False,figsize=(8,5.5),snr_cut=0,savefig='',fontweight='normal',circ_label=True,
            grid_alpha=grid_alpha,small_labelsize=small_labelsize):
    rgb = lambda x,y,z: (x/255.,y/255.,z/255.) 
    def merge_two_dicts(x, y):
        z = x.copy()   # start with x's keys and values
        z.update(y)    # modifies z with y's keys and values & returns None
        return z
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
                'LMT-SPT':'yellow',
                'LMT-PV':rgb(153, 102, 51),
                'SMA-SPT':'darkred',
                'JCMT-SPT':'darkred',
                'SMT-SPT':'salmon', 
                'PV-SPT':'saddlebrown',
                'PV-SMA':'tan',
                'JCMT-PV':'tan',
                'SMT-PV':rgb(179, 179, 0)}
    palette_dict_inv = {k.split('-')[1]+'-'+k.split('-')[0] : v for k, v in palette_dict.items()}
    current_palette = merge_two_dicts(palette_dict, palette_dict_inv)
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
    df=df[df.snr>snr_cut]

    plt.figure(figsize=figsize)
    plt.rcParams["font.weight"] = "normal"
    plt.rcParams["axes.labelweight"] = "normal"
    plt.grid(alpha=grid_alpha)

    df2 = df.copy()
    df2['u'] = -df['u']
    df2['v'] = -df['v']
    dataF = pd.concat([df,df2],ignore_index=True)
    dataF['u'] = dataF['u']/1e9
    dataF['v'] = dataF['v']/1e9
    foo = dataF
    
    #redundant baselines
    for base in sorted(list(foo.baseline.unique())):
        if len(base)==2:
            basefull = Z2SMT[base[0]]+'-'+Z2SMT[base[1]]
        else:    
            basefull = AZ2SMT[base[:2]]+'-'+AZ2SMT[base[3:]]
        #print(basefull,current_palette[basefull])
        if ('JCMT' in basefull) or (('APEX' in basefull) and ('ALMA' not in basefull)) :
            colorLoc=np.asarray([current_palette[basefull]])
            plt.scatter(foo[foo.baseline==base].u,foo[foo.baseline==base].v,
            s=size_dots_redundant,linewidths=line_width, edgecolors=mark_edge_color,c=colorLoc,label=basefull)
    
    #primary baselines
    for base in sorted(list(foo.baseline.unique())):
        if len(base)==2:
            basefull = Z2SMT[base[0]]+'-'+Z2SMT[base[1]]
        else:    
            basefull = AZ2SMT[base[:2]]+'-'+AZ2SMT[base[3:]]
        if ('JCMT' not in basefull) and (('APEX' not in basefull) or ('ALMA' in basefull)) :
            colorLoc=np.asarray([current_palette[basefull]])
            plt.scatter(foo[foo.baseline==base].u,foo[foo.baseline==base].v,
            s=size_dots_primary,c=colorLoc,linewidths=line_width, edgecolors=mark_edge_color,label=basefull)

    
    t= np.linspace(0,2*np.pi,256)
    uas = (1e3)*np.pi/180/60/60
    w0 = 1/(50*uas)
    w1 = 1/(25*uas)
    plt.axvline(0,linestyle='-',color= (0.5, 0.5, 0.5), zorder=0)
    plt.axhline(0,linestyle='-',color= (0.5, 0.5, 0.5), zorder=0)
    plt.plot(w0*np.sin(t),w0*np.cos(t),'--',color= (0.5, 0.5, 0.5),zorder=0)
    plt.plot(w1*np.sin(t),w1*np.cos(t),'--',color= (0.5, 0.5, 0.5),zorder=0)

    plt.axis('equal')
    plt.axis(xlim+ylim)
    r1 = 8.6; a1 = np.pi*(0.26)
    r2=4.4; a2=np.pi*0.26
    if circ_label:
        plt.text(r1*np.cos(a1),r1*np.sin(a1), '25 $\mu$as', fontsize=small_labelsize,rotation=42,fontname=fontname2)
        plt.text(r2*np.cos(a2),r2*np.sin(a2), '50 $\mu$as', fontsize=small_labelsize,rotation=42,fontname=fontname2)
    plt.gcf().subplots_adjust(left=0.3,top=0.95)
    labelfontsize=15
    arcfotsize=13

    plt.xlabel('u (G$\lambda$)',fontname=fontname,fontsize=fontsize)
    plt.ylabel('v (G$\lambda$)',fontname=fontname,fontsize=fontsize)
    plt.tick_params(axis='both', which='both',direction="in", labelsize=fontsize,top=True,right=True)
    plt.xticks(fontname=fontname,fontsize=ticks_fontsize,fontweight=fontweight)
    plt.yticks(fontname=fontname,fontsize=ticks_fontsize,fontweight=fontweight)
    plt.minorticks_on()
    
    if ticks_in_style:
        plt.tick_params(axis="y",direction="in", pad=-28)
        plt.tick_params(axis="x",direction="in", pad=-16)
    if legend:
        plt.legend(bbox_to_anchor=(1.0, 1.0),loc=2)
    if savefig!='':
        plt.savefig(savefig,bbox_inches='tight') 
    plt.show()