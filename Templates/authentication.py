import requests
import json
requests.packages.urllib3.disable_warnings()


def get_jsessionid(base_url,username, password):
    
    #base_url=return_baseurl(vmng)

    api = "j_security_check"

    url = base_url + api
    payload = {'j_username': username, 'j_password': password}
    response = requests.post(url=url, data=payload, verify=False)
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
    return data

def get_token(jsessionid,base_url):
    headers = {'Cookie': jsessionid}
    api = "dataservice/client/token"
    url = base_url + api
    print("Getting token...")
    response = requests.get(url=url, headers=headers, verify=False)
    if response.status_code == 200:
        print("Token OK...")
        return(response.text)
    else:
        print("No TOKEN...")
        return None