How to run the program:
Example : python3 ./src/purchase_analytics.py ./input/products.csv ./input/order_products.csv ./output/report.csv
The input file and the output filenames for running purchase_analytics.py have to be passed as parameters.
The script will calculate the ratio of first time order of product with total number of requests of product per department

Steps Involved:
Ingest products.csv to a dictionary prod_dept 
Ingest order_products.csv. Look up department from prod_dept dictionary for each product in order_products.csv.
Create a dictionary dept with department_id as key and  first time request, total number of requests of product as values
Calculate percentage of first time requests by total number of requests of products per department
Write into report.csv file

Assumptions:
Skip line if department_id is not found for a particular product. 
   