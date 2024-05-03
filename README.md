# Upstox-api-RIL-data-ETL-AWS


This project implements an ETL pipeline to extract, transform, and load data.

**Pipeline Stages**

The pipeline follows these three stages:

1. **Extract:** Data is retrieved from a source system. (e.g., Amazon EventBridge in this example)
2. **Transform:** The data is converted into a format suitable for the target system. This may involve cleaning, formatting, or deriving new data points.
3. **Load:** The transformed data is loaded into a designated target system (data warehouse, data lake, analytics platform).

**How to Use This Project**

This project implements an ETL pipeline to extract, transform, and load Reliance stock data for further analysis using Amazon Athena.

**Pipeline Stages**

The pipeline executes the following stages in a sequence:

1. **Data Extraction (Daily):**
   - An EventBridge trigger fires daily.
   - The triggered Lambda function extracts Reliance stock data from the Upstox API.
   - The extracted data is stored in JSON format within an S3 bucket.

2. **Data Transformation:**
   - An S3 event trigger is invoked upon data insertion into the S3 bucket.
   - The triggered Lambda function transforms the JSON data into CSV format.
   - The transformed CSV data is stored in a separate location within the S3 bucket.

3. **Data Loading and Analysis:**
   - An AWS Glue crawler crawls the S3 bucket where the CSV data resides.
   - The crawled data is stored in a designated data catalog database.
   - Amazon Athena can then be used to analyze the loaded stock data.


1. Clone the repository:
   - All the lambda scripts are added for your reference.

```bash
git clone https://github.com/dsharshgupta/Upstox-api-RIL-data-ETL-AWS.git
