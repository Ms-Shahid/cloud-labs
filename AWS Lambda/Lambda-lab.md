
## Cloud lab - 1 AWS Lambda Layers

#### Intro AWS lambda - objectives
- we will learn to deploy Lambda functions with conventional deployment packages and layers, enabling we to perform tasks like API calls, sentiment analysis, and processing image text from an S3 bucket.
- AWS Lambda, provided by Amazon Web Services, is a serverless platform that helps code execution without the need to manage underlying servers. 
- creating a Lambda function with Python, incorporating the requests library to enable API interactions. Then, we will package and deploy this function with its dependencies. 
- Next, we will optimize by creating a Lambda layer with the requests library, allowing for more efficient code editing and package management. 
- we’ll also delve into sentiment analysis by adding the textblob library to a Lambda layer and applying this to analyze text data. 
- Finally, we’ll learn to share this textblob layer across multiple Lambda functions, including the analysis of the text from an image stored in an S3 bucket.

### Architecture overview

![High Level Architecture](https://github.com/Ms-Shahid/cloud-labs/blob/master/resoruces/AWS%20Lambda%20Layers.png)


### Getting started 

AWS Lambda is a serverless platform that helps code execution without the need to manage underlying servers. We write the code, and AWS Lambda takes care of where and how it runs. However, sometimes, our code needs extra dependencies or libraries that aren’t included by default. This is where Lambda layers come in.

Lambda layers are helpful additions to the AWS Lambda functions. These layers are essentially .zip files packed with extra libraries, code, or configurations that the Lambda function can use. They can include things like:

    - Libraries: These are extra code libraries that the Lambda function needs to work properly.

    - Custom runtimes: If the Lambda function needs a specific programming environment that’s not already available in AWS Lambda, we can add it via layers.

    - Configuration files: These are the settings and instructions that tell the Lambda function how to act.

with lambda layer, we can easily store them into seperate layer, instead of replicating them into each lambda function. 

Lambda functions keep additional components separate from the main function code by utilizing Lambda layers, ensuring a more organized and modular structure.

invoke url : 
API key : 

### Triggering the lambda call via AWS cli

- First, create a virtual environment named virtual_env using Python 3.11 with python3.11 -m venv virtual_env. Then, activate this environment using source ./virtual_env/bin/activate. Install the requests library inside the environment with pip install requests and exit the environment using deactivate.

```
python3.11 -m venv virtual_env && source virtual_env/bin/activate && pip install requests && deactivate
```

- The requests library is installed in the virtual_env/lib/python3.11/site-packages folder. All the files need to be in the site-packages folder to create a package for the Lambda function. These commands will create a zip archive of all the files from the site-packages directory, and copy it into the LambdaFolder with the file name requests_packages.zip.

```
cd virtual_env/lib/python3.11/site-packages && zip -r requests_package.zip . && cp requests_package.zip /usercode/LambdaFolder && cd /usercode/LambdaFolder
```

- Enter the following command to include the lambda_function.py and template.html in the file name requests_packages.zip:
```
zip requests_package.zip lambda_function.py template.html
```

- Finally, deploy the Lambda function function_api_call with the new package we have created. Enter the following command to deploy the package to the Lambda function:
```
aws lambda update-function-code --function-name function_call_api --zip-file fileb://requests_package.zip  --no-cli-pager
```

### Response output 
```
{
    "FunctionName": "function_call_api",
    "FunctionArn": "arn:aws:lambda:us-east-1:656315963027:function:function_call_api",
    "Runtime": "python3.11",
    "Role": "arn:aws:iam::656315963027:role/LambdaExecutionRole",
    "Handler": "lambda_function.lambda_handler",
    "CodeSize": 9267190,
    "Description": "",
    "Timeout": 3,
    "MemorySize": 128,
    "LastModified": "2024-09-21T14:09:56.000+0000",
    "CodeSha256": "n5iW+1D/nTQp/kW+O8vnEyYGXi2j7CquXFWNhLzRCZ0=",
    "Version": "$LATEST",
    "TracingConfig": {
        "Mode": "PassThrough"
    },
    "RevisionId": "9c65402d-9a31-4141-950a-fb4c38ccdb2a",
    "State": "Active",
    "LastUpdateStatus": "InProgress",
    "LastUpdateStatusReason": "The function is being created.",
    "LastUpdateStatusReasonCode": "Creating",
    "PackageType": "Zip",
    "Architectures": [
        "x86_64"
    ],
    "EphemeralStorage": {
        "Size": 512
    },
    "SnapStart": {
        "ApplyOn": "None",
        "OptimizationStatus": "Off"
    },
    "RuntimeVersionConfig": {
        "RuntimeVersionArn": "arn:aws:lambda:us-east-1::runtime:93e1685a33effc0cd2497a9a132c7328deb2e03b8a600ecae522c00fc95a1c8f"
    },
    "LoggingConfig": {
        "LogFormat": "Text",
        "LogGroup": "/aws/lambda/function_call_api"
    }
}
```

### Execute the following commands in the code playground above:

The terminal of the code playground will open in the LambdaFolder directory. Here, we’ll create the requestsFolder/python folders and install the requests library.
```
pip install requests -t ./requestsFolder/python
```

Navigate to the requestsFolder directory and compress the contents into a .zip file:
```
cd requestsFolder
zip -r requests_layer.zip .
```

We’ve successfully created the requests package for the Lambda layer.

Enter the following command to create requests_layer with the package we’ve created with the requests library.
```
aws lambda publish-layer-version --layer-name requests_layer --zip-file fileb://requests_layer.zip --compatible-runtimes python3.11 --no-cli-pager
```

### Attach the layer to the Lambda function

Follow these steps to attach the Lambda layer to the Lambda function function_with_layers:

1. Navigate to the Lambda function, function_with_layers, in the AWS Management Console.

2. Scroll to the “Layers” section and click the “Add a layer” button.

3. Select “Custom layers” and choose the “requests_layer” from the “Custom layers” drop-down list.

4. Select the “1” from the “Version” drop-down list and click the “Add” button to add the layer to the Lambda function.

Now, the requests library is included in the Lambda function, function_with_layers, as a layer.


### Focus on Core Logic with Lambda Layers

So far, we’ve learned that Lambda layers are very useful in managing package size and dependencies, which in turn allows for more straightforward editing and updating of the code. A key advantage of using Lambda layers is their ability to help us focus on the core function logic.

Let’s consider a scenario where our objective is to perform sentiment analysis on the quote we receive from the API Gateway. By utilizing Lambda layers, we can integrate the textblob library for natural language processing without cluttering our core Lambda function code with dependency management.

In this task, we’ll create a Lambda layer with the textblob library to perform sentiment analysis on quotes text. This approach helps separate core function logic from dependencies, allowing us to independently update the Lambda function code and dependencies. We’ll use the two features of the textblob library: Polarity and Subjectivity. After the completion of this task, the provisioned infrastructure would be similar to the one shown in the figure below:

![lambda-layer](https://github.com/Ms-Shahid/cloud-labs/blob/master/resoruces/lambda-layer.png)


Execute the following commands in the terminal of the code playground above:

    The terminal of the code playground will open in the LambdaFolder directory. Here, we’ll create the TextBlobFolder/python folders and install the textblob library.
    ```
    pip install textblob -t ./TextBlobFolder/python
    ```

Ace Editor

    Navigate to the TextBlobFolder directory and compress the contents into a .zip file:
    ```
    cd TextBlobFolder
zip -r textblob_layer.zip .
    ```

Ace Editor

We’ve successfully created the textblob package for the Lambda layer.

    Enter the following command to create textblob_layer with the textblob library we’ve installed.
    ```
    aws lambda publish-layer-version --layer-name textblob_layer --zip-file fileb://textblob_layer.zip --compatible-runtimes python3.11 --no-cli-pager
    ```

Ace Editor

We’ve successfully created the Lambda layer with the textblob library.
