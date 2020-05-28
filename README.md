# Chrome-tab-time-tracker

A simple productivity code where you can track your web activity on Chrome.
Boost your productivity by blocking distracting websites and set a bound on their usage time/day.

## Technology Used:
1) Python
2) Flask Server for extracting the tab info and keeping track of time
3) Chrome API using Javascript for collecting information from Chrome tab acitivity

## How to run the tracker:
1) Click on the 3-dot icon on the top left cornor of your chrome window.
2) Go to more tools and then Extensions
3) Enable the developer mode
4) Click on Load unpacked and load the chrome extension
5) Download Python 3.7 and Flask
6) Go to the directory where your track_tab_time.py is saved and input flask run on your terminal

## How does it work:
Event listeners have been added on chrome.tabs, hence any acitivity is recorded by the listener and sent to the Flask server. The flask server recieves the json data, decodes it and stores it in a dictionary with its corresponding time. Wehn another activity is triggered, the time spent between the current tab and the previous tab is calculated and stored

A separate dictionary (blocked_url) for blocked url and its permissible time is created and can be configured for taking input during runtime. A separate thread is created using python threading for the background loop which constantly keeps track of time. When the time limit for a website in the blocked_url has been reached, the block function from blockweb.py is called and the website is unblocked. 

You can set the work hours, and after the working hour, all the websites are unblocked. 
