import awswrangler as wr  # A library for handling AWS services
import pandas as pd
import urllib.parse  # Helps with URL decoding for S3 object keys
import os # to access environmental variables

#Read Environment Variables
os_input_s3_cleansed_layer = os.environ['s3_cleansed_layer']  # Target S3 location for processed data
os_input_glue_catalog_db_name = os.environ['glue_catalog_db_name'] #AWS glue database name
os_input_glue_catalog_table_name = os.environ['glue_catalog_table_name'] #AWS Glue table name for storing metadata
os_input_write_data_operation = os.environ['write_data_operation'] # here we will be using "append" operation for writing data

def lambda_handler(event,contex):   #event - The input triggering the function  
    #Retreives S3 bucket name and key from the S3 event. unqoute_plus decodes special characters from the file path.
    bucket = event['Records'][0]['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding = 'utf-8')

    try:
        df_raw = wr.s3.read_json('s3://{}/{}'.format(bucket,key)) #Read the JSON file from S3 into pandas dataframe using AWS Wrangler 
        df_step_1 = pd.json_normalize(df_raw['items']) #Flattens nested JSON structure under the 'items' into a structured Dataframe
        wr_response = wr.s3.to_parquet(
            df = df_step_1,
            path = os_input_s3_cleansed_layer,
            dataset = True,
            database = os_input_glue_catalog_db_name,
            table = os_input_glue_catalog_table_name, 
            mode = os_input_write_data_operation
        )

        return wr_response
    except Exception as e:
        print(e)
        print("Error getting object {} from bucket {}. Make sure they exist and is in the same region as the function".format(bucket,key))
        raise e


"""
Summary of Workflow
Triggered by an S3 event when a new JSON file is uploaded.
Extracts the file details (bucket & key).
Reads the JSON file into a Pandas DataFrame.
Normalizes nested JSON data (extracts relevant fields).
Writes the transformed data to an S3 bucket in Parquet format.
Registers metadata in AWS Glue Catalog.
Handles errors gracefully.

"""

    


