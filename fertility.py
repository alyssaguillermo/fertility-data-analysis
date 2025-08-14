import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# set column names
columns = [
    'Season', 
    'Age', 
    'Childish Disease(s)?', 
    'Accident/Serious Trauma?', 
    'Surgical Intervention?', 
    'High Fevers in Last Year?', 
    'Alcohol Consumption Frequency', 
    'Smoking Habit', 
    'Number of Hours Spent Sitting a Day', 
    'Diagnosis'
]

# read txt file 
data = pd.read_csv(
    '/Users/alyssaguillermo/Downloads/python projects/fertility/fertility_Diagnosis.txt', 
    names=columns, 
    header=0
)

# convert normalized age (0–1) to real age (18–36)
data['Age'] = (data['Age'] * (36 - 18) + 18).round().astype(int)

# dictionaries to convert numerical values to strings
conversions = {
    'Season': {-1: 'Winter', -0.33: 'Spring', 0.33: 'Summer', 1: 'Fall'}, 
    'Childish Disease(s)?': {0: 'Yes', 1: 'No'}, 
    'Accident/Serious Trauma?': {0: 'Yes', 1: 'No'}, 
    'Surgical Intervention?': {0: 'Yes', 1: 'No'}, 
    'High Fevers in Last Year?': {-1: '< 3 months ago', 0: '> 3 months ago', 1: 'No'}, 
    'Smoking Habit': {-1: 'Never', 0: 'Occasionally', 1: 'Daily'}, 
    'Diagnosis': {'N': 'Normal', 'O': 'Altered'}
}
alcohol_conversions = {
    0.20: 'Several times a day',
    0.40: 'Every day',
    0.60: 'Several times a week',
    0.80: 'Once a week',
    1.0: 'Hardly ever/Never'
}

# convert normalized sitting hours (0-1) to real sitting hours (0-16)
normalized = data['Number of Hours Spent Sitting a Day'] 
# min and max of real (original) sitting hours 
min_hours = 0
max_hours = 16
# denormalize sitting hours
real_hours = normalized * (max_hours - min_hours) + min_hours
data['Number of Hours Spent Sitting a Day'] = real_hours.round().astype(int)

# apply dictionary conversions
for col, mapping in conversions.items(): 
    data[col] = data[col].replace(mapping)
data['Alcohol Consumption Frequency'] = data['Alcohol Consumption Frequency'].round(2).replace(alcohol_conversions)

# print updated data
print(data)

# save as csv file 
data.to_csv('/Users/alyssaguillermo/Downloads/python projects/fertility/fertility_Diagnosis_updated.csv', index=False)

# read csv file
new_data = pd.read_csv('/Users/alyssaguillermo/Downloads/python projects/fertility/fertility_Diagnosis_updated.csv')

# get unique alcohol categories
alcohol_categories = new_data['Alcohol Consumption Frequency'].unique()

# convert to numpy array to process
diagnosis_array = new_data['Diagnosis'].to_numpy()
alcohol_array = new_data['Alcohol Consumption Frequency'].to_numpy()

# custom order of x-axis bars
custom_order = [
    'Hardly ever/Never',
    'Once a week',
    'Several times a week',
    'Every day',
    'Several times a day'
]

# keepcategories that actually exist in the data, in custom order
ordered_categories = [cat for cat in custom_order if cat in alcohol_categories]

# count occurrences in custom order
normal_counts = [np.sum((alcohol_array == cat) & (diagnosis_array == 'Normal')) 
                 for cat in ordered_categories]
altered_counts = [np.sum((alcohol_array == cat) & (diagnosis_array == 'Altered')) 
                  for cat in ordered_categories]

# count occurances for each diagnosis within each alcohol category
normal_counts = np.array([np.sum((alcohol_array == category) & (diagnosis_array == 'Normal')) for category in alcohol_categories])
altered_counts = np.array([np.sum((alcohol_array == category) & (diagnosis_array == 'Altered')) for category in alcohol_categories])

# set up bar positions
x = np.arange(len(alcohol_categories))
bar_width = 0.35

# plot bars
plt.figure(figsize=(10,6))
plt.bar(x - bar_width/2, normal_counts, width=bar_width, label='Normal', color='skyblue')
plt.bar(x + bar_width/2, altered_counts, width=bar_width, label='Altered', color='salmon')

# formatting
plt.title('Alcohol Consumption by Diagnosis')
plt.xlabel('Alcohol Consumption Frequency')
plt.ylabel('Count')
plt.xticks(x, alcohol_categories, rotation=30)
plt.legend()
plt.tight_layout()

# show plot
plt.show()