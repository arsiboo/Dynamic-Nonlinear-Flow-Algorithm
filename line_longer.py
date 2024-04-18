import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Ward selection
wards = ["EMERGENCY DEPARTMENT", "Medicinavdelning 30 E", "Infektionsavdelning 30 F"]
colors = ['darkviolet', 'limegreen', 'dodgerblue']

# Initialize an empty figure
plt.figure(figsize=(12, 6))

# Define the window size for the moving average
window_size = 1

for idx, ward in enumerate(wards):
    # Load the data from Excel
    df = pd.read_excel("OUTPUT/" + ward + ".xlsx")

    # Filter out values over 1000 or less than -1000 in 'residual capacity'
    df = df[(df['residual capacity'] <= 1000) & (df['residual capacity'] >= -1000)]

    # Group by 'time' and compute the mean for each unique time value
    grouped = df.groupby('time').mean().reset_index()

    # Compute the moving average
    grouped['moving_avg'] = grouped['residual capacity'].rolling(window=window_size).mean()

    # Plotting the moving averages
    plt.plot(grouped['time'], grouped['moving_avg'], color=colors[idx], marker=' ', label=ward)

# Adjusting the x-axis ticks and labels
#plt.xticks(np.arange(len(grouped['time'])), grouped['time'])
plt.rcParams.update({'font.size': 10})  # Change 14 to your desired font size
plt.xlabel('Hours',fontsize=10)
plt.ylabel('Average Residual Capacity',fontsize=10)
plt.title('Average Residual Capacity for One Day (Moving Average = '+str(window_size)+')',fontsize=10)
plt.legend(fontsize=10)
plt.grid(True)
plt.tight_layout()  # Adjust the layout to avoid overlapping
plt.show()
