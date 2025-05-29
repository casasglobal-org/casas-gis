## PERL script overview

### `cliparse_TC.pl`

`cliparse_TC.pl`: This Perl script transforms a string containing attribute values from a database file into a formula suitable for use in GRASS GIS (Geographic Resources Analysis Support System) clipping operations.

Input:

1. **Command-line Arguments:**

   - `$HomeDir`: The CASAS home directory where the script should operate.
   - `$fieldName`: The name of the attribute column in the database file.
   - `$fieldType`: The type of the attribute column (either 'number' or 'string').
   - `$input`: The path to the input file containing the attribute values.
   - `$output`: The path to the output file where the formula will be written.

2. **Input File:**
   - The input file contains a list of attribute values, which can be either space-separated or comma-separated.

Output:

- The output file contains a single line with a formula that can be used in GRASS GIS for clipping operations. The formula is a series of conditions joined by the `or` operator, e.g., `(fieldName=value1)or(fieldName=value2)`.

Example:

If the input file contains the values `USA, Canada, Mexico` and the field type is 'string', the output file will contain:

```
(fieldName='USA')or(fieldName='Canada')or(fieldName='Mexico')
```

### `convertITA.pl`

`convertITA.pl`: This Perl script processes output tables from CASAS systems models for import into GRASS GIS, where they can be used for interpolation and visualization.

Input:

1. `$HomeDir`: The script expects the path to the CASAS home directory as its first command-line argument.
2. **Configuration File**: Within this directory, it looks for a file named `inputPar.txt`, which contains three integers indicating the columns for longitude, latitude, and a parameter in the model output files.
3. **Model Output Files**: The script processes `.txt` The only `*.txt` files resulting from the PBDM simulation located in the `outfiles` subdirectory of the CASAS home directory.

Output:

- The script creates a temporary directory called `models_temp` within the CASAS home directory.
- It processes each `.txt` file in the `outfiles` directory, extracts specific columns (longitude, latitude, and parameter), and writes the extracted data to new files in the `models_temp` directory. These new files are named based on the parameter and the original file name.

Key Operations:

- **Column Extraction**: The script uses the column indices from `inputPar.txt` to extract the relevant data from each line of the model output files.
- **File Naming**: The output files are named by combining the parameter name and the original file name (without the `.txt` extension).
- **Data Formatting**: The script ensures that the data is formatted correctly for import into GRASS GIS, including handling newline characters and whitespace.

### `HtmlPlotC.pl`

`HtmlPlotC.pl`: This Perl script generates an HTML page that displays histogram images produced by d.histogram from GRASS GIS and saves the HTML page in a specified directory.

Input:

1. **Directory Path (`$SaveDir`)**: The first argument is the directory where the histogram images are stored.
2. **Legend String (`$LegendString`)**: The second argument is a string used to name the HTML file and as a title within the HTML content.

Output:

- `$SaveDir`: An HTML file named `"$LegendString-PLOTc.html"` is created in the specified directory (`$SaveDir`). This HTML file contains:
  - A title derived from the `$LegendString`.
  - A series of histogram images (`.png` files) that match the pattern `.-HIST.png`.
  - Each histogram image is displayed with a corresponding caption indicating the input file name.

### `htmlSum.pl`

`htmlSum.pl`: This Perl script generates an HTML visual summary for CASAS models.

Input:

1. `$SaveDir`: The directory where the maps are saved.
2. `$LegendString`: A string used for naming the HTML file and other related files.
3. `$MapPar`: The parameter being mapped.
4. `$LowerCut`: The lower cutting point for the map.
5. `$UpperCut`: The upper cutting point for the map.
6. `$AltClip`: The altitude clip value.
7. `$SurfCut`: yes/no indicating if stations above altitude clip were used to interpolate.
8. `$EtoClip`: The region clip value.
9. `$Plots`: A flag indicating whether to include links to barchart plots.

Output:

The script generates an HTML file named `$LegendString.html` in the specified directory (`$SaveDir`). The HTML file contains:

1. A title and meta information.
2. A report section with links to output maps (PNG images) and their corresponding stat reports (TXT files).
3. Optional links to barchart plots and histograms if the `$Plots` flag is set.
4. A section listing the mapping parameters.
5. A log of input files read from `$LegendString.log`.

