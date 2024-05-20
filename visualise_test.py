import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Read the CSV file
df = pd.read_csv('averages_weather_data.csv')

# Selecting columns for 3D scatter plot
cols = ['Rain (mm)', 'Min Temp (°C)', 'Max Wind Speed (Kmph)', 'Min Humidity (%)', 'Max Humidity (%)', 'District', 'Mandal', 'Max Temp (°C)', 'Min Temp (°C)', 'Min Wind Speed (Kmph)']

# Ensure that all values are numeric (drop rows with non-numeric values in the selected columns)
#df = df[cols].dropna()

# Calculate average humidity
df['Avg Humidity (%)'] = (df['Min Humidity (%)'] + df['Max Humidity (%)']) / 2
df['AvgTemp (°C)'] = (df['Min Temp (°C)'] + df['Max Temp (°C)']) / 2
df['Avg Wind Speeds'] = (df['Min Wind Speed (Kmph)'] + df['Max Wind Speed (Kmph)']) / 2
# Normalize the average humidity for color mapping
norm = plt.Normalize(df['Avg Humidity (%)'].min(), df['Avg Humidity (%)'].max())
colors = cm.coolwarm(norm(df['Avg Humidity (%)']))

# Create figure and 3D axes
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot data points
sc = ax.scatter(df['Rain (mm)'], df['AvgTemp (°C)'], df['Avg Wind Speeds'], 
                c=colors, s=100, alpha=0.6, edgecolors='w')

# Set labels and title
ax.set_xlabel('Rain (mm)')
ax.set_ylabel('Avg Temp (°C)')
ax.set_zlabel('Avg Wind Speed (Kmph)')
plt.title('3D Scatter Plot of Rain, Avg Temp, Avg Wind Speed for Each District and Mandal')

ax.set_box_aspect([1,1,1])

# Add annotations for each point
'''for i in range(len(df)):
    ax.text(df['Rain (mm)'].iloc[i], df['Min Temp (°C)'].iloc[i], df['Max Wind Speed (Kmph)'].iloc[i], 
            f"{df['District'].iloc[i]}, {df['Mandal'].iloc[i]}", size=1, zorder=1, color='k')

'''# Show plot
plt.show()
