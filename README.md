# CourseScraper

This program will pull up a window to UW-Madison's Course Search and Enroll, where you will log in and select the options you want (in the left bar). Then, it will sort all the courses selected by those options by average GPA.

**Run the python script "scraper.py". A internet connection is required.**

#### Optional arguments:
+  -h, --help
    + Displays help on how to use program
+  -w [WRITE], --write [WRITE]
    + Write course codes to a file without sorting. Filename specification is optional.
+  -r [READ], --read [READ]
    + Read course codes from file and sort by GPA. Filename specification is optional.
+  -o [OUTPUT], --output [OUTPUT]
    + Output the final results to a file. Filename specification is optional.
+  -p [PRINT] [PRINT], --print [PRINT] [PRINT]
    + Print output again. Filename specification is optional. Can also specify max course code.

#### Examples:

+ python scraper.py -w
    + *will display all courses sorted by average GPA and write the courses to the default write file*
+ python scraper.py -w -o 
    + *will display all courses sorted by average GPA, write the courses to the default write file, and write all the sorted courses to the default output file*
+ python scraper.py -r test_file.csv 
    + *will display all courses read from test_file.csv sorted by average GPA*
+ python scraper.py -p 400 
    + *will display all courses under the 400 level sorted by average GPA*
+ python scraper.py -p out_file.csv 400 
    + *will display all courses under the 400 level sorted by average GPA loaded from out_file.csv*
