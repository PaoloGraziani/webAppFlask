
$(document).ready(function () {
    username = $(this).attr('username');
$.ajax({
    url: "/api/orders/agent?id_agent=" + username,
    method: 'GET',
    dataType: 'json',
    success: function (data) {
        console.log(data);
        var event_data = '';
        $.each(data, function (index, value) {

            event_data += '<tr>';
            event_data += '<td>' + value.num_ord + '</td>';
            event_data += '<td>' + value.importOrder + '</td>';
            event_data += '<td>' + value.advance_ord + '</td>';
            event_data += '<td>' + value.ordDate + '</td>';
            event_data += '<td><details><summary>' + value.Cust_id.cust_name + '</summary>' +
                '<div>' + 'Id: ' + value.Cust_id.id + '<br>Città: ' + value.Cust_id.cust_city + '<br>Area di lavoro: ' + value.Cust_id.working_area + '<br>Nazione: ' + value.Cust_id.cust_country +
                '<br>Grado: ' + value.Cust_id.grade + '<br>Importo di apertura: ' + value.Cust_id.opening_amt + '<br>Importo da ricevere: ' + value.Cust_id.receive_amt + '<br>Importo del pagamento: '
                + value.Cust_id.payment_amt + '<br>Importo in sospeso: ' + value.Cust_id.outstanding_amt + '<br>Numero di telefono: ' + value.Cust_id.phone_no +
                '</div></details></td>';

            event_data += '<td>' + value.Description + '</td>';
            event_data += '<td><a class="modLink" href="/changeOrder?ordNum=' + value.num_ord + '"> Modifica </a></td>'
            event_data += '<td><a class="modLink" href="/deleteOrder?ord_num=' + value.num_ord + '"> Elimina </a></td>'
            event_data += '</tr>';
        });
        $("#datiTab").append(event_data);
    },
    error: function (data) {
        alert('Caricamento Impossibile!')
    }
})
});