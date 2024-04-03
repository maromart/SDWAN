
import json
import requests
import csv
from time import time
from time import sleep
import sys
import getpass
from threading import Thread
from utils import *
from authentication import *
from sys import stdout as terminal
from itertools import cycle
from threading import Thread



__author__ = "Mario Uriel Romero Martinez"
__version__ = "1.0"
__maintainer__ = "Mario Uriel Romero Martinez"



def animate():
    for c in cycle(['|', '/', '-', '\\']):
        if done:
            break
        terminal.write('\rworking ' + c)
        terminal.flush()
        sleep(0.1)
    terminal.write('\rDone!    ')
    terminal.flush()

#Set header
def setheader(jsessionid,token):
    if token is not None:
        header = {'Content-Type': "application/json", 'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
    else:
        header = {'Content-Type': "application/json", 'Cookie': jsessionid}

    return header


#Logout
def logouts(header,base_url):
    lourl=f"{base_url}logout?nocache={str(int(time()))}"
    payload={}


    response = requests.request("GET", lourl, headers=header, data=payload, verify=False)

    if response.status_code == 200:
        print("Session closed succesfully")
    else:
        print("Unable to close the session",response.status_code)



#Get all Device templates
def getdt(header,base_url,jfile):
   
    
    dictdevfeat = {}
    listdevcetemp=[]

    dturl="dataservice/template/device"
    dtresponse=requests.get(url=f"{base_url}{dturl}",headers=header,verify=False)
   
    print(f"Getting device templates...")
   

    if dtresponse.status_code==200:
        dtdata=dtresponse.json()["data"]
        for dtd in dtdata:
            listdevcetemp.append({"dtname":dtd["templateName"],"dtid":dtd["templateId"]})

    else:
        print("Error", dtresponse.status_code,dtresponse.text)


    dictdevfeat["data"]=listdevcetemp
    savefile(jfile,dictdevfeat)
    


#Get all devices associated to a Device Template
def get_devices(header,base_url,jfile,dtdjfile):
    dictdev = {}
    
    listdt=[]

    with open(jfile,'r') as jaf:
        jafile=jaf.read()
        jparse=json.loads(jafile)["data"]

    for dix in jparse:
        listdev=[]
        devurl=f"dataservice/template/device/config/attached/{dix['dtid']}"
        print(f"Searching for devices attached to {dix['dtname']}")
        response=requests.get(url=f"{base_url}{devurl}",headers=header,verify=False)
        if response.status_code==200:      
            devresponse=response.json()["data"]
            for device in devresponse:
                listdev.append({"uuid":device["uuid"],"Hostname":device["host-name"]})
        else:
            print("Error retrieving data...",response.status_code)

        listdt.append({dix['dtid']:listdev})

    dictdev["data"]=listdt
    savefile(dtdjfile,dictdev)

#Get csv file
def getcsv(header,base_url,devicename,templateid,deviceid,csvdir):
    listkeys=[]
    listvalues=[]
   
    payload={"templateId":templateid,"deviceIds":[deviceid],"isEdited":False,"isMasterEdited":False}

    input_url="dataservice/template/device/config/input/"
    
    response=requests.post(url=f"{base_url}{input_url}", headers=header,data=json.dumps(payload),verify=False)
    if response.status_code==200:
        csvcfg=response.json()["data"]
        filename = f"{csvdir}{devicename}.csv"
        for cf in csvcfg:
            for k,v in cf.items():
                if k!="csv-status":
                    listkeys.append(k)
                    listvalues.append(v)   

        with open(filename, 'w',newline='',encoding='utf-8') as csvfile: 
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(listkeys)
                csvwriter.writerow(listvalues)  

    else:
            
        print("Error retrieving data...",response.status_code)   


#Get csv for all devices
def get_all_csv_values(header,base_url,jfile,csvdir):

    global done
    done= False

    create_dir(csvdir)
    print("Getting csv files...")
    t = Thread(target=animate)
    t.start()
    
    with open(jfile,'r') as jaf:
        jafile=jaf.read()
        jparse=json.loads(jafile)["data"]
    
    for dt in jparse:
        for k,v in dt.items():
            for device in v:
                getcsv(header,base_url,device["Hostname"],k,device["uuid"],csvdir)

    done = True

if __name__ == "__main__":

    #base_url="https://url/"

    

    vmanage_url=input("Please enter vManager url without https:// ")
    base_url=f"https://{vmanage_url}/"
    user=input("username:")
    password=getpass.getpass()
   

    jsessionid=get_jsessionid(base_url,user,password)
    token=get_token(jsessionid,base_url)
    header=setheader(jsessionid,token)

    jfile="devicetemplates.json"
    dtdjfile="dtdevices.json"
    csvdir="csv_template_values/"

    getdt(header,base_url,jfile)
    get_devices(header,base_url,jfile,dtdjfile)
    get_all_csv_values(header,base_url,dtdjfile,csvdir)
    logouts(header,base_url)
