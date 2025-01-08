import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

excel_file = 'OUTPUT/minmax_graph.xlsx'
df = pd.read_excel(excel_file, index_col=0)
df = df.sort_index()
df = df.applymap(lambda x: float(x.split(':')[0]) if x != "N" else np.nan)
cmap_name = "tab20c"
fig, ax = plt.subplots(figsize=(12, 10))
im_value = ax.imshow(df, cmap=cmap_name, interpolation='none', aspect='equal')
cbar_value = fig.colorbar(im_value, ax=ax, shrink=0.9)
ax.set_xticks(np.arange(len(df.columns)))
ax.set_yticks(np.arange(len(df.index)))
ax.set_xticklabels(df.columns, rotation=90, fontsize=10)
ax.set_yticklabels(df.index, fontsize=10)
ax.set_xticks(np.arange(len(df.columns)) - 0.5, minor=True)
ax.set_yticks(np.arange(len(df.index)) - 0.5, minor=True)
ax.grid(which="minor", color="black", linestyle='-', linewidth=0.5, alpha=0.8)
plt.rcParams.update({'font.size': 14})
plt.title('Overflows during a day', fontsize=14)
plt.xlabel('Target wards', fontsize=14)
plt.ylabel('Source wards', fontsize=14)
cbar_value.set_label('Residual capacity', fontsize=14)
plt.tight_layout()
plt.show()
