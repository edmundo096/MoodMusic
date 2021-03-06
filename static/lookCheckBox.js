function post(path, params, method) {
    method = method || "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
         }
    }

    document.body.appendChild(form);
    form.submit();
}

function getCheckBox(Form, typeOfSearch){
	mood="mood:";

    // For the mood types.
    if (typeOfSearch == 'mood')
        mood += ' ' + 'mood:';
    else if (typeOfSearch == 'genre')
        mood += ' ' + 'genre:';

	for (i=0 ; i<Form.elements.length; i++){
		
		if(Form.elements[i].type =="checkbox"){
			if(Form.elements[i].checked==true){
				mood += " " + Form.elements[i].getAttribute('data-mood');
			}
		}
		
	}
	post("/home",{ search: mood})
}
