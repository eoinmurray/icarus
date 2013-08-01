

import numpy as np 
import matplotlib.pyplot as plt 
from mpl_toolkits.axes_grid1 import Grid



def normalize(arr):
    
    x = arr[:,0]
    y = arr[:,1]
    
    hold_max = []
    hold_int = []
    
    pulse_width = 25
    
    for j in xrange(int(x.max()/pulse_width)):
        minIdx = np.abs(x - pulse_width*j).argmin()
        maxIdx = np.abs(x - pulse_width*(j+1)).argmin()
        peakX = x[minIdx: maxIdx]
        peakY = y[minIdx:maxIdx]	
        
        if j != 6:
            hold_max.append( np.max(peakY) )
            hold_int.append( np.sum(peakY) )
        else:
            delay_peak = np.sum(peakY)

    y = y/np.mean(hold_max)

    return np.array(np.vstack((x,y)).T), calculate_g2(delay_peak, hold_int)



def calculate_g2(delay_peak, hold_int):
    
    if np.array(hold_int).mean() > 0:
        g2 = delay_peak/np.array(hold_int).mean()
        g2 = np.around(g2, decimals=3)
        return g2
    else:
        return 0

    

def plot_corrs(arr11, arr12, arr21, arr22, arr31, arr32, title):
    delay = 180 - 20
    x_min = - 100
    x_max = 100
    
    arr11, g2_11 = normalize(arr11)
    arr12, g2_12 = normalize(arr12)
    arr21, g2_21 = normalize(arr21)
    arr22, g2_22 = normalize(arr22)
    arr31, g2_31 = normalize(arr31)
    arr32, g2_32 = normalize(arr32)
    
    grect = (g2_11 - g2_12) / (g2_11 + g2_12)
    gdiag = (g2_21 - g2_22) / (g2_21 + g2_22)
    gcirc = (g2_31 - g2_32) / (g2_31 + g2_32)
    fidelity = (1 + grect + gdiag - gcirc)/4

    fig = plt.figure(1, (12, 5))
    fig.subplots_adjust(left=0.05, right=0.98)
    
    fig.suptitle('Fidelity: ' + np.array(fidelity).astype('|S5').tostring() + ', ' + title)
    
    grid = Grid(fig, 111, nrows_ncols = (1, 3), axes_pad = 0.3, label_mode = 'l')
    
    grid[0].plot(arr11[:,0]  - delay, arr11[:,1], 'b-', arr12[:,0] - delay, arr12[:,1], 'r-')
    grid[0].set_xlim([x_min, x_max])
    grid[0].set_ylabel('Counts', fontsize = 14) ; grid[0].set_xlabel('$\\tau(ns)$', fontsize=14)
    grid[0].legend(['HH', 'HV'])
    
    grid[1].plot(arr21[:,0]  - delay, arr21[:,1], 'b-', arr22[:,0] - delay, arr22[:,1], 'r-')
    grid[1].set_xlim([x_min, x_max])
    grid[1].set_xlabel('$\\tau(ns)$', fontsize=14)
    grid[1].legend(['DA', 'DD'])
    
    grid[2].plot(arr31[:,0]  - delay, arr31[:,1], 'b-', arr32[:,0] - delay, arr32[:,1], 'r-')
    grid[2].set_xlim([x_min, x_max])
    grid[2].set_xlabel('$\\tau(ns)$', fontsize=14)
    grid[2].legend(['LL', 'LR'])

    plt.show()
    
    
def plot_by_folder(name, title = ''):
    plot_corrs(
        np.loadtxt('out/2013-08-01/'+name+'/linear D1D3.txt', delimiter=','),
        np.loadtxt('out/2013-08-01/'+name+'/linear D2D3.txt', delimiter=','),
        np.loadtxt('out/2013-08-01/'+name+'/diag D1D3.txt', delimiter=','),
        np.loadtxt('out/2013-08-01/'+name+'/diag D2D3.txt', delimiter=','),
        np.loadtxt('out/2013-08-01/'+name+'/circ D1D3.txt', delimiter=','),
        np.loadtxt('out/2013-08-01/'+name+'/circ D2D3.txt', delimiter=','),
        title
    )
    
if __name__ == "__main__":
	import sys
	plot_by_folder(str(sys.argv[1]))