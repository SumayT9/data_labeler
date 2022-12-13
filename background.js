var serverhost = 'http://127.0.0.1:8000';
var paths;
var response;

	chrome.runtime.onMessage.addListener(
		function(request, sender, sendResponse) {
            var url
			console.log(request)
            if (request.text){
			url = serverhost + '/data_labeler/write/?text='+ encodeURIComponent(request.text);
			fetch(url)
			.then(response => response.json())
			.then(response => sendResponse({farewell:response}))
			.catch(error => console.log(error))
            } else if (request.label) {
            url = serverhost + '/data_labeler/set_field/?label='+ encodeURIComponent(request.label);
			fetch(url)
			.then(response => response.json())
			.then(response => sendResponse({farewell:response}))
			.catch(error => console.log(error))
            }
			else if (request.query){
				url = serverhost + '/data_labeler/get_paths/?query='+ encodeURIComponent(request.query);
				fetch(url)
				.then(response => response.json())
				.then(response => sendResponse({farewell:response}))
				.catch(error => console.log(error))
			}
			else if (request.url){
				url = serverhost + '/data_labeler/extract_text/?query='+ encodeURIComponent(request.url);
				fetch(url)
				.then(response => response.json())
				.then(response => sendResponse({farewell:response}))
				.catch(error => console.log(error))

			} else if (request.debug){
				url = serverhost + '/data_labeler/debug/?query='+ encodeURIComponent(request.debug);
				fetch(url)
				.then(response => response.json())
				.then(response => sendResponse({farewell:response}))
				.catch(error => console.log(error))

			}
			
			return true;  // Will respond asynchronously.
		  
	});


	
