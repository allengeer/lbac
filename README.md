# LexBot as Code (LBaC)

This application expects the definition of a lex bot, lex intents, lex slots, and the corresponding lambdas to
be done via YAML definitions in the corresponding directory. This is a sample application.


## Boto3 Configuration
You will need to configure Boto3 to use your AWS access keys.

In your home directory create two files

### ~/.aws/config
    [default]
    region=us-east-1

### ~/.aws/credentials
    [default]
    aws_access_key_id = <ACCESS KEY ID>
    aws_secret_access_key = <SECRET ACCESS KEY>


## How To Use
You will need to define your corresponding bots, intents, slot types, and lambdas in the corresponding directories.
You will need to follow the yaml specification shown in the HelloWorld samples.

For lambdas, you will need to put the fullfillment script in the code subdirectory.
In the YAML you will need to set the handler to point to the function to execute in that script in the format

    filename.functionname

For example, in our script the file is *sayhello.py* and the function is *execute* so the handler is *sayhello.execute*

To point the intent at a lambda you deploy you will have to specify the ARN of the lambda you deploy which likely
includes your member id for your AWS account.

Once you have setup your boto3, yaml and scripts, you simply run the deploy.py and it will deploy or update
all the resources you defined.