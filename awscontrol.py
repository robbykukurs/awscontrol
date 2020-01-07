#below is module for managing aws infrastructure
import boto3
#below is module for establishing low-level aws sessions etc
import botocore
#below is module for creating CLI commands
import click
#below is module for dealing with directories and paths in Python
from os.path import expanduser

#Setting up aws user access
def setup_aws_access():
    ACCESS_KEY = input("Please provide your AWS ACCESS_KEY here: ")
    SECRET_KEY = input("Please provide your AWS SECRET_KEY here: ")
    profile_name = input("Please provide your AWS profile name here: ")

    #showing Python the correct path to the aws configuration aws configuration file
    path = expanduser("~")

    #opening file for editing or creating a new one if it doesn't exist
    aws_config_file = open(path + "/.aws/credentials", "a+")

    #appending the aws profile name and credentials to the aws configuration file
    aws_config_file.write("[" + profile_name + "]\r\n")
    aws_config_file.write("aws_access_key_id = " + ACCESS_KEY+ "\r\n")
    aws_config_file.write("aws_secret_access_key = " + SECRET_KEY+ "\r\n")

    #close the file when done
    aws_config_file.close()

if __name__ == '__main__':
    setup_aws_access()

#aws session is going to be established by using environmental variables
#session = boto3.Session(
#    aws_access_key_id=ACCESS_KEY,
#    aws_secret_access_key=SECRET_KEY,
#    aws_session_token=SESSION_TOKEN,
#)


#def cli():
#    """Robby Kukur's CLI tool to connect to and manage AWS cloud"""
#
#@cli.group('setup')
#def setup():
#    """Setting up AWS environment"""
#
#@setup.command('accountid')
#
#if __name__ == '__main__':
#    cli()
