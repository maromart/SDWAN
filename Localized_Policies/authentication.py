import requests
import json
import sys

requests.packages.urllib3.disable_warnings()

__author__ = "Mario Uriel Romero Martinez"
__version__ = "1.0"
__maintainer__ = "Mario Uriel Romero Martinez"



def get_jsessionid(base_url,username,password):
    
    #base_url=return_baseurl(vmng)

    api = "j_security_check"

    url = base_url + api
    payload = {'j_username': username, 'j_password': password}
    response = requests.post(url=url, data=payload, verify=False)
    response.raise_for_status()
    try:
        if response.status_code==200:

            try:
                print("Getting session cookie...")
                cookies = response.headers["Set-Cookie"]
                jsessionid = cookies.split(";")
                print("OK...")
                data=(jsessionid[0])
                
            except:
                print("No valid JSESSION ID returned\n")
                #exit()
                data=None

    except requests.exceptions.HTTPError as httpe:
        print("HTTP Request error",httpe)
        sys.exit()
    except requests.exceptions.Timeout as toe:
        print("HTTP Request error",toe)
        sys.exit()
    except requests.exceptions.ConnectionError as coe:
        print("HTTP Request error",coe)
        sys.exit()
    except requests.exceptions.RequestException as err:
        print("HTTP Request error",err)
        sys.exit()

    return data

def get_token(jsessionid,base_url):
    headers = {'Cookie': jsessionid}
    api = "dataservice/client/token"
    url = base_url + api
    print("Getting token...")
    try:
        response = requests.get(url=url, headers=headers, verify=False)
        response.raise_for_status()
        if response.status_code == 200:
            print("Token OK...")
            return(response.text)
        else:
            print("No TOKEN...")
            return None
        
    except requests.exceptions.HTTPError as httpe:
        print("HTTP Request error",httpe)
        sys.exit()
    except requests.exceptions.Timeout as toe:
        print("HTTP Request error",toe)
        sys.exit()
    except requests.exceptions.ConnectionError as coe:
        print("HTTP Request error",coe)
        sys.exit()
    except requests.exceptions.RequestException as err:
        print("HTTP Request error",err)
        sys.exit()