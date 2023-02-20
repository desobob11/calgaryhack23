function sendDataCallback() {
    //check if respone is ready
    console.log("Data creation response received");
    getDate(); 
    dataDiv = document.getElementById("sent-data-container");
    // set current data text
    dataDiv.innerHTML = xhr.responseText;
}

function sendData() {
    dataToSend = document.getElementById('data-input').value;
    if (!dataToSend) {
        console.log("Data is empty.");
        return;
    }
    console.log("Sending data: " + dataToSend);
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = sendDataCallback();
    // asynchronous requests
    xhr.open("POST", "http://localhost:6969/users", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    // Send the request over the network
    xhr.send(JSON.stringify({"data": dataToSend}));
}