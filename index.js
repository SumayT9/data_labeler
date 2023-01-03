document.getElementById("start").onclick = async () => {
    var n = document.getElementById("tin").value
    chrome.runtime.sendMessage({label: n }, function(response){ result=response.farewell})
    document.getElementById("tin").value = ""
}

document.getElementById("extract").onclick = async () => {
    // chrome.runtime.sendMessage({url: "fdjhakf" }, function(response){ result=response.farewell})
    var page_url;
    chrome.tabs.query({'active': true, 'windowId': chrome.windows.WINDOW_ID_CURRENT},
    function(tabs){
      page_url = tabs[0].url;
      chrome.scripting.executeScript({
        target:{tabId : tabs[0].id},
        files : ['scripts/label_visualization.js']
      })
    })
//       chrome.runtime.sendMessage({url: page_url }, function(response){ 
//         result=response.farewell})
//    }
// );
}
