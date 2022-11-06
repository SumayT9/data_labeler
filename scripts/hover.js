// Unique ID for the className.
var MOUSE_VISITED_CLASSNAME = 'crx_mouse_visited';

// Previous dom, that we want to track, so we can remove the previous styling.
var prevDOM = null;

// Mouse listener for any move event on the current document.
document.addEventListener('mousemove', function (e) {
  var srcElement = e.target;

  if (
    srcElement.nodeName == 'P' || 
    (srcElement.nodeName.length == 2 && srcElement.nodeName.match("H.") != null) ||
    srcElement.nodeName == 'LI' || 
    srcElement.nodeName == 'SPAN'|| 
    srcElement.nodeName == 'DIV'
    ) {
    if (prevDOM != null) {
        prevDOM.classList.remove(MOUSE_VISITED_CLASSNAME);
      }
  
      // Add a visited class name to the element. So we can style it.
      srcElement.classList.add(MOUSE_VISITED_CLASSNAME);
  
      // The current element is now the previous. So we can remove the class
      // during the next iteration.
      prevDOM = srcElement;
  }
}, false);

// add onclick message
document.addEventListener('click', function (e) {
  var srcElement = e.target;
  let text = srcElement.textContent
  chrome.runtime.sendMessage({text: text + "|" + location.href + "|" + getXpath(srcElement)}, function(response){ result=response.farewell})
}, false);

function getXpath(element)
  {
    var paths = [];  // Use nodeName (instead of localName) 
    // so namespace prefix is included (if any).
    for (; element && element.nodeType == Node.ELEMENT_NODE; 
           element = element.parentNode)
    {
        var index = 0;
        var hasFollowingSiblings = false;
        for (var sibling = element.previousSibling; sibling; 
              sibling = sibling.previousSibling)
        {
            // Ignore document type declaration.
            if (sibling.nodeType == Node.DOCUMENT_TYPE_NODE)
                continue;

            if (sibling.nodeName == element.nodeName)
                ++index;
        }

        for (var sibling = element.nextSibling; 
            sibling && !hasFollowingSiblings;
            sibling = sibling.nextSibling)
        {
            if (sibling.nodeName == element.nodeName)
                hasFollowingSiblings = true;
        }

        var tagName = (element.prefix ? element.prefix + ":" : "") 
                          + element.localName;
        var pathIndex = (index || hasFollowingSiblings ? "[" 
                   + (index + 1) + "]" : "");
        paths.splice(0, 0, tagName + pathIndex);
    }

    return paths.length ? "/" + paths.join("/") : null;
};
