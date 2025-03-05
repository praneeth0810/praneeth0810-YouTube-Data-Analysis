# YouTube Data Analysis for Ad Campaigns

## Project Overview

I created this project to help clients or companies run ad campaigns using YouTube as a source. The key questions I aim to answer are:

- **How can I categorize videos based on comments and statistics?**
- **What factors influence the popularity of a YouTube video?**

## Goals and Success Criteria

- **Data Ingestion**: Efficiently ingest data, both one-off and incrementally.
- **ETL Design**: Extract, transform, and load (ETL) data efficiently.
- **Data Lake**: Design and build a scalable data lake architecture.
- **Scalability**: Ensure the data architecture scales efficiently.
- **AWS Cloud**: Implement cloud-based data storage and processing.
- **Reporting**: Develop a business intelligence dashboard for insights.

## Technology Used

For this project, I used the following technologies:

- **Python**: For data processing and scripting.
- **PySpark**: To process large datasets efficiently.
- **AWS Glue**: For ETL automation and metadata management.
- **ETL Pipelines**: To extract, transform, and load data seamlessly.
- **Cloud Storage (S3)**: To store raw, cleansed, and processed data.
- **SQL**: For querying and transforming data in the analytics layer.


## Project Architecture
![alt text](architecture.png)

### Data Organization

I created two folders:

1. **JSON Data** - Contains category IDs for different regions.
2. **CSV Data** - Contains daily trending YouTube videos.

I use AWS Glue to crawl and extract metadata from JSON files. IAM roles required for this process:

- **AmazonS3FullAccess**: Grants full access to S3.
- **AWSGlueServiceRole**: Allows AWS Glue to interact with S3, CloudWatch, and other AWS services.

## Data Cleaning Process

![Data Cleaning](attachment:31f19db7-ff35-4c2d-bb60-29091f2987f7:image.png)

- **Convert JSON files to column and row format (Apache Parquet)**.
- **Normalize nested JSON fields** to extract relevant data.
- **Handle missing and inconsistent values**.

### AWS Lambda Workflow

1. Triggered by an **S3 event** when a new JSON file is uploaded.
2. Extracts **file details** (bucket & key).
3. Reads the JSON file into a **Pandas DataFrame**.
4. **Normalizes nested JSON data**.
5. Writes transformed data to **S3 in Parquet format**.
6. Registers metadata in **AWS Glue Catalog**.
7. **Handles errors gracefully**.

### AWS Lambda Permissions Needed

- **AmazonS3FullAccess**: Grants full access to Amazon S3.
- **AWSGlueServiceRole**: Provides AWS Glue with necessary permissions.

## Preprocessing Steps

| Step | Description |
| --- | --- |
| **1. Data Filtering** | Loads only **Canada, US, GB** data using predicate pushdown. |
| **2. Data Type Mapping** | Ensures correct data types for all columns. |
| **3. Resolving Type Conflicts** | Handles inconsistencies in column data types. |
| **4. Removing Null Fields** | Drops records where all values are NULL. |
| **5. Optimizing Output** | Coalesces data, partitions by `region`, and saves as **Parquet** in **S3**. |

## ETL Design

- I created two tables: **Statistics** and **Statistics Reference Data**.
- I designed an **ETL pipeline** using AWS Glue to join both tables via an **inner join**.
- The final processed data is stored in a **new S3 bucket** and an **analytics database**.

### Cleansed vs. Analytics Layer

| Layer | Purpose |
| --- | --- |
| **Cleansed Layer** | Stores cleaned data; requires joins for analysis. |
| **Analytics Layer** | Pre-aggregated tables optimized for queries. |

## Dashboard Visualizations

I use the final processed dataset to create dashboards and visualizations, providing actionable insights for decision-making.

[text](Analytics_visualizations.pdf)

