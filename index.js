document.getElementById("start").onclick = async () => {
    var n = document.getElementById("tin").value
    chrome.runtime.sendMessage({label: n }, function(response){ result=response.farewell})
    document.getElementById("tin").value = ""
}