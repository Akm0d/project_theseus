/**
 * Created by tyler on 2/27/17.
 */

// Constantly update console
var source = new EventSource("/console");
source.onmessage = function(event) {
    document.getElementById("console").innerHTML += "> " + event.data + "<br/>";
    updateScroll()
};

// Add buttons
addEventListener("DOMContentLoaded", function() {
    var commandButtons = document.querySelectorAll(".command");
    for (var i=0, l=commandButtons.length; i<l; i++) {
        var button = commandButtons[i];
        button.addEventListener("click", function(e) {
            e.preventDefault();

            var clickedButton = e.target;
            var command = clickedButton.value;

            var request = new XMLHttpRequest();
            request.open("GET", "/" + command, true);
            request.send();
        });
    }
}, true);

// Stay scrolled to bottom of box
var scrolled = false;
function updateScroll(){
    if(!scrolled){
        var element = document.getElementById("console");
        element.scrollTop = element.scrollHeight;
    }
}
$("#console").on('scroll', function(){
    scrolled=true;
});

