
// When the page is loaded, query the state of all the sensors
$(document).ready(function(){
    // TODO When the page is loaded, get the state of all devices.
});

document.getElementById("ultrasonic-enable").onclick = function() {
    var x = new XMLHttpRequest();
    x.open('GET', 'http://' + document.location.host + '/api/ultrasonic/toggle', true);
    x.onload = function (e) {
        if (x.readyState === 4) {
            if (x.status === 200) {
                var data = JSON.parse(x.response);
                document.getElementById("ultrasonic-enable").innerHTML = data["status"];
            }
        }
    };
    x.send();
};
