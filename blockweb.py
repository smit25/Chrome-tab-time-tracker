import time
from datetime import datetime as dt 

redirect_to_host = "127.0.0.1" # local host IP
host_addr = "‪C:\Windows\System32\drivers\etc\\hosts" # address of hosts file in Windows

website_list = [] # list of webistes which have been blocked

def block(website_url):
    # monday = 0 & sunday = 6
    if dt(dt.now().year,dt.now().month,dt.now().day,9) <= dt.now() <= dt(dt.now().year,dt.now().month,dt.now().day,20) and int(dt.today().weekday())!=6:
        with open(host_addr,'r+') as file:
            data = file.read()
        if website_url in data:
            pass
        else:
            file.write(redirect_to_host+" "+website_url+ "\n")
            print("This website has been blocked")
            global website_list
            website_list.append(website_url)
    return

def unblock():
    with open(host_addr,'r+') as file:
        data = file.readlines() # becomes a list of separate lines
    file.seek(0)
    for line in data:
        if not any(website in line for website in website_list):
            file.write(line)
    file.truncate()
    print("Access has been granted")
    time.sleep(3)
    return




