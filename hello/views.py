from django.http import HttpResponse
from django.shortcuts import render
import os
import requests
import pyodbc

#SQL Server/DB connect info 
server = 'tcp:***'
database = '*****'
username = '*******'
password = '*****'   
driver= '{ODBC Driver 17 for SQL Server}'







identity_endpoint = os.environ["IDENTITY_ENDPOINT"]# Known by applicaton ENV
identity_header = os.environ["IDENTITY_HEADER"]#Known by Application ENV.

#print(identity_endpoint) Remove comment to view 
#print(identity_header) Remove comment to view 


#Function to get access token---If access token is being returned, you should be able to connect using MSI
def get_bearer_token(resource_uri):
    token_auth_uri = f"{identity_endpoint}?resource={resource_uri}&api-version=2019-08-01"
    head_msi = {'X-IDENTITY-HEADER':identity_header}

    resp = requests.get(token_auth_uri, headers=head_msi)
    access_token = resp.json()['access_token']
   
    print("Access token:     ", access_token)
    return access_token

def hello(request):   
    
     #Fucntion to get Bearer token 
    get_bearer_token("https://database.windows.net/")
    try:

        #Connection string using User and Password 
       # cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        
        
        
        #Connection string using System Assigned MSI
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';Authentication=ActiveDirectoryMsi')
        cursor = cnxn.cursor() 
        print("Connected to database Successfully. ")
    except:
        print("Error connecting to database. ")
    
            


    #simple return 
    return HttpResponse("Hello, World!")
