import os
import sys
import numpy as np

def calculate_g2(delay_peak, hold_int):
    
    if np.array(hold_int).mean() > 0:
        g2 = delay_peak/np.array(hold_int).mean()
        g2 = np.around(g2, decimals=3)
        return g2
    else:
        return 0

    

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


def get_deg_of_corr(arr11, arr12, arr21, arr22, arr31, arr32):
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
        
    return [grect, gdiag, gcirc]

def get_corr_by_folder(full_name):

    return get_deg_of_corr(
        np.loadtxt(full_name + '/linear D1D3.txt', delimiter=','),
        np.loadtxt(full_name + '/linear D2D3.txt', delimiter=','),
        np.loadtxt(full_name + '/diag D1D3.txt', delimiter=','),
        np.loadtxt(full_name + '/diag D2D3.txt', delimiter=','),
        np.loadtxt(full_name + '/circ D1D3.txt', delimiter=','),
        np.loadtxt(full_name + '/circ D2D3.txt', delimiter=','),
    )

def get_data(rootdir):

    hold_outfile = []
    hold_crosstau = []
    
    for root, subFolders, files in os.walk(rootdir):
    
        outfileName = os.path.join(root, "params.txt")
    
        if os.path.exists(outfileName):
            params = np.genfromtxt(outfileName, dtype=str, delimiter=',')
            crosstau = float(params[:,1][params[:,0]=='crosstau'][0])
            
            hold_crosstau.append(crosstau)
            hold_outfile.append(root)
    
            
    data = np.vstack((hold_crosstau, hold_outfile)).T        
    
    idx = np.argsort(data[:,0].astype(float))
    
    data = data[idx]
    
    degree_of_corrs = np.array([get_corr_by_folder(d[1]) for d in data])
    
    hold_crosstau = data[:,0]
    
    grect = degree_of_corrs[:,0]
    gdiag = degree_of_corrs[:,1]
    gcirc = degree_of_corrs[:,2]
    
    return [hold_crosstau, [grect, gdiag, gcirc]]
