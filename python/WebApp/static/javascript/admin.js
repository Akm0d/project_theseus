
// When the page is loaded, query the state of all the sensors
$(document).ready(function(){

});

document.getElementById("ultrasonic-enable").onclick = function() {
    var x = new XMLHttpRequest();
    x.open('GET', 'http://' + document.location.host + '/api/ultrasonic/toggle', false);
    x.send();
    var data = JSON.parse(x.response);
    document.getElementById("ultrasonic-enable").innerHTML = data["status"];
};