### `multiColorRule.pl`

`multiColorRule.pl`: This Perl script generates a color rule file based on the range of data found in model output files. It can use any combination of any number of colors.

Input:

1. **Command-line Arguments:**

   - `$HomeDir`: The directory where the script will look for temporary model output files in `$HomeDir/models_temp/` and where it will write the output files.
   - `$rule`: A string of colors separated by dashes (e.g., "red-blue-green") that will be used to create the color rules.
   - `$lowCut`: The lower cutoff value for the data range.
   - `$hiCut`: The upper cutoff value for the data range.
   - `$divergentRule`: A flag ("divYes" or "divNo") indicating whether the color rule should be divergent.

2. **Model Output Files:**
   - The script reads temporary files from the `models_temp` directory within the specified CASAS home directory. These files contain data that will be used to determine the range for the color rules.

Output:

1. **`customColorRule.txt`:**

   - A file containing the color rules, where each line consists of a coefficient and a corresponding color.
   - The file ends with the word "end" as required by GRASS GIS.

2. **`min.txt`:**

   - A file containing the minimum value of the data range.

3. **`max.txt`:**

   - A file containing the maximum value of the data range.

### `printCols.pl`

`printCols.pl`: This Perl script processes model output files located in a specified directory. It reads the files, extracts column and row names, and prints them to the standard output.

Input:

- `$HomeDir`: The script takes a single command-line argument, which is the CASAS home directory path (`$HomeDir`). This directory is expected to contain a subdirectory named `outfiles` containing resulting files from the PBDM simulation.

Output:

- The script prints the column names and the number of rows from the first `.txt` file (resulting from the PBDM simulation) it encounters in the `outfiles` directory.

Note:

- The script does not handle the extraction and printing of years. This functionality has been moved to a separate script called `printYear.pl`.

Example Output:
If the first `.txt` file in the `outfiles` directory has the following content:

```
Column1    Column2    Column3
Row1Data1  Row1Data2  Row1Data3
Row2Data1  Row2Data2  Row2Data3
```

The script will output:

```
The following column names were found:

1. Column1
2. Column2
3. Column3

Number of rows is 3.
```

### `printYear.pl`

`printYear.pl`: This Perl script processes text files resulting from the PBDM simulation in `$HomeDir/outfiles/` to extract analysis years from them, and writes the extracted data to new output files for use in d.legend of GRASS GIS.

Input:

1. :`$HomeDir` The script expects a single command-line argument, which is the path to the CASAS home directory.
2. **Directory Structure**: Within the CASAS home directory, it looks for a subdirectory named `outfiles` containing `.txt` files (resulting from the PBDM simulation).
3. **Configuration File**: It also expects a file named `inputPar.txt` in the CASAS home directory, which contains configuration data.

Output:

- **Output Files**: For each `.txt` file processed, the script creates a corresponding `yearX.txt` file in the CASAS home directory, containing the extracted year.

Example:

If the `outfiles` directory contains `file1.txt` and `file2.txt`, and `inputPar.txt` specifies that the year is in the 4th column, the script will create `year1.txt` and `year2.txt` in the CASAS home directory, each containing the year extracted from the respective file.

### `voroparse.pl`

`voroparse.pl`: This Perl script transforms a list of categories from a file into a formula suitable for use with the `v.extract` command in GRASS GIS.

Input:

1. `$HomeDir`: The script expects a single command-line argument, which is the CASAS home directory).
2. `voronoi.txt`: Within the specified CASAS home directory, the script reads a file named `voronoi.txt`. This file is expected to contain a list of categories, each on a new line.

Output:

- `voronoiFormula.txt`: The script writes the resulting formula to a file named `voronoiFormula.txt` in the specified CASAS home directory. This formula can be used in GRASS GIS to extract vector features based on the categories listed in `voronoi.txt`.

Example:

If `voronoi.txt` contains:

```
1
2
3
```

The output file `voronoiFormula.txt` will contain:

```
(cat=1) or (cat=2) or (cat=3)
```

This formula can then be used in GRASS GIS (`v.extract` command) to select and extract Voronoi polygons that match any of the specified categories.
