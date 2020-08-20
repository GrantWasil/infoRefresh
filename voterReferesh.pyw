import http.client as httplib
import threading
import time
from tkinter import messagebox
import subprocess
import boto3 
from boto3.session import Session

# The following variables are the credentials for the AWS IAM account: jeffco-test. They need to be moved to a config file
ACCESS_KEY = 'accesskey'
SECRET_KEY = 'secretkey'
access_bucket = 'accessbuket'

# The following variables are used to track the download file for timing purposes 
download = None
download_available = threading.Event()

#checkInternet(url=String, timeout=Number) Returns Boolean
# Returns True if a valid connection to url can be established
# Will default to "www.google.com" if no variables are provided
def checkInternet(url="www.google.com", timeout=3, maxattempts=3):
    conn = httplib.HTTPConnection(url, timeout=timeout)
    tries = 0
    while tries < maxattempts:
        try:
            conn.request("HEAD", "/")
            conn.close()
            return True
        except Exception as e:
            tries += 1
            messagebox.showinfo("Attempt Number", tries)
            time.sleep(90)
    return False

# updateVoterInfo() Downloads File
# Downloads a specific file from AWS S3 Server
def updateVoterInfo() :
    global download
    s3 = boto3.client ('s3',
                   aws_access_key_id=ACCESS_KEY,
                   aws_secret_access_key=SECRET_KEY)
    s3.download_file(access_bucket,
                'CE-VR011A.txt',
                './CE-VR011A.txt')
    download = True
    download_available.set()

# runRefreshData(file=String) Runs External File
# Runs a BATCH File to import our data into SQL 
def runRefreshData(file="3-REFRESHDATA.BAT") :
    location = f"./{file}"
    subprocess.Popen(file)

# If there is a valid internet connection, update the voter records. Otherwise display an error
if checkInternet() :
    # Thread is used to ensure the file is finished downloading before refreshing the data 
    thread = threading.Thread(target=updateVoterInfo())
    thread.start
    download_available.wait()
    runRefreshData()
else :
    messagebox.showinfo("Connectivity Problem", "Unable to get latest Voter Registration Data. Please contact your IT Rover")

# Code is minified using pyminify before being bundled with pyinstaller
