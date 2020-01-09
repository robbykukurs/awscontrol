#below is module for managing aws infrastructure
import boto3
#below is module for establishing low-level aws sessions etc
import botocore
#below is module for creating CLI commands
import click
#below is module for dealing with directories and paths in Python
from os.path import expanduser

#Function for setting up aws user access
def setup_aws_access():
    ACCESS_KEY = input("Please provide your AWS ACCESS_KEY here: ")
    SECRET_KEY = input("Please provide your AWS SECRET_KEY here: ")
    profile_name = input("Please provide your AWS profile name here: ")

    #showing Python the correct path to the user's home direcotory
    path = expanduser("~")

    #opening file for editing or creating a new one if it doesn't exist
    aws_config_file = open(path + "/.aws/credentials", "a+")

    #appending the aws profile name and credentials to the aws configuration file
    aws_config_file.write("[" + profile_name + "]\r\n")
    aws_config_file.write("aws_access_key_id = " + ACCESS_KEY+ "\r\n")
    aws_config_file.write("aws_secret_access_key = " + SECRET_KEY+ "\r\n")

    #close the file when done
    aws_config_file.close()

#USER CONFIRMING THE AWS PROFILE
#we're going to ask user which aws profile name they want to use in order to establish session to aws
#I want to offer the user all available profile names which I think would be cool

#showing Python the correct path to the user's home direcotory
path = expanduser("~")
#now let us read the aws credentials file and save it to a variabe
aws_credentials_file = open(path + "/.aws/credentials", "r")
#now let us read the individual lines from the credentials file
contents = aws_credentials_file.readlines()
#profile name is listed in [] so let's filter those entries and add to a list
profile_list = []
for i in contents:
    if "[" and "]" in i:
        profile_list.append(i)
#removing new line characters from end of each list item
final_profile_list = []
for i in profile_list:
    final_profile_list.append(i.strip())
#now we want to convert the profile name list entries to a nice string so we can
#append it to a prompt string later on
s = " "
s = s.join(final_profile_list)
prompt_line = str("You can choose from the following profiles: " + s)
print(prompt_line)

#available_aws_profile_names =
#session_profile_name = input("Please provide your AWS profile name for establishing user session here: ")

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
