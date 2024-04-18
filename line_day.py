import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Ward selection
wards = ["EMERGENCY DEPARTMENT", "Medicinavdelning 30 E", "Infektionsavdelning 30 F"]
colors = ['darkviolet', 'limegreen', 'dodgerblue']

# Initialize an empty figure
plt.figure(figsize=(12, 6))

for idx, ward in enumerate(wards):
    # Load the data from Excel
    df = pd.read_excel("OUTPUT/" + ward + ".xlsx")

    # Group by 'time' and compute the mean for each unique time value
    grouped = df.groupby('time').mean().reset_index()

    # Plotting the average residual capacities
    plt.plot(grouped['time'], grouped['residual capacity'], color=colors[idx], marker=' ', label=ward)

# Adjusting the x-axis ticks and labels
plt.xticks(np.arange(len(grouped['time'])), grouped['time'])
plt.xlabel('Hours')
plt.ylabel('Average Residual Flow')
plt.title('Average Residual Flow for one day')
plt.legend()
plt.grid(True)
plt.tight_layout()  # Adjust the layout to avoid overlapping
plt.show()
