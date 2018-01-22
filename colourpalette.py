# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 09:30:42 2018

@author: Thabak
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# create data
x = np.random.rand(80) - 0.5
y = x+np.random.rand(80)
z = x+np.random.rand(80)
df = pd.DataFrame({'x':x, 'y':y, 'z':z})
 
# plot
#sns.lmplot( x='x',y = 'y', data=df, fit_reg=False, legend=False, palette="PuOr")
 
# reverse palette
#sns.lmplot( x='x', y='y', data=df, fit_reg=False, hue='x', legend=False, palette="PuOr_r")
#plt.figure(figsize = (10,1))
plt.imshow([[0.,1.], [0.,1.]], 
  cmap = plt.cm.RdBu, 
  interpolation = 'bicubic',
  aspect = 'auto'
)
for spine in plt.gca().spines.values():
    spine.set_visible(False)

plt.title('Comparison with mean')
plt.tick_params(left = False)
plt.xticks(np.linspace(-0.5,1.5,num=3),(r'Definitely Lower',r'Equal',r'Definitely Higher'))
ax = plt.gca()
ax.set_yticklabels([])