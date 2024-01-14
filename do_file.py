# %%
#import relevant libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import matplotlib.path as path
import pandas as pd
import seaborn as sns
import os
import statsmodels.api as sm

# %%
# Specify the path where the CSV files are located
csv_folder = "C:/Users/DONKAMS/Downloads/Income-Inequality-Analysis-with-Quantitative-Modeling/data"

# List all CSV files in the specified folder
csv_files = [file for file in os.listdir(csv_folder) if file.endswith(".csv")]

# Create an empty list to store DataFrame names
dataframe_names = []

# Create a dictionary to store DataFrames
dataframes = {}

# Iterate through the CSV files and import them into pandas DataFrames
for file in csv_files:
    # Extract the filename without extension to use as the DataFrame name
    dataset_name = os.path.splitext(file)[0]

    # Import the current CSV file into a pandas DataFrame
    df = pd.read_csv(os.path.join(csv_folder, file))

    # Store the DataFrame in the dictionary with the specified name
    dataframes[dataset_name] = df

    # Store the DataFrame name in the list
    dataframe_names.append(dataset_name)

# Display the list of DataFrame names
print("DataFrame Names:", dataframe_names)

# Access a specific DataFrame from the dictionary
# For example, to access the DataFrame named "example_dataset":
# example_dataset_df = dataframes["example_dataset"]


# %%
#Utilize the "A1 Descriptives" worksheet for initial descriptive statistics, focusing on variables such as year, region, and country.
df = dataframes["A1 Descriptives"]
# Display initial summary statistics
summary_statistics = df.describe()

# Display unique values in the 'year', 'region', and 'country' columns
unique_years = df['Year'].unique()
unique_regions = df['Region'].unique()
unique_countries = df['Country'].unique()

# Print the summary statistics and unique values
print("Summary Statistics:")
print(summary_statistics)

print("\nUnique Years:")
print(unique_years)

print("\nUnique Regions:")
print(unique_regions)

print("\nUnique Countries:")
print(unique_countries)


# %% [markdown]
# <h1 align = 'center'> Subset Selection </h1>

# %%
#Choose a subset of countries based on the research objectives.
#Select a consistent range of years for analysis.
df = dataframes["A1 Descriptives"]
# Define the subset of countries you want to analyze
selected_countries = ['Canada', 'Australia', 'China', 'Austria', 'United States', 'United Kingdom', 'France', 'Germany', 'India', 'Brazil',]

# Filter the DataFrame to include only the selected countries
df_subset_countries = df[df['Country'].isin(selected_countries)]

# Define the range of years for analysis
start_year = 2000
end_year = 2014

# Filter the DataFrame to include only the selected range of years
df_subset_years = df_subset_countries[(df_subset_countries['Year'] >= start_year) & (df_subset_countries['Year'] <= end_year)]

# show the result as a dataframe in pandas
df_subset_years

# %% [markdown]
# <h1 align = 'center'> Time Series Analysis </h1>

# %%
# Set up the panel data structure using the 'year' and 'country' columns
panel_data = df_subset_years.set_index(['Country', 'Year'])

# Use xtset-like functionality to define the panel structure
# This helps in informing the library about the panel structure for time series analysis
panel_data = panel_data.sort_index(level=['Country', 'Year'])

# Perform time series analysis using panel data methods, for example, fixed effects regression
# Replace 'dependent_variable' and 'independent_variable' with your actual variable names
model = sm.PanelOLS.from_formula('dependent_variable ~ independent_variable + EntityEffects', data=panel_data)
results = model.fit()

# Print the regression results
print(results.summary())

# %%
from statsmodels.formula.api import PanelOLS

# Set up the panel data structure using the 'year' and 'country' columns
panel_data = df_subset_years.set_index(['Country', 'Year'])

# Use xtset-like functionality to define the panel structure
# This helps in informing the library about the panel structure for time series analysis
panel_data = panel_data.sort_index(level=['Country', 'Year'])

# Perform time series analysis using panel data methods, for example, fixed effects regression
# Replace 'dependent_variable' and 'independent_variable' with your actual variable names
model = PanelOLS.from_formula('dependent_variable ~ independent_variable + EntityEffects', data=panel_data)
results = model.fit()

