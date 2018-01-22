# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 13:00:23 2018

@author: Thabak
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

rainfall = pd.read_csv("Rainfall.csv")
rainfall.columns = rainfall.columns.str.title()
rainfall.Subdivision = rainfall.Subdivision.str.title()
#rainfall.Year = pd.to_datetime(rainfall.Year, format = '%Y')
temp = pd.read_csv("GTbyState.csv")

#print(rainfall.SUBDIVISION.unique())

state = 'Assam & Meghalaya'

rainfall_state = rainfall[rainfall.Subdivision == state]
rainfall_state = rainfall_state.loc[:,['Year','Annual']].reset_index(drop = True)
rainfall_state = rainfall_state[(rainfall_state.Year >= 1901)]
#print(rainfall_state)

temp_state = temp[(temp.Country == 'India') & (temp.State == 'Meghalaya')]
temp_state.dt = pd.to_datetime(temp_state.dt)
temp_state = temp_state.groupby(pd.PeriodIndex(temp_state.dt, freq ='A')).mean()
temp_state.index = temp_state.index.to_series().astype(str)
temp_state = temp_state.reset_index()
temp_state.rename(columns = {'dt':'Year'}, inplace = True)
temp_state.Year = [int(x) for x in temp_state.Year]
temp_state = temp_state[temp_state.Year>=1901].reset_index(drop = True)
#temp_state.columns[0] = 'Year'

plt.figure(figsize = (10,30), dpi = 100)
#host = fig.add_subplot(211)
#par = host.twinx()

fit = np.polyfit(rainfall_state.Year,rainfall_state.Annual,1)
temp_fit = np.polyfit(temp_state.Year, temp_state.AverageTemperature,1)

rain = plt.subplot(211)
plt.title('Changing Weather in Meghalaya')
rain.spines['right'].set_visible(False)
rain.spines['top'].set_visible(False)
rain.spines['bottom'].set_visible(False)
rain.tick_params(bottom = False)
#rain.spines['top'].set_visible(False)
plt.plot(rainfall_state.Year,rainfall_state.Annual,'o', color = 'skyblue', label = '_nolabel_')
plt.ylabel('Rainfall per year (mm)')
l1, = plt.plot(rainfall_state.Year, 
                   fit[0]*rainfall_state.Year + fit[1],'--',
                   color = 'blue', alpha = 0.5,
                   label = 'Trend in rainfall')
#plt.legend(frameon = False)
for label in rain.get_xticklabels():
    label.set_visible(False)
#rain.get_xticklabels().set_visible(False)
temp = plt.subplot(212, sharex = rain)
plt.plot(temp_state.Year,temp_state.AverageTemperature,'o', color = 'red', alpha = 0.5, label = '_nolabel_')
plt.ylabel('Temperature ($^o$C)')
l2, = plt.plot(temp_state.Year,
         temp_fit[0]*temp_state.Year + temp_fit[1],'--',
         color = 'red', alpha = 0.5,
         label = 'Trend in temperature')
temp.spines['right'].set_visible(False)
temp.spines['top'].set_visible(False)
plt.legend(handles = [l1,l2],frameon = False, loc = 4)

## Decade Year Averages
#rainfall_decade = rainfall[rainfall.Subdivision == state]
#rainfall_decade = rainfall_decade.loc[:,['Year','Annual']].reset_index(drop = True)
#rainfall_decade = rainfall_decade[(rainfall_state.Year >= 1901) & (rainfall_decade.Year < 2011)]
#rainfall_decade.Year = pd.to_datetime(rainfall_decade.Year.astype(str))
#rainfall_decade = rainfall_decade.set_index('Year')
#rainfall_decade = rainfall_decade.groupby((rainfall_decade.index.year//10)*10).sum()
#
#plt.figure()
#plt.bar(rainfall_decade.index,rainfall_decade.Annual)
#


#line1, = host.plot(rainfall_state.Year,rainfall_state.Annual,'o', color = 'skyblue')
#line1, = host.plot(rainfall_state.Year, 
#                   fit[0]*rainfall_state.Year + fit[1],'--',
#                   color = 'green')
#line2, = par.plot(temp_state.Year,temp_state.AverageTemperature,'-', color = 'red', alpha = 0.5)
#host.axis["left"].label.set_color(line1.get_color())
#host.set_ylim(1000,4000)
#par.set_ylim(25,30)