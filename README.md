# Table of Contents

  * [Problem](README.md#problem)
  * [Approach](README.md#approach)	 
  * [Run](README.md#run)

# Problem

* **General goal:**  
Research immigration data trends on H1B visa application processing over past years.

* **Specific goal:**  
Calculate two metrics for **certified** visa applications:  
  1. **top 10 occupations**;  
  2. **top 10 states**.

# Approach

## 1. Generate the input dataset
The raw data can be found [here](https://www.foreignlaborcert.doleta.gov/performancedata.cfm) under the **Disclosure Data** tab. Then, convert the **Excel files** into **CSV files** with a **semicolon-separated (";")** format. (Note: other formats require changes to the *python script* under the *src* folder.) The **CSV files** are the input dataset, which should be under the *input* folder.

## 2. Extract relevant data from the input dataset ##
Only 3 fields are relevant for this specific task: the **status** of the visa application, the **occupational name** and the **state** where the work take place.  


*a). Locate the relevant information in the input dataset.*


According to the **File Structures** for the past few years (see the [webpage](https://www.foreignlaborcert.doleta.gov/performancedata.cfm) of the raw data), we found the following features of their field names:


`status`: The application status is the only field name contains the word "status", e.g. "CASE_STATUS" or "APPROVAL_STATUS".


`occupational name`: It contains the word "SOC" (abbreviation for Standard Occupational Classification). There are always two field names contain "SOC". It is not the one contains the word "CODE". It usually contains either "SOC_NAME" or "SOC_TITLE". *The fiscal year 2008 and 2009 efile are special cases where "Occupational_Title" is used instead.*


`state`: The field name contains both the words "WORK" and "STATE". *The fiscal year 2008 & 2009 efile are special cases where "State_1" is used instead.*


*b). Search for the 'CERTIFIED' cases and store their occupation names and working states for the statistical analysis.*

## 3. Analyze the data

*a). Count the number of certified applications for each occupation and state.*


*b). Sort the results and save the data for the top 10 occupations and the top 10 states.*

Sort by the number of certified applications. If there is a tie, then sort by alphabetically by the name of the occupation or of the state.


*c). Based on the count, calculate the percentage of certified applications for each occupation and state compared to the total number of certified applications.*


## 4. Output the results
Create two output files to store the results from the previous step:


* `top_10_occupations.txt`: Top 10 occupations for certified visa applications.
* `top_10_states.txt`: Top 10 states for certified visa applications.


**File Structure** for `top_10_occupations.txt`:


1. `TOP_OCCUPATIONS`: The occupation name associated with an application's Standard Occupational Classification (SOC) code.
2. `NUMBER_CERTIFIED_APPLICATIONS`: The number of applications that have been certified for that occupation. An application is considered certified if it has a case status of `CERTIFIED`.
3. `PERCENTAGE`: % of applications that have been certified for that occupation compared to the total number of certified applications regardless of occupation.



**File Structure** for `top_10_states.txt`:


1. `TOP_STATES`: State where the work takes place.
2. `NUMBER_CERTIFIED_APPLICATIONS`: The number of applications that have been certified for work in that state. An application is considered certified if it has a case status of `CERTIFIED`.
3. `PERCENTAGE`: % of applications that have been certified in that state compared to the total number of certified applications regardless of state.



Depending on the input, there may be fewer than 10 lines in each file. There, however, will not be more than 10 lines in each file. In case of ties, only list the top 10 based on the sorting instructions given above.  
Percentages are rounded off to 1 decimal place. For instance, 1.05% is rounded to 1.1% and 1.04% is rounded to 1.0%. Also, 1% is represented by 1.0%.

# Run

1\. Make sure the H1B visa application dataset (CSV file with a semicolon-separated (";") format) is placed in the *input* folder.


2\. Open the `run.sh` script. Put the relative path of the dataset you want to analyze as the first argument of the python script: `./src/h1b_counting.py`. Then, put the relative path of the two output files as the second and third argument. The order of these two arguments does not matter. However, the input dataset must be placed in the `input` folder, the output file for the top 10 occupations must contain the word "occupation", and the output file for the top 10 states must contain the word "state".  
Example:
```shell
python ./src/h1b_counting.py ./input/name_of_the_dataset.csv ./output/top_10_occupations.txt ./output/top_10_states.txt
```


3\. Open the `Terminal` and go to the directory where the `run.sh` file is located. Once the output files are successfully generated, you will see `Finish output file: ./output/name_of_the_output_file.txt` on your terminal.  
Example for MacOS:
```bash
$ cd /path/to/the/script
$ sh run.sh
Finish output file: ./output/top_10_states.txt
Finish output file: ./output/top_10_occupations.txt
```  

Example for Linux:
```bash
$ cd /path/to/the/script
$ ./run.sh
Finish output file: ./output/top_10_states.txt
Finish output file: ./output/top_10_occupations.txt
```
