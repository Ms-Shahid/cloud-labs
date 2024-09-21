import boto3

from textblob import TextBlob

import json

import time

import urllib.parse

import base64



def lambda_handler(event, context):

    # Initialize AWS services

    textract = boto3.client('textract')

    s3 = boto3.client('s3')



    # Define S3 bucket and object key

    bucket_name = 's3-bucket-lambda-layer-test'

    key = 'sample.png'



    try:

        # Start Textract job

        response = textract.start_document_text_detection(

            DocumentLocation={'S3Object': {'Bucket': bucket_name, 'Name': key}}

        )

        job_id = response['JobId']



        # Poll Textract job status

        while True:

            result = textract.get_document_text_detection(JobId=job_id)

            if result['JobStatus'] in ['SUCCEEDED', 'FAILED']:

                break

            time.sleep(5)



        # Process Textract result

        if result['JobStatus'] == 'SUCCEEDED':

            extracted_text = " ".join([block['Text'] for block in result['Blocks'] if block['BlockType'] == 'LINE'])

            blob = TextBlob(extracted_text)

            sentiment = blob.sentiment

        else:

            raise Exception("Textract job failed")



        # Read image from S3 and encode as base64 for data URI

        image_object = s3.get_object(Bucket=bucket_name, Key=key)

        image_content = image_object['Body'].read()

        image_data_uri = f"data:image/png;base64,{base64.b64encode(image_content).decode()}"



        # Read HTML content

        with open('template.html', 'r') as file:

            html_template = file.read()



        html_content = html_template.format(

            image_data_uri=image_data_uri,

            extracted_text=extracted_text,

            polarity=sentiment.polarity,

            subjectivity=sentiment.subjectivity

        )



        return {

            'statusCode': 200,

            'headers': {'Content-Type': 'text/html'},

            'body': html_content

        }

    except Exception as e:

        return {

            'statusCode': 500,

            'body': f'<html><body><h1>Error</h1><p>{str(e)}</p></body></html>',

            'headers': {'Content-Type': 'text/html'}

        }