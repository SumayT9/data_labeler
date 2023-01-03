chrome.runtime.sendMessage({url: this.location.href }, async function(response){
    result=response.farewell
    var span = document.createElement( 'span' );
    span.style.backgroundColor = 'yellow';
    var e = document.getElementsByTagName( 'body' )[0];
    var colors = ["red", "green", "blue", "orange", "grey", "yellow"]
    var color_to_rgb = {
        "red" : "#b05151", 
        "green": "#90ee90",
        "blue" : "#87cef8",
        "orange" : "#ad600e",
        "grey" : "#524c47",
        "yellow" : "#d4b413"
    }
    let idx = 0
    let message = ""
    var label_to_color = {}
    for (const key in result){
        label_to_color[key] = colors[idx]
        message += " " + key + " : " + colors[idx]
        idx += 1
    }
    alert(message)
    while ( e ) {
        // If it's a text node, match it against the regexp:
        if ( e.nodeType == Node.ELEMENT_NODE ) {
            for (const key in result){
                for (let i = 0; i < result[key].length; i++){
                    var txt = result[key][i]
                    if (e.textContent.split("\n").join("").split(" ").join("").split("\t").join("") == txt.split("\n").join("").split(" ").join("").split("\t").join("")){
                        e.style.backgroundColor = color_to_rgb[label_to_color[key]]
                        chrome.runtime.sendMessage({test: txt});
                    }
                    } 
                }
            }
        // Advance to next node in DOM (bugfix: skip textarea content):
            
        var n = e.firstChild;
            if ( /^(head|title|script|style|textarea)$/i.test( e.tagName ) ) n = null;
            while (!n && e) {
                n = e.nextSibling;
                e = e.parentNode;
            }
            e = n;
    }
});

