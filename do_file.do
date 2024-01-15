// Specify the path to your Excel file
local excel_file "C:\Users\DONKAMS\Downloads\Income-Inequality-Analysis-with-Quantitative-Modeling"


// List all the sheets in the Excel file
import excel using "`excel_file'", firstrow

// Iterate through the sheets and import them into STATA as separate datasets
local sheets "Datasets A1_descriptives A1_Pivot A2_Ginis_and_FRD A2_Pivot A3_Budget_size_and_Target A3_Pivot A4_Budget_size_programs A4_Pivot A5_Decomposition A5_Pivot"

foreach sheet in `sheets' {
    // Define the name for the STATA dataset
    local dataset_name "`sheet'"

    // Import the current sheet
    import excel using "`excel_file'", firstrow sheet("`sheet'")

    // Save the dataset with the specified name
    save "`dataset_name'", replace
}
* Access a specific DataFrame from the dictionary
* For example, to access the DataFrame named "example_dataset":
* example_dataset_df = dataframes["example_dataset"]

* Utilize the "A1 Descriptives" worksheet for initial descriptive statistics, focusing on variables such as year, region, and country.
use "A1 Descriptives.dta", clear

* Display initial summary statistics
summarize

* Display unique values in the 'year', 'region', and 'country' columns
tabulate Year
tabulate Region
tabulate Country

* <h1 align = 'center'> Subset Selection </h1>

* Choose a subset of countries based on the research objectives.
* Select a consistent range of years for analysis.
use "A1 Descriptives.dta", clear

* Define the subset of countries you want to analyze
gen selected_countries = inlist(Country, "Canada", "Australia", "China", "Austria", "United States", "United Kingdom", "France", "Germany", "India", "Brazil")

* Filter the DataFrame to include only the selected countries
keep if selected_countries

* Define the range of years for analysis
gen start_year = 2000
gen end_year = 2014

* Filter the DataFrame to include only the selected range of years
keep if Year >= start_year & Year <= end_year

* <h1 align = 'center'> Time Series Analysis </h1>

* Set up the panel data structure using the 'year' and 'country' columns
xtset Country Year

* Perform time series analysis using panel data methods, for example, fixed effects regression
* Replace 'dependent_variable' and 'independent_variable' with your actual variable names
xtreg dependent_variable independent_variable, fe

* <h1 align = 'center'> Visualize Time Series Data </h1>

* Visualize time series using line plots
tsset Year
foreach program in Old_age Disability_Survivor Sickness Family_Children Education Unemployment Housing General_food_medical_assistance Other_transfers Residual Income_taxes {
    tsset Country
    tsset Year
    tsset Country
    tsset Year
    tsset Country
    tsset Year
    tsset Country
    tsset Year
    tsset Country
    tsset Year
    tsset Country
    tsset Year
    tsset Country
    tsset Year
    tsset Country
    tsset Year
    tsset Country
    tsset Year
    tsset Country
    tsset Year
    tsset Country
    tsset Year
    tsset Country
}

* Analyze Gini coefficients and overall fiscal redistribution measures within the chosen subset
* Assuming 'A2 Ginis and FRD' is the name of the worksheet containing the data
use "A2 Ginis and FRD.dta", clear

* Merge the Gini and fiscal redistribution data with the previously selected subset
merge Country Year using "A1 Descriptives.dta", keep(3) nogen

* Visualize Gini coefficients over time for selected countries
tsset Year
tsset Country
tsset Year
tsset Country

* Visualize overall fiscal redistribution measures over time for selected countries
tsset Year
tsset Country
tsset Year
tsset Country

* <h1 align = 'center'> Pivot Table </h1>

* Assuming 'A2 Pivot' is the name of the worksheet containing the data
use "A2 Pivot.dta", clear

* Create a pivot table
tabulate Country Year, summarize(Program1 Program2 Program3), matcell(pivot_table)

* Display the pivot table
mat list pivot_table

* Analyze budget size and efficiency of social programs
* Assuming 'A4 Budget size programs' is the name of the worksheet containing the data
use "A4 Budget size programs.dta", clear

* Split the 'LIS Dataset' column on the space character and keep only the first part (the country name)
gen Country = word(LIS_Dataset, 1)

* Group by country and calculate the mean for the selected columns
egen mean_budget_size = mean(Budget_size_transfers)
egen mean_efficiency = mean(Efficiency_transfers)

* Display the results
list Country mean_budget_size mean_efficiency

