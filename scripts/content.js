let firstNode = null;
count = 0
alert("Green = bio, blue=awards, red=education")
document.addEventListener('mousemove', async function (e) {
    if (count < 1){
        await new Promise(r => setTimeout(r, 2000));
        chrome.runtime.sendMessage({query: this.location.href }, async function(response){
            result=response.farewell
            var fields = result.field
            var paths = result.xpath
            var render_paths = result.renderPath
            let nodes = []
            let labels = []
            for (let i = 0; i < fields.length; i++){
                let valueAtPath = document.evaluate(render_paths[i], document, null, XPathResult.ANY_TYPE, null);
                firstNode = valueAtPath.iterateNext()
                if (firstNode != null){
                    nodes.push(firstNode)
                    labels.push(fields[i])
                }
            }
            for (let j = 0; j < nodes.length; j++){
                nodes[j].classList.add(labels[j])
            } 
            await new Promise(r => setTimeout(r, 10000));
            for (let j = 0; j < nodes.length; j++){
                nodes[j].classList.remove(labels[j])
            } 
        })
        count += 1
    }
})
