import os
import boto3
import yaml
import fnmatch
import base64
import shutil

"""
Global Information
"""
lex = boto3.client('lex-models')
lambdaaws = boto3.client("lambda")
s3 = boto3.client("s3")
lambda_bucket = "allengeerlambdas"
rootdir = cwd = os.getcwd()

"""
Place Slots

For each .yaml file in the slots directory, open that file and load the YAML.
Check to see if that slot already exists in AWS, if so set the checksum to enable update.
Write the slot to AWS
"""

os.chdir("%s/slots" %rootdir)
slot_yaml = fnmatch.filter(os.listdir('.'), '*.yaml')

for slot in slot_yaml:
    with open(slot, 'r') as stream:
        try:
            slotdef = yaml.load(stream)
        except yaml.YAMLError as exc:
            print exc
    try:
        slotdef_aws = lex.get_slot_type(name=slotdef["name"], version="$LATEST")
        slotdef["checksum"] = slotdef_aws["checksum"]
    except Exception as e:
        print e
    lex.put_slot_type(**slotdef)


"""
Place Lambdas

For each .yaml file in the lambda directory, open that file and load the YAML.

For each lambda, put the referred to file into the appropriate zip format (with the included python workspace)
Put that zip file in an S3 bucket
Update the lambda code property to include the appropriate S3 information
Write the lambda to AWS
"""

os.chdir("%s/lambda" %rootdir)
lambda_yaml = fnmatch.filter(os.listdir('.'), '*.yaml')
for lambdafile in lambda_yaml:
    with open(lambdafile, 'r') as stream:
        try:
            lambdadef = yaml.load(stream)
        except yaml.YAMLError as exc:
            print exc
    try:
        lamdadef_aws = lambdaaws.get_function(FunctionName=lambdadef["FunctionName"])
        print "do lambda update"
        shutil.make_archive("%s" % lambdadef["FunctionName"], 'zip', "code")
        del lambdadef["Code"]["file"]
        lambdaaws.update_function_code(
            FunctionName=lambdadef["FunctionName"],
            ZipFile=open("%s.zip" %lambdadef["FunctionName"], 'rb').read(),
            Publish=False,
            DryRun=False
        )
    except Exception as e:
        print "do lambda create"
        shutil.make_archive("%s" %lambdadef["FunctionName"], 'zip', "code")
        del lambdadef["Code"]["file"]
        lambdadef["Code"]["ZipFile"] = open("%s.zip" %lambdadef["FunctionName"], 'rb').read()
        lambdaaws.create_function(**lambdadef)

        lambdaaws.add_permission(
            FunctionName=lambdadef["FunctionName"],
            StatementId="%sLEX" %lambdadef["FunctionName"],
            Action='lambda:*',
            Principal='lex.amazonaws.com'
        )


"""
Place Intents

For each .yaml file in the intent directory, open that file and load the YAML.
Check to see if that intent already exists in AWS, if so set the checksum to enable update.
Write the intent to AWS
"""


os.chdir("%s/intents" %rootdir)
intent_yaml = fnmatch.filter(os.listdir('.'), '*.yaml')
for intent in intent_yaml:
    with open(intent, 'r') as stream:
        try:
            intentdef = yaml.load(stream)
        except yaml.YAMLError as exc:
            print exc
    try:
        intentdef_aws = lex.get_intent(name=intentdef["name"], version="$LATEST")
        intentdef["checksum"] = intentdef_aws["checksum"]
    except Exception as e:
        print e
    lex.put_intent(**intentdef)


"""
Place Bots

For each .yaml file in the bot directory, open that file and load the YAML.
Check to see if that bot already exists in AWS, if so set the checksum to enable update.
Write the bot to AWS
"""

os.chdir("%s/bots" %rootdir)
bot_yaml = fnmatch.filter(os.listdir('.'), '*.yaml')
for bot in bot_yaml:
    with open(bot, 'r') as stream:
        try:
            botdef = yaml.load(stream)
        except yaml.YAMLError as exc:
            print exc
    try:
        botdef_aws = lex.get_bot(name=botdef["name"], versionOrAlias="$LATEST")
        botdef["checksum"] = botdef_aws["checksum"]
    except Exception as e:
        print e
    lex.put_bot(**botdef)