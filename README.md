## Problem


A newspaper editor was researching immigration data trends on H1B(H-1B, H-1B1, E-3) visa application processing over the past years, trying to identify the occupations and states with the most number of approved H1B visas. She has found statistics available from the US Department of Labor and its [Office of Foreign Labor Certification Performance Data](https://www.foreignlaborcert.doleta.gov/performancedata.cfm#dis). But while there are ready-made reports for [2018](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2018/H-1B_Selected_Statistics_FY2018_Q4.pdf) and [2017](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2017/H-1B_Selected_Statistics_FY2017.pdf), the site doesn’t have them for past years.

This code creates a mechanism to analyze past years data, specificially calculate two metrics: **Top 10 Occupations** and **Top 10 States** for certified visa applications. But can also be easily modified to return `topN` results. 


## Approach

After To only have to run through the data once, we compute the indicies of the columns of `status_index`, `occ_index`and `state_index`. Then we can only if `status == CERTIFIED` we increment two dictionaries based on the count of occupations and states. We then sort the dictionaries based on the number of occurances of occupations and states and then alphabetically based on name. We only keep the `topN` (10) occupations and states. We then compute the percentage of applications that have been certified compared to total number of certified applications and save the results to a text file. Each line holds one record and each field on each line is separated by a semicolon (;).



## How to Run 

Two different ways to run the code. 
- You may include your CSV file in the `input` directory with the name `h1b_input.csv` and from the top-level root of the repository run the bash command
```
sh run.sh
```
- Or you can simply run the python file directly from this top-level directory. 
```
./src/h1b_counting.py input_filepath occupation_output_filepath state_output_filename
```
Where the first argument is the path your raw CSV file, and the second and third are the paths where you want to save the output text files. 

An example of this might include 
```
./src/h1b_counting.py ./input/H1B_FY_2016.csv ./output/top_10_occupations.txt ./output/top_10_states.txt
```


## Sample Output
```
TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE
SOFTWARE DEVELOPERS, APPLICATIONS;6;60.0%
ACCOUNTANTS AND AUDITORS;1;10.0%
```
```
TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE
FL;2;20.0%
AL;1;10.0%
CA;1;10.0%
```




## Dependancies 

python3.6


## Tests

You can run the test with the following command from within the `insight_testsuite` folder:
```
insight_testsuite~$ sh run_tests.sh
```