# Print the regression results
print(results.summary())

# %%
# Visualize time series using seaborn
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_subset_years, x='Year', y='Mean equivalized income', hue='Country', marker='o')
plt.title('Time Series Analysis for Selected Countries')
plt.xlabel('Year')
plt.ylabel('Mean equivalized income')
plt.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# %%
# Visualize time series using seaborn
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_subset_years, x='Year', y='# Observations \nPrimary\nIncome', hue='Country', marker='o')
plt.title('Time Series Analysis for Number of observations for Primary Income')
plt.xlabel('Year')
plt.ylabel('# Observations \nPrimary\nIncome')
plt.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# %%
# analyze Gini coefficients and overall fiscal redistribution measures within the chosen subset
# Assuming 'A2 Ginis and FRD' is the name of the worksheet containing the data
df_ginis_frd = dataframes["A2 Ginis and FRD"]


# Merge the Gini and fiscal redistribution data with the previously selected subset
df_merged = pd.merge(df_subset_years, df_ginis_frd, on=['Country', 'Year'])

# Visualize Gini coefficients over time for selected countries
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_merged, x='Year', y='Primary\nIncome', hue='Country', marker='o')
plt.title('Gini Coefficient Over Time for Selected Countries')
plt.xlabel('Year')
plt.ylabel('Gini Coefficient(Primary income)')
plt.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# Visualize overall fiscal redistribution measures over time for selected countries
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_merged, x='Year', y='Total15', hue='Country', marker='o')
plt.title('Fiscal Redistribution Measure Over Time for Selected Countries')
plt.xlabel('Year')
plt.ylabel('Fiscal Redistribution Measure')
plt.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()


# %%
df_ginis_frd = dataframes["A2 Ginis and FRD"]
df_ginis_frd.head()

# %%
# Merge the Gini and fiscal redistribution data with the previously selected subset
df_merged = pd.merge(df_subset_years, df_ginis_frd, on=['Country', 'Year'])

# Create a pivot table
pivot_table = pd.pivot_table(df_merged, values=['Primary\nIncome', 'Total15'],
                              index='Country', columns='Year', aggfunc='mean')

# Display the pivot table
print(pivot_table)

# %%
df_a2_pivot = dataframes["A2 Pivot"]
# Replace the following column names with the actual ones in your DataFrame
# Replace the following column names with the actual ones in your DataFrame
index_columns = ['Row Labels']  # Assuming 'Row Labels' is the country column 
columns_to_aggregate = [
    'Gini P income', 'Gini G income', 'Gini D income',
    'Fiscal redistr (%)', 'From tranfers', 'From income taxes',
    'Gini P income WA', 'Gini G income WA', 'Gini D income WA',
    'Fiscal redistr (%) WA', 'From transfers WA', 'From income taxes WA'
]

# Create a pivot table
pivot_table_a2 = pd.pivot_table(df_a2_pivot, values=columns_to_aggregate,
                                index=index_columns, aggfunc='sum')

# Display the pivot table
print(pivot_table_a2)

#make it a dataframe pandas format
df_a2_pivot = pd.DataFrame(pivot_table_a2.to_records())
df_a2_pivot.head()


# %%
# Split the 'Row Labels' column on the space character and keep only the first part (the country name)
df_a2_pivot['Row Labels'] = df_a2_pivot['Row Labels'].str.split(' ').str[0]

# Display the first few rows of the DataFrame to verify the changes
df_a2_pivot.head()

# %%
#filter to remain with the countries of interest
df_a2_pivot = df_a2_pivot[df_a2_pivot['Row Labels'].isin(selected_countries)]
df_a2_pivot.head()

# %%
# Split the 'Row Labels' column on the space character and keep only the first part (the country name)
df_a2_budget_target['LIS Dataset'] = df_a2_budget_target['LIS Dataset'].str.split(' ').str[0]

# Display the first few rows of the DataFrame to verify the changes
df_a2_budget_target.head()

# %%
# Replace it with the actual column name in your DataFrame
country_column = 'LIS Dataset'

