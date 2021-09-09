$(document).ready(function() {
    /*
     * Ordinamento colonne
     */
    $(".ordina").click(function(event) {
        sort = $(this).attr('sort');

        console.log(sort) // stampa il nome della cella se è crescente, stampa -[nome della cella se è decrescente]
        $("#datiTab").empty(); //svuoto la tabella prima di riempirla di nuovo
        $.ajax({

            url: "/api/orders/sort_by/"+sort,
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
                    if(role == 'DIRETTORE'|| role =='AGENTE') {
                        event_data += '<td><details><summary>' + value.Cust_id.cust_name + '</summary>' +
                            '<div>' + 'id: ' + value.Cust_id.id + '<br>city: ' + value.Cust_id.cust_city + '<br>working area: ' + value.Cust_id.working_area + '<br>country: ' + value.Cust_id.cust_country +
                            '<br>grade: ' + value.Cust_id.grade + '<br>opening amt: ' + value.Cust_id.opening_amt + '<br>receive amt: ' + value.Cust_id.receive_amt + '<br>payment amt: '
                            + value.Cust_id.payment_amt + '<br>out standing: ' + value.Cust_id.outstanding_amt + '<br>telephone number: ' + value.Cust_id.phone_no +
                            '</div></details></td>';
                    }
                    if(role == 'DIRETTORE'|| role =='CLIENTE') {

                        event_data += '<td><details><summary>' + value.Agent_code.agent_name + '</summary>' +
                            '<div>' + 'id: ' + value.Agent_code.id + '<br>working area: ' + value.Agent_code.working_area + '<br>commission: ' +
                            value.Agent_code.commission + '<br>telephone number: ' + value.Agent_code.phone_no + '<br>country: ' + value.Agent_code.country +
                            '</div></details></td>';
                    }
                    event_data += '<td>' + value.Description + '</td>';
                    if (role == 'DIRETTORE'|| role =='AGENTE') {
                        event_data += '<td><a class="modLink" href="/changeOrder?ordNum=' + value.num_ord + '"> Modifica </a></td>'
                    }
                    if(role=='AGENTE') {
                        event_data += '<td><a class="modLink" href="/deleteOrder?ordNum=' + value.num_ord + '"> Elimina </a></td>'
                    }
                    event_data += '</tr>';
                });
                $("#datiTab").append(event_data);
            },
            error: function (data) {
                alert('Caricamento Impossibile!')
            }
        });
    })
})