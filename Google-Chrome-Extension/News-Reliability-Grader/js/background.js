// On install
chrome.runtime.onInstalled.addListener(function() {  
  console.log("News Website Classifier Extension Successfully Installed.");

  chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
      chrome.declarativeContent.onPageChanged.addRules([{
        conditions: [new chrome.declarativeContent.PageStateMatcher({
          pageUrl: {urlMatches: '.*'},
        })],
        actions: [new chrome.declarativeContent.ShowPageAction()]
      }]);
  });
});

// On tab change
chrome.tabs.onActivated.addListener(function(activeInfo) {
    chrome.tabs.sendMessage(activeInfo.tabId, {message: "tab-changed"});
});

// On message
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if(request.siteToAnalyze.length > 0) {
    var endpoint = "<API-HOSTNAME-PATH-ENDPOINT-HERE>/classify.php";

    fetch(endpoint, {method: "post", body: JSON.stringify(request)}).then(function(res) {
      if(res.status !== 200) {
        console.error("API call received bad status: " + res.status);
        sendResponse({status: "Error"});
        return;
      }
      res.json().then(function(data) {
        console.log("API call completed Successfully");
        sendResponse({status: "Success", classification: data});
      });
    }).catch(function(err) {
      console.error("API call experienced a fatal error: " + err);
      sendResponse({status: "Error"});
    });
  }

  return true;
});
