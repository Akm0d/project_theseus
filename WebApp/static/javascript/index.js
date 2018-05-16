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
    x.open('GET', 'http://' + document.location.host + '/api/high-scores/');
    x.onload = function () {
        if(x.readyState === 4)
        {
            if(x.status === 200)
            {
                var data = JSON.parse(x.response);
                for(var i = 1; i <=5; i++){
                    document.getElementById("name" + i).innerHTML = '<td id="name' + i + '">' + data['team' + i]['name'] + '</td>';
                    document.getElementById("teamTime" + i).innerHTML = '<td id="teamTime' + i + '">' + data['team' + i]['time'] + '</td>';
                    // console.log(i);
                }
            }
        }
    };
    x.send();
}

function updatePercentage() {
    var y = new XMLHttpRequest();
    var z = new XMLHttpRequest();
    y.open('GET', 'http://' + document.location.host + '/api/successes/');
    z.open('GET', 'http://' + document.location.host + '/api/attempts/');
    y.onload = function () {
        if(y.readyState === 4)
        {
            if(y.status === 200)
            {
                z.onload = function () {
                    if(z.readyState === 4)
                    {
                        if(z.status === 200)
                        {
                            var dividend = JSON.parse(y.response);
                            var divisor = JSON.parse(z.response);
                            document.getElementById("percentID").innerHTML = ((dividend['successes'] / divisor['attempts'])*100).toFixed(1) + '%';
                        }
                    }
                }
            }
        }
    };
    y.send();
    z.send();
}


setInterval(function(){
    // TODO after the project is complete the refresh time can be set based on how long it takes python code to run
    updateTimerText();
}, 1000);

setInterval(function(){
    updateAttemptText();
    updateSuccessText();
    updateTableText();
    updatePercentage();
}, 10000);
