// Specify the path to your Excel file
local excel_file "C:\Users\DONKAMS\Downloads\Income-Inequality-Analysis-with-Quantitative-Modeling\resources-other-llbifr-data.xlsx"


// List all the sheets in the Excel file
import excel using "excel_file", firstrow


// List of sheets
local sheets "Datasets A1_descriptives A1_Pivot A2_Ginis_and_FRD A2_Pivot A3_Budget_size_and_Target A3_Pivot A4_Budget_size_programs A4_Pivot A5_Decomposition A5_Pivot"

// Iterate through the sheets and import them into STATA as separate datasets
foreach sheet in `sheets' {
    // Define the name for the STATA dataset
    local dataset_name "`sheet'"

    // Import the current sheet
    import excel using "`excel_file'", firstrow sheet("`sheet'")

    // Save the dataset as a Stata file with the specified name
    save "`dataset_name'.dta", replace
}

//Import the "Datasets" worksheet containing gross and net income data into STATA

// Specify the path where the CSV files are located
local csv_folder "C:\Users\DONKAMS\Downloads\Income-Inequality-Analysis-with-Quantitative-Modeling\data"

// List all CSV files in the specified folder
local csv_files : dir "`csv_folder'" files "*.csv"

// Iterate through the CSV files and import them into Stata as separate datasets
foreach file in `csv_files' {
    // Extract the filename without extension to use as the dataset name
    local dataset_name : subinstr local file ".csv" "", all

    // Import the current CSV file
    import delimited "`csv_folder'\`file'", clear

    // Save the dataset as a Stata file with the specified name
    save "`dataset_name'.dta", replace
}
// Specify the path to your CSV file
local csv_file "C:\Users\DONKAMS\Downloads\Income-Inequality-Analysis-with-Quantitative-Modeling\data\Datasets.csv"

// Import the "Datasets" worksheet into Stata
import delimited "`csv_file'", clear

// Save the dataset as a Stata file
save "Datasets.dta", replace

// Specify the path to your CSV file
local csv_file "C:\Users\DONKAMS\Downloads\Income-Inequality-Analysis-with-Quantitative-Modeling\data\A1 Descriptives.csv"

// Import the "A1 Descriptives" worksheet into Stata
import delimited "`csv_file'", clear

// Display initial descriptive statistics
summarize year region country

// If you want to save the descriptive statistics as a separate dataset
save "A1_Descriptives_Stats.dta", replace


