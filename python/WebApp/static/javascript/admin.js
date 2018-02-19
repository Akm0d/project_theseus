
// When the page is loaded, query the state of all the sensors
$(document).ready(function(){
    ultrasonic_status(toggle=false)
});

document.getElementById("ultrasonic-enable").onclick = function() {
    ultrasonic_status(toggle=true)
};

function ultrasonic_status(toggle){
    var x = new XMLHttpRequest();
    x.open('GET', 'http://' + document.location.host + '/api/ultrasonic' + (toggle? "/toggle": "/status"), true);
    x.onload = function () {
        if (x.readyState === 4) {
            if (x.status === 200) {
                var data = JSON.parse(x.response);
                document.getElementById("ultrasonic-enable").innerHTML = data["status"];
            }
        }
    };
    x.send();
}
