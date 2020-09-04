import time
import os
import base64
import requests
from requests.auth import HTTPProxyAuth
from requests.adapters import HTTPAdapter
from zipfile import ZipFile

#Code to download 1 hour of Logs
end_time=int(time.time())*1000
start_time=int(time.time())*1000 - 3600000

#As you won't be allowed to fetch logs directly, thus Proxy settings below
PROXY_IP="10.20.30.40"      #Proxy IP
PROXY_PORT="8080"           #Proxy Port
API_UNAME="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"        #API Username
API_PASS="eeeeeeee-dddd-cccc-bbbb-aaaaaaaaaaaa"         #API Password
uname_pass=base64.b64decode("ZG9tYWluLmNvLmluXHVzZXJuYW1lOnBhc3N3b3Jk") #Base64 Encoded Username Password, for Domain IDs, use Domain\username:pass

url="https://portal.threatpulse.com/reportpod/logs/sync?apiUsername="+API_UNAME+"&apiPassword="+API_PASS+"&startDate="+str(start_time)+"&endDate="+str(end_time)+"&token=none"
while True:
    try:
        #Code for Proxy
        proxies = {
         "http": "http://"+uname_pass+"@"+str(PROXY_IP)+":"+str(PROXY_PORT),
         "https": "http://"+uname_pass+"@"+str(PROXY_IP)+":"+str(PROXY_PORT),
        }

        #Code to make the request
        r = requests.get(url, proxies=proxies, allow_redirects=True,verify=False)

        #Check if Status code is not 429 (That means its not accessive number of request)
        if str(r.status_code)!="429":
            print "####Downloading Logs####"
            file = open("output.zip", "wb")     #Create Output.zip
            file.write(r.content)               #Dump all logs in form of bytes into the zip
            file.close()
            print "####Download Complete####"
            with ZipFile('output.zip', 'r') as zipObj:
               zipObj.extractall('output')      #Unzip the zip into an output folder 
               os.remove("output.zip")          #Delete the output.zip
            print "####Extraction Complete and Zip deleted, Exiting...####"
            time.sleept(5)
            exit()
        else:
            print r.text
        time.sleep(180)
    except Exception as x:
        print "URL Open timeout!!, Retrying"
        print x
        print url
