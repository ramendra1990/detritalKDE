# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 11:08:44 2020

@author: ramendra
"""



def silverman_bw(x):
    import numpy as np
    s = np.nanstd(x)
    IQR = np.nanquantile(df.iloc[:, 0], .75) - np.nanquantile(df.iloc[:, 0], .25)
    A = np.min([s, IQR / 1.349])
    n = np.count_nonzero(~np.isnan(x))
    return 0.9 * A * (n ** (-0.2))

def kde_plot(df, bw, xmin, xmax, c, label = None):
    import matplotlib.pyplot as plt
    plt.xlim(xmin, xmax)
    
    
    kde = df.plot.kde(bw_method = bw, color = c, label = label)
    
    plt.tick_params(
        axis = 'y',
        which = 'both',
        right = False,
        left = False,
        labelleft = False)
    
    plt.ylabel('')
    
    ax1 = plt.gca()
    ax1.spines['right'].set_visible(False)
    ax1.spines["top"].set_visible(False)
    
    return kde
    
def endmembers(coords_kde, df_e, tolerance, noData = False):
    """ 
    Tolerance in percentage, i.e 5 percent or 1 percent
    """
    names = df_e.iloc[:, 0]
    sizes = []
    labels = []
    coords = []
    
    coords_x = coords_kde[:, 0]
    coords_y = coords_kde[:, 1]
    
    from sklearn.metrics import auc
    
    for j in range(len(names)):
        coords_x_j = coords_x[(coords_x >= df_e.iloc[j, 1]) & (coords_x <= df_e.iloc[j, 2])]
        coords_y_j = coords_y[(coords_x >= df_e.iloc[j, 1]) & (coords_x <= df_e.iloc[j, 2])]
        try:
            area = auc(coords_x_j, coords_y_j)
            if area > tolerance / 100.0:
                sizes.append(area)
                labels.append(names[j])
                coords.append([coords_x_j, coords_y_j])
        except ValueError: # Usually occurs when the data range is not within the endmembers
            pass        
    
    if noData == True:
        from math import isclose
        if isclose(1, np.sum(np.array(sizes)), rel_tol = tolerance / 100.0):
            sizes = sizes
        else:
            sizes.append(1 - np.sum(np.array(sizes)))
            labels.append('Unknown')
            
    sizes = [asize / max(sizes) for asize in sizes]
        
    return sizes, labels, coords

#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

# file_path = filedialog.askopenfilename()

data = filedialog.askopenfilename(title='Select Datasheet', 
                                  filetypes=[("Comma-separated value files", "*.csv")])
df = pd.read_csv(data)


# end-members
# Condition, whether pie plot needed or not
con = input("Do you want to make a pie plot along with kde (y / n)? : ")

if con == 'y':
    # Making a color dictionary
    data_e = filedialog.askopenfilename(title='Select endmember File', 
                                    filetypes=[("Excel files", "*.xlsx")])
    df_e = pd.read_excel(data_e)
    colordict = {}
    name_of_endmembers = list(df_e.iloc[:, 0])
    # name_of_endmembers.append('Unknown')
    cmap = plt.cm.Paired
    colors = cmap(np.linspace(0., 1., len(name_of_endmembers)))
    for l,c in zip(name_of_endmembers,colors):
        colordict[l] = c

#%% Pllotting of kde with the pie plots

x_axis_label = input('Please provide x-axis label : If you need Latex formatted label, you can try something like - $\epsilon_{Nd}$. For quick help, see http://wch.github.io/latexsheet/ : ')

con_axislimit = input('Do you want automatic limit for x-axis or you want to provide? (y/n) : ')

if con_axislimit == 'y':
    xmin = min(df.min())
    xmax = max(df.max()) 
else:
    axis_limit = input('Please provide lower and upper limit of the x-axis in figure, separated with a comma(,) : ')
    axis_limit = axis_limit.split(',')
    xmin = int(axis_limit[0])
    xmax = int(axis_limit[1])
    

# --------------------------------------------------------------
# Selection of columns for which the plot is to be made
list_cols = []
indices = input("Please type the numbers of the columns you want to make the plots for. Numbers should be separated with comma (,). If you want to plot for all the columns, just type 'a'. : ")

indices = indices.split(',')
for ind in indices:
    try:
        list_cols.append(int(ind))
    except ValueError:
        pass

if len(list_cols) == 0:
    n = len(df.columns)
    list_cols = list(np.arange(0, n))
else:
    n = len(list_cols)


# --------------------------------------------------------------
# n = 1

# -------------------------------------------------------------------------

# -------------------------------------------------------------------------

if con == 'y':
    fig, ax = plt.subplots(figsize = (10, (n / 2) + 1.0))
    gs = gridspec.GridSpec(n, 2, wspace = 0.0, hspace = 0.0, 
                           width_ratios=[8, 1])
    fig_size = fig.get_size_inches()
    plt.subplots_adjust(top = 1 - (0.4 / fig_size[1]), 
                        bottom = 0.5 / fig_size[1])

else:
    
    # ---------------------------------------------------------------------
    # Condition, whether to combine 2, 3 columns of the datasheet, number-wise
    con_combine = input("Do you want to combine multiple column of the data-sheet (y / n)?: ")
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    if con_combine == 'y':
        cols = input("Please enter the numbers of the columns you want to combine. The numbers should be separated with comma(,). If you want multiple combinations of columns, separate the group of numbers with semi-columns(;) : ")
        cols = cols.split(';')
        indx = []
        for col in cols:
            col = col.split(',')
            for x in col:
                indx.append(int(x) - 1)
        for index in sorted(indx, reverse=True):
            del list_cols[index]    
        
        
        for col in cols:
            col = col.split(',')
            list_cols.append([int(x) - 1 for x in col])
            
        n = len(list_cols)
    # ----------------------------------------------------------------------    
    fig, ax = plt.subplots(figsize = (8, (n / 2) + 1.0))
    gs = gridspec.GridSpec(n, 1, wspace = 0.0, hspace = 0.0)
    fig_size = fig.get_size_inches()
    plt.subplots_adjust(top = 1 - (0.4 / fig_size[1]), 
                        bottom = 0.5 / fig_size[1])

#%% Actual data loop runs
list_labels = []   
bw = float(input("Please provide bandwidth for kde plot : "))
legend_pos = float(input("Please provide position of legend for individual plots. Position value should be between 0 (for leftmost) and 1 (for right most) : "))
for i in range(n):
    
    if con == 'y':
        plt.subplot(gs[2 * i])
    else:
        plt.subplot(gs[i])
            
    
    if type(list_cols[i]) != list:
        kde = kde_plot(df.iloc[:, list_cols[i]], bw, xmin, xmax, 'k')
        ax1 = plt.gca()
        ax1.set_ylim(bottom=0)
        ax1.spines['right'].set_visible(True)
        ax1.spines["top"].set_visible(True)
        # ax1.spines["left"].set_visible(False)
        
        txt = df.columns[list_cols[i]]
        txt1 = r'$n = $' + str(np.count_nonzero(~np.isnan(df.iloc[:, list_cols[i]])))
        
        ax1.text(legend_pos, 0.75, txt, transform = ax1.transAxes)
        ax1.text(0.9, 0.1, txt1, transform = ax1.transAxes)
    else:
        cs = ['r', 'g', 'b', 'k', 'y', 'm', 'c']
        n1 = 0
        for k in list_cols[i]:
            kde = kde_plot(df.iloc[:, k], bw, xmin, xmax, cs[n1])
            ax1 = plt.gca()
            ax1.set_ylim(bottom=0)
            ax1.spines['right'].set_visible(True)
            ax1.spines["top"].set_visible(True)
            n1 += 1
            
        plt.legend(ncol = 2, fontsize = 8)
            
        
    if i < n - 1:
        plt.tick_params(
        axis = 'x',
        which = 'both',
        bottom = True,
        top = False,
        labelbottom = False)
        
    else:
        plt.xticks(fontsize = 10)
        plt.xlabel(x_axis_label, fontsize = 12)
    
    
    
    if con == 'y':
        coords = kde.get_children()[0].get_path().vertices
        sizes, lb, coordinates = endmembers(coords, df_e, 5)
        m = 0
        for coord in coordinates:
            plt.fill_between(coord[0], coord[1], facecolor = colordict[lb[m]])
            # plt.fill_between(coord[0], coord[1], color = 'grey')
            m += 1
        
        plt.subplot(gs[(2 * i) + 1])
        
        
        # pie = plt.pie(sizes, labels = lb, autopct='%1.2f%%', radius = 1, 
        #         startangle = 90)
        pie = plt.pie(sizes, labels = lb, radius = 1, 
                startangle = 90)
        plt.axis('equal')
        
        
        for pie_wedge in pie[0]:
            end_member_label = pie_wedge.get_label()
            pie_wedge.set_facecolor(colordict[pie_wedge.get_label()])
            list_labels.append(end_member_label)
            # pie_wedge.set_label(None)
            # pie_wedge.set_facecolor(colordict[l] for l in lb)
        
        for t in pie[1]:
            # t.set_fontsize(8)
            t.remove()
        
    # for t1 in pie[2]:
    #     t1.set_fontsize(6)
    
# plt.suptitle('Constant Bandwidth = 0.2', fontsize = 12, y = 0.95)  
# plt.suptitle("Silverman's Bandwidth", fontsize = 12, y = 0.95)  
fig.add_subplot(111, frame_on=False)
plt.tick_params(labelcolor="none", bottom=False, left=False)

plt.ylabel('Density', labelpad = -10, fontsize = 12)

if con == 'y':
    unique_labels = list(set(list_labels))
    colors = [colordict[lab] for lab in unique_labels]
    from matplotlib.patches import Patch
    legend_elements = []
    for l,c in zip(unique_labels, colors):
        legend_elements.append(Patch(facecolor = c, label = l))
        
    horz_extent = input("Horizontal extent of the legend box in fraction : ")
    plt.legend(handles = legend_elements, 
                bbox_to_anchor=(0, 1 + (.1 / fig_size[1]), float(horz_extent), 0.2), 
                loc="lower left",
                mode="expand", borderaxespad = 0, 
                ncol = len(legend_elements))



