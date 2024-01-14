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

