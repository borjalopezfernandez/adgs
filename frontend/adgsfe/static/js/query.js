/* Function to perform a GET method to a URL, sending a JSON for the parameters */
export function request_info_json(url, callback, json, show_loader = false){
    if (show_loader == true){
        var loader = document.getElementById("updating-page");
        loader.className = "loader-render"
    }

    var xmlhttp = new XMLHttpRequest();
    if (callback){
        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var returned_value = callback(this.responseText);
                if (show_loader == true){
                    var loader = document.getElementById("updating-page");
                    loader.className = ""
                }
                return returned_value
            }
            else if (this.readyState == 4 && this.status == 403){
                var permission_denied_response = {
                    "return_code": 403
                };

                return callback(permission_denied_response);
            }
            else if (this.readyState == 4 && this.status == 500){
                var internal_server_error_response = {
                    "return_code": 500
                };

                return callback(internal_server_error_response);
            }
        };
    }

    xmlhttp.open("POST", url, true);
    xmlhttp.setRequestHeader('content-type', 'application/json');
    xmlhttp.send(JSON.stringify(json));
}
