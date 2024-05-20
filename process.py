import csv
from collections import defaultdict

# Function to calculate averages of columns with integer data
def calculate_averages(data):
    columns = ['Rain (mm)', 'Min Temp (°C)', 'Max Temp (°C)', 'Min Humidity (%)', 'Max Humidity (%)', 'Min Wind Speed (Kmph)', 'Max Wind Speed (Kmph)']
    averages = {col: 0 for col in columns}

    for col in columns:
        total = 0
        count = 0
        for row in data:
            try:
                value = float(row[col])
                total += value
                count += 1
            except ValueError:
                continue
        averages[col] = total / count if count > 0 else 0

    return averages

# Function to group data by district and mandal and calculate averages
def group_and_calculate_averages(filename):
    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        grouped_data = defaultdict(list)

        for row in csv_reader:
            key = (row['District'], row['Mandal'])
            grouped_data[key].append(row)

    averages_by_group = {}
    for key, rows in grouped_data.items():
        averages_by_group[key] = calculate_averages(rows)

    return averages_by_group, csv_reader.fieldnames

# Function to write grouped averages to a new CSV file
def write_averages_to_csv(averages_by_group, fieldnames, output_filename):
    with open(output_filename, mode='w', newline='') as file:
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()

        for (district, mandal), averages in averages_by_group.items():
            average_row = {field: '' for field in fieldnames}
            average_row['District'] = district
            average_row['Mandal'] = mandal
            for col, avg in averages.items():
                average_row[col] = f"{avg:.2f}"
            csv_writer.writerow(average_row)

# Main execution
input_filename = 'weather_data_2.csv'
output_filename = 'averages_weather_data_test.csv'

averages_by_group, fieldnames = group_and_calculate_averages(input_filename)
write_averages_to_csv(averages_by_group, fieldnames, output_filename)

print(f"Averages have been written to {output_filename}")
