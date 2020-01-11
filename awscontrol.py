#below is module for managing aws infrastructure
import boto3
#below is module for establishing low-level aws sessions etc
import botocore
#we also have to import an exception from botocore that we're going to catch
#turns out if an exception is raised within an imported model, python won't just detect it
from botocore.exceptions import ProfileNotFound
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

####### THIS IS WHERE THE SCRIPT ACTUALLY STARTS RUNNING #######

#here we're naming the main @click group - click is a module helping us
#with creation of CLI options and commands - it's imported on very top
@click.group()
def aws_control():
    """Robby Kukurs' Python CLI tool to manage AWS resources. Please use "user connect" command to establish session first"""

#here we're naming the "user" command
@aws_control.group('user')
def user():
    """Commands for connecting to AWS and establishing a user session. Use the "connect" option to start session"""

@user.command('connect')
#FUNCTION FOR ESTABLISHING USER SESSION TO aws - it will only stop when a valid aws profile is selected and session is established
# check if the aws credentials file exists, if not -  run setup_aws_access first
# then run while loop for aws credentials file and establish session based on input
# if incorrect profile name provided - keep within the loop till valid name provided

#below function can be called whatever you want, it will automatically go with
#above @click user.command - so sequence is very important here
def establish_session_to_aws():
    #let's point towards the user's home direcotory
    path = expanduser("~")
    #let's open the aws credentials file, but if it doesn't exist - we need to catch the exception so we have to do a try section
    try:
        aws_credentials_file = open(path + "/.aws/credentials", "r")
    #if aws credentials file doesn't exist; let's catch the exception and setup aws access
    except FileNotFoundError:
        setup_aws_access()

    while aws_credentials_file:
        try:
            aws_profile_prompt()
            aws_profile_name = input("Please enter the profile name to use: ")
            #establishing aws user session using the profile
            session = boto3.Session(profile_name=str(aws_profile_name))
        #if user enters non-existent profile name, it will throw an exception; let's catch that and return the loop back to top
        except ProfileNotFound:
            print("Sorry, but such an AWS profile can't be found")
            #if exception caught - jump back to try
            continue
        #if session established successfully, exit the while loop
        break

if __name__ == '__main__':
    aws_control()
