var event_data = '';
var event_data1 = '';
document.addEventListener('DOMContentLoaded', function (data) {
    event_data += '<h1 aria-describedby="descLog" id="titolo">Login</h1>';
    event_data += '<form action="login" method="post">' +
        '<input aria-label="Inserisci il tuo username." class="campo" name="username" type="text" maxlength="6" pattern="[ACD0-9]{4,}" placeholder="Username" required/>' +
        '<input aria-label="Inserisci la tua password." class="campo" name="password" type="password" maxlength="16" placeholder="Password" required/>' +
        '<input type="hidden" name="ruolo" />' +
        '<br/><br/><br/>' +
        '<input id="bottone" type="submit" value="Accedi"/>' +
        '</form>';
    <!-- Accessibilita' -->
    event_data += '<p id="descLog">In questa pagina puoi effettuare il login per visualizzare la lista dei tuoi ordini.</p>'
    event_data1 += '<hr/>';
    event_data1 += '<p>Paolo Graziani - Lorenzo Genghini &copy 2021</p>';
    $("#sfondoCred").append(event_data);
    $("#marchio").append(event_data1);
},false);