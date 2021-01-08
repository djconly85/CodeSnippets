# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 14:12:49 2021

@author: dconly
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mticker

mpl.rcParams['font.size'] = 6.5

x = np.array(range(1000, 5000, 500))
y = 37*x

fig, [ax1, ax2, ax3] = plt.subplots(1,3)

ax1.plot(x,y, linewidth=5, color='green')
ax2.plot(x,y, linewidth=5, color='red')
ax3.plot(x,y, linewidth=5, color='blue')

label_format = '{:,.0f}'

# nothing done to ax1 as it is a "control chart."

# fixing yticks with "set_yticks"
ticks_loc = ax2.get_yticks().tolist()
ax2.set_yticks(ax1.get_yticks().tolist())
ax2.set_yticklabels([label_format.format(x) for x in ticks_loc])

# fixing yticks with matplotlib.ticker "FixedLocator"
ticks_loc = ax3.get_yticks().tolist()
ax3.yaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
ax3.set_yticklabels([label_format.format(x) for x in ticks_loc])

# fixing xticks with FixedLocator but also using MaxNLocator to avoid cramped x-labels
ax3.xaxis.set_major_locator(mticker.MaxNLocator(3))
ticks_loc = ax3.get_xticks().tolist()
ax3.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
ax3.set_xticklabels([label_format.format(x) for x in ticks_loc])

fig.tight_layout()
plt.show()