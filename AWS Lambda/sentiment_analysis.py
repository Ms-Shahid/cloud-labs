import requests
from textblob import TextBlob

def lambda_handler(event, context):
    
    api_endpoint = '<END_POINTt>'
    api_key = '<API_KEY>'

    try:
        header_parameters = {
            'Content-Type': 'application/json',
            'x-api-key': api_key,
        }

        response = requests.get(api_endpoint, headers=header_parameters)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()[0]  # Read the first item in the list

        # Perform sentiment analysis
        sentiment = TextBlob(data['content']).sentiment

        # Read the HTML template from the file
        with open('template.html', 'r') as template_file:
            html_template = template_file.read()

        # Replace placeholders with actual quote data and author name
        html_response = html_template.replace('{{QUOTE}}', data['content'])
        html_response = html_response.replace('{{AUTHOR}}', data['author'])
        html_response = html_response.replace('{{SENTIMENT}}', f"Polarity: {sentiment.polarity}, Subjectivity: {sentiment.subjectivity}")

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html',
            },
            'body': html_response
        }
    except requests.exceptions.RequestException as error:
        print(error)
        raise Exception('An error occurred while fetching data')
