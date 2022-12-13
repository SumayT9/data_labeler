chrome.runtime.sendMessage({url: this.location.href }, async function(response){
    result=response.farewell
    var span = document.createElement( 'span' );
    span.style.backgroundColor = 'yellow';
    var e = document.getElementsByTagName( 'body' )[0];
    while ( e ) {
        // If it's a text node, match it against the regexp:
        if ( e.nodeType == Node.TEXT_NODE ) {
            
            for (const key in result){
                
                for (let i = 0; i < result[key].length; i++){
                    var txt = result[key][i]
                    if (e.textContent.split("\n").join("").split(" ").join("").split("\t").join("") == txt.split("\n").join("").split(" ").join("").split("\t").join("")){
                        e.parentNode.backgroundColor = 'blue'
                        chrome.runtime.sendMessage({test: txt});
                        // e.parent.backgroundColor = 'blue'
                    } else {
                        chrome.runtime.sendMessage({debug: txt + "|" + e.textContent})
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
//     var fields = result.field
//     var paths = result.xpath
//     var render_paths = result.renderPath
//     let nodes = []
//     let labels = []
//     for (let i = 0; i < fields.length; i++){
//         let valueAtPath = document.evaluate(render_paths[i], document, null, XPathResult.ANY_TYPE, null);
//         firstNode = valueAtPath.iterateNext()
//         if (firstNode != null){
//             nodes.push(firstNode)
//             labels.push(fields[i])
//         }
//     }
//     for (let j = 0; j < nodes.length; j++){
//         nodes[j].classList.add(labels[j])
//     } 
//     await new Promise(r => setTimeout(r, 10000));
//     for (let j = 0; j < nodes.length; j++){
//         nodes[j].classList.remove(labels[j])
//     } 
// })

        // {
        //     "matches": ["<all_urls>"],
        //     "js" : ["scripts/content.js"],
        //     "css" : ["scripts/content.css"],
        //     "run_at": "document_end",
        //     "all_frames": true
        // }

// let firstNode = null;
// count = 0
// alert("Green = bio, blue=awards, red=education")
// document.addEventListener('mousemove', async function (e) {
//     if (count < 1){
//         await new Promise(r => setTimeout(r, 2000));
//         chrome.runtime.sendMessage({url: this.location.href }, async function(response){
//             result=response.farewell
//             for (const key in result){

//             }
//             var fields = result.field
//             var paths = result.xpath
//             var render_paths = result.renderPath
//             let nodes = []
//             let labels = []
//             for (let i = 0; i < fields.length; i++){
//                 let valueAtPath = document.evaluate(render_paths[i], document, null, XPathResult.ANY_TYPE, null);
//                 firstNode = valueAtPath.iterateNext()
//                 if (firstNode != null){
//                     nodes.push(firstNode)
//                     labels.push(fields[i])
//                 }
//             }
//             for (let j = 0; j < nodes.length; j++){
//                 nodes[j].classList.add(labels[j])
//             } 
//             await new Promise(r => setTimeout(r, 10000));
//             for (let j = 0; j < nodes.length; j++){
//                 nodes[j].classList.remove(labels[j])
//             } 
//         })
//         count += 1
//     }
// })
