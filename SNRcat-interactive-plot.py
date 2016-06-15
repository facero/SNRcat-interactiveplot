#
#
# 10 June, 2016 F. Acero
#
# Code to produce interactive html plot where you can zoom and pan in the galactic plane
# to explore the population of known supernova remnant (SNRs) shown here as radio.
# When overing your mouse over a disk, a pop-up window shows a list of information (e.g. age, dist, whatever)
# In this code the age and distances are faked but can be linked to any database.
# The interactive part is handled by the mpld3 module available described here:
# https://mpld3.github.io/


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mpld3

#mpld3.enable_notebook() # to enable interactive plots to show in Jupyter notebooks




def create_df(name, age, dist ):
    """
    Create panda data frame to show some additional infos on plots
    """
    df = pd.DataFrame(index=range(len(name)))
    df['Age'] = age   #.flatten()
    df['Dist'] = dist #.flatten()

    #URLs do not work that way
    #    df['URL']      = ['<IMG SRC="image.gif" ALT="some text" WIDTH=32 HEIGHT=32>']*len(index)
    
    labels=[]
    for i in range(len(df)):
        label = df.ix[[i], :].T
        label.columns = name
    #    # .to_html() is unicode; so make leading 'u' go away with str()
        labels.append(str(label.to_html()))
    
    return labels


def get_SNR(myfile):
    """
    Reading information from a file to get positions and extension
    """
    name=np.genfromtxt(myfile,unpack=True,usecols=0,dtype='string')
    glsnr,gbsnr,radius=np.genfromtxt(myfile,unpack=True,usecols=(1,2,3),dtype='float')

    return name,glsnr,gbsnr,radius


# Define some CSS to control our custom labels
css = """
table
{
  border-collapse: collapse;
}
th
{
  color: #ffffff;
  background-color: #000000;
}
td
{
  background-color: #cccccc;
}
table, th, td
{
  font-family:Arial, Helvetica, sans-serif;
  border: 1px solid black;
  text-align: right;
}
"""


 
def plot_SNR(ax,name,x1,y1,r1):
    """
    Plot a disk for each SNR based on their radio properties (size and extension)    
    """
    circleSNR=plt.Circle((x1,y1),r1,color='green',alpha=0.65)
    ax.add_patch(circleSNR)
    return circleSNR



#--------------
#--------------
# Main section
#--------------
#--------------

#Calling get_SNR() to get all the variables
names,glsnr,gbsnr,radius  =   get_SNR('SNRcat.txt')


fig = plt.figure(figsize=(18,2))
ax = fig.add_subplot(111)

ax.set_aspect(1)

ax.set_xlim(-180,180)
ax.set_ylim(-20,20) 

ax.set_xlabel("Gal longitude",size=20)
ax.set_ylabel("Gal latitude",size=20)

x=glsnr
ind = x>180
x[ind] -=360    # scale conversion to [-180, 180]



for i,name in enumerate(names):
#  print name, x[i],gbsnr[i],radius[i]
    myplot=plot_SNR(ax,name,x[i],gbsnr[i],radius[i])
    label=create_df(np.asarray([name.replace('SNR','G')]),np.random.rand(1),np.random.rand(1) )
    tooltip= mpld3.plugins.PointHTMLTooltip(myplot, label, voffset=10, hoffset=10)
    mpld3.plugins.connect(fig, tooltip)   # connect each disk with a pop-up window


plt.gca().invert_xaxis() # Reverse X axis after everything is plotted 


#mpld3.display(fig) to display the plot in Jupyter notebooks
mpld3.save_html(fig,'SNRCAT-interactive-results.html')


#--------------
#END
#--------------

