import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the Excel file into a DataFrame
excel_file = 'OUTPUT/minmax_graph.xlsx'
df = pd.read_excel(excel_file, index_col=0)
df = df.sort_index()

# Define the list of vertex names to drop with capitalized first letters
#vertices_to_drop = ["Source", "Sink"]

# Drop the specified rows and columns
#df = df.drop(vertices_to_drop, axis=0)  # Drop rows
#df = df.drop(vertices_to_drop, axis=1)  # Drop columns

# Replace non-numeric values (e.g., 'N') with NaN
df = df.applymap(lambda x: float(x.split(':')[0]) if x != "N" else np.nan)

# Use a suitable colormap
cmap_name = "tab20c"

# Create a figure and subplot for the values
fig, ax = plt.subplots(figsize=(12, 10))
im_value = ax.imshow(df, cmap=cmap_name, interpolation='none', aspect='equal')

# Add a color bar
cbar_value = fig.colorbar(im_value, ax=ax, shrink=0.9)

# Customize axis labels and ticks
ax.set_xticks(np.arange(len(df.columns)))
ax.set_yticks(np.arange(len(df.index)))
ax.set_xticklabels(df.columns, rotation=90, fontsize=8)
ax.set_yticklabels(df.index, fontsize=8)

# Add grid lines with less transparency (alpha=0.8)
ax.set_xticks(np.arange(len(df.columns)) - 0.5, minor=True)
ax.set_yticks(np.arange(len(df.index)) - 0.5, minor=True)
ax.grid(which="minor", color="black", linestyle='-', linewidth=0.5, alpha=0.8)

# Set plot title and labels
plt.rcParams.update({'font.size': 10})  # Change 14 to your desired font size
plt.title('Overflows during a day', fontsize=10)
plt.xlabel('Target wards', fontsize=10)
plt.ylabel('Source wards', fontsize=10)

# Add a color bar text
cbar_value.set_label('Residual capacity', fontsize=10)

# Display the plot
plt.tight_layout()
plt.show()
