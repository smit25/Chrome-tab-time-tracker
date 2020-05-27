// ACTIVATION WHEN NEW TAB IS OPENED
chrome.tabs.onActivated.addListener(function (activeInfo) { // Event Fires when the active tab in a window changes.
  chrome.tabs.get(activeInfo.tabId, function (tab) {
    var link = tab.url;// url of new tab
    var xmlhttp = new XMLHttpRequest(); // instantiating new http request
    xmlhttp.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) { // requests data from chrome server
        console.log(this.responseText);
      }
    };
    xmlhttp.open('POST', 'http://127.0.0.1:5000/send_url'); // send the new url to the server
    xmlhttp.send('url=' + link);
  });
});

// UPDATION OF TABS
chrome.tabs.onUpdated.addListener((tabId, change, tab) => { // Fired when a tab is updated
  if (tab.active && change.url) {
    var xhttp = new XMLHttpRequest(); // send new url to the server end
    xhttp.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
        console.log(this.responseText)
      }
    };
    xhttp.open('POST', 'http://127.0.0.1:5000/send_url');
    xhttp.send('url=' + change.url);
  }
});

// UPDATION AND DELETE.
// removal of tab also considered an update

var tabToUrl = {};
chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
  tabToUrl[tabId] = tab.url;
})

chrome.tabs.onRemoved.addListener(function (tabId, removeInfo) { // Fired when a tab is closed
// mapping for getting url of removed tab sinse tab is not available inside onRemoved
  console.log(tabToUrl[tabId]);

  var xmlhttp2 = new XMLHttpRequest();
  xmlhttp2.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      console.log(this.responseText);
    }
  };
  xmlhttp2.open('POST', 'http://127.0.0.1:5000/quit_url');
  xmlhttp2.send('url=' + tabToUrl[tabId]);
  // Remove information for non-existent tab
  delete tabToUrl[tabId];
});
