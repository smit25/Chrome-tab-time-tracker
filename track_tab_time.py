from flask import Flask, jsonify, request, redirect
import time
from datetime import datetime as dt
#import sys
#sys.path.insert(1,'c:\\Users\\Smit\\Coding')
import threading
from blockweb import block,unblock

app = Flask(__name__)
url_currtime = {} # wesbite and the time they started
url_viewtime = {} # website and time viewed
block_url = {"www.marketplace.org":4} #  Include your website and the its limit here
prev_url = ""
prev_day_viewtime = {} # check history
prev_day = -1 # to check for new day and refresh
main_url = "" # url which is currently being viewed
website_list =[]


def strip_url(url):
    if "http://" in url or "https://" in url:
        url = url.replace("https://", '').replace("http://", '').replace('\"', '')
    if "/" in url:
        url = url.split('/', 1)[0] # only takes domain name as first element in list url, split at '/
    return url

@app.route('/send_url', methods=['POST','GET'])
def send_url():
    resp_json = request.get_data() # get data on server
    params = resp_json.decode()  # decode json data
    url = params.replace("url=", "") # remove 'url='
    global main_url
    main_url = strip_url(url)
    print(" HEY URL RECEIVED ")
    print("currently viewing: " + main_url)
   
    global url_currtime
    global url_viewtime
    global prev_url
    global block_url

    print("previous tab: ", prev_url)
    print("initial db currtime: ", url_currtime)

    if main_url not in url_currtime.keys():
        url_viewtime[main_url] = 0 

    url_currtime[main_url] = int(time.time()) # store the new starting time for every url
    # time.time() is the no. of secs since Jan 1 1970
    
    if prev_url != '' and prev_url not in block_url:
        time_spent = int(time.time() - url_currtime[prev_url])
        url_viewtime[prev_url] = url_viewtime[prev_url] + time_spent

    prev_url = main_url
    print("final viewtimes: ", url_viewtime)

    return jsonify({'message': 'success!'}), 200

@app.route('/quit_url', methods=['POST','GET'])
def quit_url(): # for when the tab is closed
    resp_json = request.get_data()
    print("Url closed: " + resp_json.decode())
    return jsonify({'message': 'quit success!'}), 200


def background():
    
    global main_url
    global url_curr_time
    global url_viewtime
    global block_url
    global prev_day_viewtime
    global website_list

    # TO CHECK IF THE TIME LIMIT OF THE BLOCKED WEBSITE HAS EXCEEDED OR NOT
    while True:
        obj = time.localtime()
        t = time.asctime(obj)
        print(t)
        if main_url in block_url.keys():
            # monday = 0 & sunday = 6
            if dt(dt.now().year,dt.now().month,dt.now().day,9) <= dt.now() <= dt(dt.now().year,dt.now().month,dt.now().day,23) and int(dt.today().weekday())!=2 and main_url not in website_list:    
                if int(time.time() - url_currtime[main_url]) + url_viewtime[main_url]>= block_url[main_url]:
                    website_list.append(main_url)
                    #block(main_url)    # redirects to another script
                    url_viewtime[main_url]=block_url[main_url]
                else:
                    url_viewtime[main_url]+=int(time.time()-url_currtime[main_url])

        # UNBLOCK ALL WEBSITES
        if dt(dt.now().year,dt.now().month,dt.now().day,22) == dt.now():
            #unblock()                   # redirects to another script
            print("Smit")
        # TO CHECK FOR A NEW DAY
        global prev_day
        if int(dt.today().weekday())!=prev_day: # clears all the data when new day starts
            prev_day = int(dt.today().weekday())
            prev_day_viewtime = url_viewtime.copy()
            url_viewtime.clear()
            url_currtime.clear()
        
        time.sleep(3)

if __name__ == '__main__':
    t1 = threading.Thread(target = background)
    t1.start()
    app.run(host='0.0.0.0', port=5000, threaded = True, debug = True, use_reloader = False)