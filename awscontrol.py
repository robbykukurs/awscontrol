#below is module for managing aws infrastructure
import boto3
#below is module for establishing low-level aws sessions etc
import botocore
#below 2 modules get imported purely because they will throw exceptions and I will have to catch them
import urllib3
import socket
#we also have to import an exception from any modules that we're going to catch
#turns out if an exception is raised within an imported model, python won't just detect it
from botocore.exceptions import ProfileNotFound
from botocore.exceptions import EndpointConnectionError
from urllib3.exceptions import NewConnectionError
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

#FUNCTION FOR USER CONFIRMING THE AWS PROFILE
#we're going to ask user which aws profile name they want to use in order to establish session to aws
#I want to offer the user all available profile names which I think would be cool
def aws_profile_prompt():
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
    prompt_line = str("You can choose from the following profiles to establish a session to AWS: " + s)
    print(prompt_line)

#List of all AWS regions to be used when establishing a session
aws_regions = {
"US East (Ohio)" : "us-east-2",
"US East (N. Virginia)" : "us-east-1",
"US West (N. California)" : "us-west-1",
"US West (Oregon)" : "us-west-2",
"Asia Pacific (Hong Kong)" : "ap-east-1",
"Asia Pacific (Mumbai)" : "ap-south-1",
"Asia Pacific (Osaka-Local)" : "ap-northeast-3",
"Asia Pacific (Seoul)" : "ap-northeast-2",
"Asia Pacific (Singapore)" : "ap-southeast-1",
"Asia Pacific (Sydney)" : "ap-southeast-2",
"Asia Pacific (Tokyo)" : "ap-northeast-1",
"Canada (Central)" : "ca-central-1",
"Europe (Frankfurt)" : "eu-central-1",
"Europe (Ireland)" : "eu-west-1",
"Europe (London)" : "eu-west-2",
"Europe (Paris)" : "eu-west-3",
"Europe (Stockholm)" : "eu-north-1",
"Middle East (Bahrain)" : "me-south-1",
"South America (São Paulo)" : "sa-east-1",
}

#asking user to input the number that corresponds with the AWS region they want to connect to
def aws_region_prompt():
    #giving user options for AWS regions
    print("These are all available AWS regions")
    for i in aws_regions:
        print("For " + str(i) + " enter " + str(aws_regions[i]))

####### THIS IS WHERE THE SCRIPT ACTUALLY STARTS RUNNING #######
##### SESSION IS GETTING ESTABLISHED EVERY TIME SCRIPT RUNS SO THAT WE KNOW WHICH PROFILE TO USE #####
#let's point towards the user's home direcotory

path = expanduser("~")
#let's open the aws credentials file, but if it doesn't exist - we need to catch the exception so we have to do a try section
try:
    aws_credentials_file = open(path + "/.aws/credentials", "r")
#if aws credentials file doesn't exist; let's catch the exception and setup aws access
except FileNotFoundError:
    setup_aws_access()

#function for establishing a user session to AWS and getting all available resources
def connect_to_aws():
    while aws_credentials_file:
        try:
            aws_profile_prompt()
            aws_profile_name = input("Please enter the profile name to use: ")
            aws_region_prompt()
            aws_region_name = input("Please enter the AWS region of your choice: ")
            #as per https://boto3.amazonaws.com/v1/documentation/api/latest/guide/session.html
            session = boto3.session.Session(profile_name=str(aws_profile_name), region_name=str(aws_region_name))
            #pulling all availableresources from the established session https://boto3.amazonaws.com/v1/documentation/api/latest/_modules/boto3/session.html#Session.get_available_services
            resource_list = session.get_available_resources()
            service_list = session.get_available_services()
            s3 = session.resource('s3')
            ec2 = session.resource('ec2')
            #if user enters non-existent profile name, it will throw an exception; let's catch that and return the loop back to top
        except ProfileNotFound:
            print("Sorry, but such an AWS profile can't be found")
            #if exception caught - jump back to try
            continue
            #if user enters non-existent aws region name, it will throw 3 exceptions in a row, let's catch that and return the loop back to top
        except (socket.gaierror, NewConnectionError, EndpointConnectionError):
            print("Sorry, but such an AWS region doesn't exist")
            #if exception caught - jump back to try
            continue
            #if session established successfully, exit the while loop
        break

#here we're naming the main @click group - click is a module helping us
#with creation of CLI options and commands - it's imported on very top
@click.group()
def aws_control():
    """Robby Kukurs' Python CLI tool to manage AWS resources. Please use one of the below options to manage a specific AWS resource"""

@aws_control.group('s3')
def s3():
    """Commands for managing S3 in your AWS accont"""

@s3.command('list')
def list_s3_bucket():
    connect_to_aws()
    for bucket in s3.buckets.all():
        print(bucket.name)

@aws_control.group('ec2')
def ec2():
    """Commands for managing VPC in your AWS accont"""

@ec2.command('list')
def list_ec2_instances():
    connect_to_aws()
    for instance in ec2.instances.all():
        print(instance.name)

if __name__ == '__main__':
    aws_control()
