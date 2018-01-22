
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv('fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
df.Date = pd.to_datetime(df.Date)
df.Data_Value = df.Data_Value/10
## MAX NOT 2015

max_data = df[(df.Element == 'TMAX') & (df.Date.dt.year != 2015)]
max_data['day'] = max_data.Date.apply(lambda x: x.strftime('%m-%d'))
max_perday_tenyears = max_data.groupby('day',as_index = False).agg({'Data_Value': max})
# Removing Feb 29th
max_perday_tenyears = max_perday_tenyears[max_perday_tenyears.day != '02-29'].reset_index(drop = True)

## MIN NOT 2015

min_data = df[(df.Element == 'TMIN') & (df.Date.dt.year != 2015)]
min_data['day'] = min_data.Date.apply(lambda x: x.strftime('%m-%d'))
min_perday_tenyears = min_data.groupby('day',as_index = False).agg({'Data_Value': min})
# Removing Feb 29th
min_perday_tenyears = min_perday_tenyears[min_perday_tenyears.day != '02-29'].reset_index(drop = True)

# MAX and MIN for 2015
data2015 = df[df.Date.dt.year == 2015]

# max per day
max_perday_2015 = data2015[data2015.Element == 'TMAX'].groupby('Date', as_index = False).agg({'Data_Value': max})

# min per day
min_perday_2015 = data2015[data2015.Element == 'TMIN'].groupby('Date', as_index = False).agg({'Data_Value': min})

# Broken Records
broken_max_ind = []
broken_min_ind = []

for i in range(len(max_perday_2015)):
    if max_perday_tenyears.Data_Value[i] - max_perday_2015.Data_Value[i] < 0 :
        broken_max_ind.append(i)
    if min_perday_tenyears.Data_Value[i] > min_perday_2015.Data_Value[i] :
        broken_min_ind.append(i)

broken_max = max_perday_2015.iloc[broken_max_ind,1]
broken_min = min_perday_2015.iloc[broken_min_ind,1]

# Plotting
fig = plt.figure(figsize=(10,7), dpi=200)
plt.plot(max_perday_tenyears.Data_Value,
         '-', c = 'blue', alpha = 0.35,
         label = "Temperature range in 2005-2014 ")

plt.plot(min_perday_tenyears.Data_Value,
         '-', c = 'blue', alpha = 0.35, 
         label ='_nolegend_')

plt.gca().fill_between( range(len(max_perday_tenyears)),
        max_perday_tenyears.Data_Value,
        min_perday_tenyears.Data_Value,
        facecolor = 'blue',
        alpha = 0.15)

plt.xticks( np.linspace(15,15 + 30*11 , num = 12), 
           (r'Jan', r'Feb', r'Mar', r'Apr', r'May', r'Jun', r'Jul', r'Aug', r'Sep', r'Oct', r'Nov', r'Dec') )

#plt.yticks( np.linspace(-40,-40 + 4*20, num = 5),
#           (r'-40($^\circ$C)',r'-20($^\circ$C)',r'0($^\circ$C)',r'20($^\circ$C)',r'40($^\circ$C)'))

plt.scatter(broken_max_ind, broken_max, 
            s = 10, c = 'red', 
            label = 'Hotter in 2015')

plt.scatter(broken_min_ind, broken_min, 
            s = 10, c = 'green',
            label = 'Colder in 2015')
#plt.ylim(-500,500)
plt.title('Extreme Weather in 2015 (Ann Arbor, USA)')
plt.legend(loc = 4, frameon = False)

# Changing the y ticks
ax = fig.gca()
ylabel = []
for item in ax.get_yticks():
    ylabel.append(str(int(round(item))) + r'$^\circ$C')
ax.set_yticklabels(ylabel)


# Getting rid of the frame
for spine in plt.gca().spines.values():
    spine.set_visible(False)


#saving the plot to a png file
plt.savefig('test1.png')

    