# Columns for analysis
columns_to_analyze = ['Budget size (transfers)', 'Efficiency (transfers)']

# Group by country and calculate the mean for the selected columns
grouped_data = df_a2_budget_target.groupby(country_column)[columns_to_analyze].mean()

# Display the results
print(grouped_data)

# %%
# List of countries of interest
countries_of_interest = ['Canada', 'Australia', 'China', 'Austria', 'India', 'Brazil']

# Filter the grouped data to include only the countries of interest
filtered_data = grouped_data.loc[countries_of_interest]

# Display the results
print(filtered_data)

# %%
# List of colors
colors = ['b', 'g', 'r', 'c', 'm', 'y']

# Visualize the results
plt.figure(figsize=(12, 6))
sns.barplot(data=filtered_data, x=filtered_data.index, y='Budget size (transfers)', palette=colors)
plt.title('Budget Size for Selected Countries')
plt.xlabel('Country')
plt.ylabel('Budget Size (transfers)')
plt.show()

# %%
# Display the list of DataFrame names
print("DataFrame Names:", dataframe_names)

# %%
A4_bugdet_size_programs = dataframes["A4 Budget size programs"]
A4_bugdet_size_programs.head()

# %%
#split the 'LIS Dataset' column on the space character and keep only the first part (the country name)
A4_bugdet_size_programs['LIS Dataset'] = A4_bugdet_size_programs['LIS Dataset'].str.split(' ').str[0]
A4_bugdet_size_programs.head()

# %%
df_social_programs = dataframes["A4 Budget size programs"]
df_social_programs.head()

# %%
#Remove the Country column
df_social_programs = df_social_programs.drop(columns=['Country'])
#rename the LIS Dataset column to Country
df_social_programs = df_social_programs.rename(columns={'LIS Dataset': 'Country'})
df_social_programs.head()

# %%
#print unique values in the 'Country' column
unique_countries = df_social_programs['Country'].unique()
print(unique_countries)

# %%
# Assuming you have already defined a subset of countries and years
subset_countries = ['Canada', 'Australia', 'China', 'Austria', 'India', 'Brazil']
subset_years = [2000, 2005, 2010, 2014]
df_subset = df_social_programs[df_social_programs['Country'].isin(subset_countries)]
df_subset.head()

# %%
# Perform relevant statistical analyses based on your research questions

# %%
df_subset.head()

# %%
# Select relevant columns for the analysis
social_program_columns = ['Old-age/ \nDisability/ \nSurvivor', 'Sickness', 'Family/\n Children', 
                           'Education', 'Unemployment', 'Housing', 
                           'General/food/ medical\nassistance', 'Other transfers', 'Residual',
                           'Income taxes']
# Time Series Analysis: Use seaborn to visualize the impact of each social program over 
plt.figure(figsize=(12, 6))
for program in social_program_columns:
    sns.lineplot(data=df_subset, x='Year', y=program, hue='Country', marker='o')
plt.title('Impact of Social Programs on Poverty and Inequality Over Time')
plt.xlabel('Year')
plt.ylabel('Program Impact')
plt.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# %%
# Set up the panel data structure using the 'xtset' command
# Assuming 'Country' and 'Year' are the columns representing country and year
#df_subset = df_subset.set_index(['Country', 'Year'])


# Use xtset-like functionality to define the panel structure
# This helps in informing the library about the panel structure for time series analysis
df_subset = df_subset.sort_index(level=['Country', 'Year'])

# Select relevant columns for the analysis
social_program_columns = ['Old-age/ \nDisability/ \nSurvivor', 'Sickness', 'Family/\n Children', 
                           'Education', 'Unemployment', 'Housing', 
                           'General/food/ medical\nassistance', 'Other transfers', 'Residual',
                           'Income taxes']

# Time Series Analysis: Use seaborn to visualize the impact of each social program over time
plt.figure(figsize=(12, 8))
for program in social_program_columns:
    sns.lineplot(data=df_subset, x='Year', y=program, hue='Country', marker='o')

plt.title('Impact of Social Programs on Poverty and Inequality Over Time')
plt.xlabel('Year')
plt.ylabel('Program Impact')
plt.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()