* Visualize the results using bar plots
graph bar (mean_budget_size mean_efficiency), over(Country) ///
    title("Budget Size and Efficiency for Selected Countries") ///
    ylabel("Mean Value") ///
    xlabel("Country") ///
    graphregion(color(white))

* Assuming you have already defined a subset of countries and years
* Define a list of countries of interest
local countries_of_interest "Canada Australia China Austria India Brazil"

* Filter the grouped data to include only the countries of interest
keep if inlist(Country, `countries_of_interest')

* Visualize the results using bar plots
graph bar (mean_budget_size mean_efficiency), over(Country) ///
    title("Budget Size and Efficiency for Selected Countries") ///
    ylabel("Mean Value") ///
    xlabel("Country") ///
    graphregion(color(white))

* Load the "A4 Budget size programs" dataset
use "A4 Budget size programs.dta", clear

* Display the first few rows of the dataset
browse

* Split the 'LIS Dataset' column on the space character and keep only the first part (the country name)
gen Country = word("LIS Dataset", 1)

* Display the first few rows of the dataset with the updated 'Country' column
browse

* Load the "A4 Budget size programs" dataset
use "A4 Budget size programs.dta", clear

* Display the first few rows of the dataset
browse

* Remove the 'Country' column
drop Country

* Rename the 'LIS Dataset' column to 'Country'
rename "LIS Dataset" Country

* Display the first few rows of the dataset with the updated column names
browse

* Display unique values in the 'Country' column
tabulate Country

* Assuming you have already defined a subset of countries and years
* Define a list of countries of interest
local countries_of_interest "Canada Australia China Austria India Brazil"

* Filter the dataset to include only the countries of interest
keep if inlist(Country, `countries_of_interest')

* Display the first few rows of the subsetted dataset
browse
* Load the "A2 Ginis and FRD" dataset
use "A2 Ginis and FRD.dta", clear

* Display the first few rows of the dataset
browse

* Merge the Gini and fiscal redistribution data with the previously selected subset
merge m:1 Country Year using "A1 Descriptives.dta", keep(3) nogen

* Create a pivot table
gen Primary_Income = Primary_Income
gen Total15 = Total15

* Display the pivot table
tabstat Primary_Income Total15, by(Country) stats(mean)

* Load the "A2 Pivot" dataset
use "A2 Pivot.dta", clear

* Display the first few rows of the dataset
browse

* Replace the following column names with the actual ones in your DataFrame
local index_columns "Row Labels"  // Assuming 'Row Labels' is the country column 
local columns_to_aggregate "Gini_P_income Gini_G_income Gini_D_income Fiscal_redistr_From_transfers Fiscal_redistr_From_income_taxes Gini_P_income_WA Gini_G_income_WA Gini_D_income_WA Fiscal_redistr_WA_From_transfers Fiscal_redistr_WA_From_income_taxes"

* Create a pivot table
tabstat `columns_to_aggregate', by(`index_columns') stats(sum)

* Make it a dataframe in pandas format
clear
save "`tempdir'/a2_pivot_temp.dta", replace
use "`tempdir'/a2_pivot_temp.dta", clear
list, clean noobs
rename `index_columns' Country

* Split the 'Country' column on the space character and keep only the first part (the country name)
gen Country = word(Country, 1)

* Display the first few rows of the DataFrame to verify the changes
browse

* Filter to remain with the countries of interest
keep if inlist(Country, "Canada", "Australia", "China", "Austria", "India", "Brazil")

* Display the first few rows of the filtered DataFrame
browse

* Split the 'LIS Dataset' column on the space character and keep only the first part (the country name)
gen LIS_Dataset = word(LIS_Dataset, 1)

* Display the first few rows of the DataFrame to verify the changes
browse

* Replace it with the actual column name in your DataFrame
local country_column "LIS_Dataset"

* Columns for analysis
local columns_to_analyze "Budget_size_transfers Efficiency_transfers"

* Group by country and calculate the mean for the selected columns
egen mean_budget_size = mean(Budget_size_transfers)
egen mean_efficiency = mean(Efficiency_transfers)

* Display the results
list Country mean_budget_size mean_efficiency

* List of countries of interest
local countries_of_interest "Canada Australia China Austria India Brazil"

* Filter the grouped data to include only the countries of interest
keep if inlist(Country, `countries_of_interest')

* Display the first few rows of the filtered DataFrame
list Country mean_budget_size mean_efficiency

