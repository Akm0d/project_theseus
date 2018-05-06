function updateTimerText() {
    var x = new XMLHttpRequest();
    x.open('GET', 'http://' + document.location.host + '/api/timer-text/');
    x.onload = function () {
        if(x.readyState === 4)
        {
            if(x.status === 200)
            {
                var data = JSON.parse(x.response);
                document.getElementById("timerText").innerHTML = '<p>' + data['timer'] + '</p>';
            }
        }
    };
    x.send();
}

function updateAttemptText() {
    var x = new XMLHttpRequest();
    x.open('GET', 'http://' + document.location.host + '/api/attempts/');
    x.onload = function () {
        if(x.readyState === 4)
        {
            if(x.status === 200)
            {
                var data = JSON.parse(x.response);
                document.getElementById("attempts").innerHTML = '<p class="info">Attempts: <span class="info-num">' + data['attempts'] + '</span></p>';
            }
        }
    };
    x.send();
}

function updateSuccessText() {
    var x = new XMLHttpRequest();
    x.open('GET', 'http://' + document.location.host + '/api/successes/');
    x.onload = function () {
        if(x.readyState === 4)
        {
            if(x.status === 200)
            {
                var data = JSON.parse(x.response);
                document.getElementById("successes").innerHTML = '<p class="info">Successes: <span class="info-succ">' + data['successes'] + '</span></p>';
            }
        }
    };
    x.send();
}

function updateTableText() {
    var x = new XMLHttpRequest();
    x.open('GET', 'http://' + document.location.host + '/api/timer-text/');
    x.onload = function () {
        if(x.readyState === 4)
        {
            if(x.status === 200)
            {
                var data = JSON.parse(x.response);
                document.getElementById("timerText").innerHTML = '<p>' + data['timer'] + '</p>';
                console.log(data['timer']);
            }
        }
    };
    x.send();
}

setInterval(function(){
    // TODO after the project is complete the refresh time can be set based on how long it takes python code to run
    updateTimerText();
    updateAttemptText();
    updateSuccessText();
    updateTableText();
}, 1000);
