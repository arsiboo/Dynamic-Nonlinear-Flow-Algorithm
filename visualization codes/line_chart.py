import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df_all = pd.read_csv("OUTPUT/wards_behaviour.csv")
df_all['residual capacity'] = pd.to_numeric(df_all['residual capacity'], errors='coerce')
#wards = ["EMERGENCY DEPARTMENT", "Medicinavdelning 30 E", "Infektionsavdelning 30 F"]
wards = ["Emergency Department", "Medical Ward", "Infectious Diseases Unit"]

colors = ['darkviolet', 'limegreen', 'dodgerblue']
plt.figure(figsize=(12, 6))
window_size = 20

for idx, ward in enumerate(wards):
    df = df_all[df_all['ward'] == ward]
    df = df[(df['residual capacity'] <= 1000) & (df['residual capacity'] >= -1000)]
    df = df.dropna(subset=['residual capacity'])
    grouped = df.groupby('time')['residual capacity'].mean().reset_index()
    grouped['moving_avg'] = grouped['residual capacity'].rolling(window=window_size).mean()
    plt.plot(grouped['time'], grouped['moving_avg'], color=colors[idx], marker=" ", label=ward)

plt.rcParams.update({'font.size': 14})
plt.xlabel('Hours', fontsize=14)
plt.ylabel('Average Residual Capacity', fontsize=14)
plt.title('Average Residual Capacity for One Day (Moving Average = ' + str(window_size) + ')', fontsize=14)
plt.legend(fontsize=14)
plt.grid(True)
plt.tight_layout()
plt.show()
