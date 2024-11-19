# -*- coding: utf-8 -*-
"""ENG_220_project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RT3ePyhERXRieu12iabaNx2Zgihj31kQ
"""

import pandas as pd
import requests

# Define the raw URL for the CSV file
file_url = "https://raw.githubusercontent.com/BlassMolina03/ENG-220-MATLAB-PROJECTS/main/Data%20Sheet%201.csv"

# Function to read a large or potentially malformed CSV file
def read_large_csv(url):
    try:
        # Attempt to read the CSV in chunks
        chunk_size = 1000  # Number of rows per chunk
        chunks = pd.read_csv(url,
                             encoding='ISO-8859-1',  # Handle potential encoding issues
                             sep=',',  # Comma is the default separator
                             on_bad_lines='skip',  # Skip lines that can't be parsed
                             chunksize=chunk_size)  # Read in chunks

        # Concatenate all chunks into a single DataFrame
        df_list = []
        for chunk in chunks:
            df_list.append(chunk)

        df = pd.concat(df_list, ignore_index=True)
        print("Data loaded successfully!")
        return df

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Read the file from the URL
df = read_large_csv(file_url)

# If the dataframe is loaded successfully, show the first few rows
if df is not None:
    print(df.head())
else:
    print("Failed to load the data.")

# Remove rows with missing values
df_cleaned = df.dropna()

# Save the cleaned dataset to a new file (optional)
df_cleaned.to_csv('Cleaned_Data.csv', index=False)

# Display basic information about the cleaned dataset
df_cleaned.info()

# Check for missing values again to confirm cleanup
print(df_cleaned.isnull().sum())

# Display the first few rows of the cleaned dataset
print(df_cleaned.head())

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure 'Incident Date' is converted to datetime
df['Incident Date'] = pd.to_datetime(df['Incident Date'], errors='coerce')

# Drop rows with invalid dates
df = df.dropna(subset=['Incident Date'])

# Extract day of the week without overwriting 'Incident Date'
df['day_of_week'] = df['Incident Date'].dt.day_name()

# Get the peak day of the week
day_of_week_counts = df['day_of_week'].value_counts()
peak_day = day_of_week_counts.idxmax()
peak_day_value = day_of_week_counts.max()

# Plot incidents by day of the week
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='day_of_week', order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
plt.title(f'Gun Violence Incidents by Day of the Week (Peak: {peak_day} - {peak_day_value} incidents)')
plt.xlabel('Day of the Week')
plt.ylabel('Number of Incidents')
plt.xticks(rotation=45)
plt.show()

# Create a separate DataFrame for resampling
df_resampled = df.copy()
df_resampled.set_index('Incident Date', inplace=True)

# Resample data by month to get the count of incidents per month
monthly_trend = df_resampled.resample('M').size()

# Convert the resampled data to a DataFrame for easy access
monthly_trend_df = monthly_trend.reset_index(name='Number of Incidents')

# Get the peak and bottom months
peak_month = monthly_trend_df.loc[monthly_trend_df['Number of Incidents'].idxmax()]
bottom_month = monthly_trend_df.loc[monthly_trend_df['Number of Incidents'].idxmin()]

# Plot the monthly trend
plt.figure(figsize=(14, 7))
plt.plot(monthly_trend.index, monthly_trend.values, marker='o', linestyle='-')
plt.title(
    f'Monthly Trend of Gun Violence Incidents\n'
    f'Peak: {peak_month["Incident Date"].strftime("%B %Y")} ({peak_month["Number of Incidents"]} incidents), '
    f'Bottom: {bottom_month["Incident Date"].strftime("%B %Y")} ({bottom_month["Number of Incidents"]} incidents)'
)
plt.xlabel('Date')
plt.ylabel('Number of Incidents')
plt.grid(True)
plt.show()

# Print the peak and bottom months
print("Peak Month:", peak_month)
print("Bottom Month:", bottom_month)

import textwrap

# Wrap long city or county names for readability
df['City Or County'] = df['City Or County'].apply(lambda x: '\n'.join(textwrap.wrap(x, width=15)))

plt.figure(figsize=(12, 30))
sns.countplot(
    data=df,
    y='City Or County',
    order=df['City Or County'].value_counts().index
)

plt.title('Gun Violence Incidents by City or County', fontsize=16)
plt.xlabel('Number of Incidents', fontsize=12)
plt.ylabel('City or County', fontsize=12)

# Adjust the spacing between y-axis labels
plt.gca().tick_params(axis='y', labelsize=10, pad=10)

plt.tight_layout()  # Automatically adjusts subplot parameters for better fit
plt.show()

# Count incidents by participant gender
gender_counts = df['Participant Gender'].value_counts()

plt.figure(figsize=(8, 8))
plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Gun Violence Incidents by Participant Gender')
plt.show()

plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='Participant Age Group', order=df['Participant Age Group'].value_counts().index)
plt.title('Gun Violence Incidents by Participant Age Group')
plt.xlabel('Age Group')
plt.ylabel('Number of Incidents')
plt.show()