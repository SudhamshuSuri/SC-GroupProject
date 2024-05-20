import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('averages_weather_data.csv')

# Selecting relevant columns for correlation analysis
cols = ['Rain (mm)', 'Min Temp (°C)', 'Max Temp (°C)', 'Min Humidity (%)', 
        'Max Humidity (%)', 'Min Wind Speed (Kmph)', 'Max Wind Speed (Kmph)']

# Calculate correlation matrix
corr_matrix = df[cols].corr()

# Extract the correlation values for 'Rain (mm)' and sort in descending order
rain_corr = corr_matrix['Rain (mm)'].drop('Rain (mm)').sort_values()

# Print the ranked correlations
print("Correlation with 'Rain (mm)' ranked in descending order:")
print(rain_corr)

# Plotting the correlations with Rain (mm)
plt.figure(figsize=(10, 6))
sns.barplot(x=rain_corr.index, y=rain_corr.values, palette='viridis')
plt.axhline(0, color='grey', linestyle='--')
plt.xlabel('Variables')
plt.ylabel('Correlation with Rain (mm)')
plt.title('Correlation of Weather Parameters with Rain (mm)')
plt.xticks(rotation=45)
plt.show()
