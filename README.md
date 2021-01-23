# VAERS-insight

The code here can be used to examine the CSV data files available from the VAERS database website. (https://vaers.hhs.gov/)
This is useful for those interested in examining how many adverse reactions were reported from vaccines, and the deaths.

To use this code, ensure you have the VAERS data files called 2021VAERSDATA.csv and 2021VAERSVAX.csv in the same folder as the appv.py code file.

Note that initially there will be errors relating to "got x columns instead of" when you run the code.
It will require the 2021VAERSDATA.csv file to be manually fixed. The easiest way is to use Excel, and search-and-replace for the character # and replace it with (say) a space. You may have to make some other small manual edits like this, because the Python code currently uses a function called genfromtxt which has limitations.

