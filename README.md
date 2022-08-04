Overview:

This tool takes a .csv log file as input, performs Incremental Development analysis on it, and outputs a .csv of the results.

The columns that it produces are:
1. User ID
2. Lab ID
3. IncDev Score
4. IncDev Trail
5. LOC Trail
6. Time Between Subs Trail
7. Coding Trail
8. Drastic Change Trail

How to run:

1. Download the tool and unzip it to a location of your choice
2. In a terminal, navigate to the directory where you unzipped the folder
3. Run the command pip install -r requirements.txt
    This command installs the python packages Pandas, datetime, and requests.
4. Run the script with the command python3 main.py
    You will be prompted to enter the name of the log file you want to use as input.
    Type the filename (ex. zybookcode_term_logfile.csv) and press enter.
5. Wait until the script finishes running
    When the script completes an output file will be generated
    The output file will have the same name as the input file, but with 'output_' prepended to it.

Notes:

1. The input log file must be placed in the 'input' folder. The output will be produced in the 'output' folder.
2. Python3/pip should be installed in order to run the commands given above. Tutorials for installing these can be found online.
3. Currently, only one lab can be analyzed at a time. Using an input file that includes multiple labs will not produce accurate results.
4. Excel and Google Sheets sometimes erroneously apply formatting to the data, making it look incorrect. To avoid this, see below.
    Excel: Open a blank workbook. Navigate to the 'Data' tab and click 'From Text/CSV'. 
        Select the output file you want to view and click 'Import'. Next, press 'Load'.
    Google Sheets: Open a blank sheet. Select 'File' > 'Import' > 'Upload'.
        Click 'Select a file from your device' or drag the file onto the page. 
        Uncheck the 'Convert text to numbers, dates, and formulas' box and press 'Import data'. 