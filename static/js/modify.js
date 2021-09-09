beforeSubmit = function() {

    var errorePrezzo = "";
    var ord_num = document.getElementById('ord_num').value;

    var acconto = document.getElementById('advance_amount').value;
    var prezzo = document.getElementById('ord_amount').value;


    if (parseFloat(acconto) > parseFloat(prezzo) || parseFloat(prezzo) == 0.00) {
        console.log("sono mago merlino!")
        if ((prezzo == '0.00')) {
            errorePrezzo += "Il prezzo deve essere maggiore di 0.00€ \n";
        }

        if (parseFloat(acconto) > parseFloat(prezzo)) {
            if (errorePrezzo == "")
                errorePrezzo += "Errore nell'inserimento: Importo < acconto";
            else
                errorePrezzo += "e Importo < acconto";
        }
        document.getElementById("errore").innerHTML = errorePrezzo;
        return false;
    }

}


$(document).ready(function () {
    $.ajax({
        url: "/api/orders/dataorder?ordNum="+ord_num,
        method: 'GET',
        dataType: 'json',
        success: function (data) {
            console.log(data)
            var event_data = '';
            var event_data1 = '';
            var event_data2 = '';
            var event_data3 = '';
            var event_data4 = '';
            $.each(data, function (index, value) {
                event_data += '<p>N° ordine</p>';
                event_data += '<input class="campo" name="ord_num" type="text" placeholder="000000" value="' + value.num_ord + '" readonly/>';

                event_data1 += '<p>Prezzo&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; Anticipo</p>';
                event_data1 += '<input id="ord_amount" class="campo" name="ord_amount" type="text" placeholder="0.00" maxlength="15" pattern="[0-9]+\.[0-9]{2}"value="' + value.importOrder + '" required/>';
                event_data1 += '<input id="advance_amount" class="campo" name="advance_amount" type="text" placeholder="0.00" maxlength="15" pattern="[0-9]+\.[0-9]{2}"value="' + value.advance_ord + '" required/>';

                event_data2 += '<p>Data ordine</p>';
                event_data2 += '<input class="campo" name="ord_date" type="date" min="2000-01-02" max="2100-12-31" value="' + value.ordDate + '" required/>';

                event_data3 += '<p>Codice cliente&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; Codice agente</p>';
                console.log(value.customers[0].cust_code.length); //25

                event_data3 += '<select class="campoCliente2" name="cust_code" required>';
                for (i = 0; i < value.customers[0].cust_code.length; i++) {
                    cust_code = value.customers[0].cust_code[i][0];
                    console.log(cust_code);
                    event_data3 += '<option value="' + cust_code + '">' + cust_code + '</option>';
                }
                event_data3 += '<option value="' + value.Cust_id + '" selected>' + value.Cust_id + '</option></select>';

                if (value.role == 'DIRETTORE') {
                    event_data3 += '<select class="campoAgente1" name="agent_code" required>';
                    for (i = 0; i < value.agents[0].agent_code.length; i++) {
                        agent_code = value.agents[0].agent_code[i][0];
                        console.log(agent_code);
                        event_data3 += '<option value="' + agent_code + '">' + agent_code + '</option>';
                    }
                    event_data3 += '<option value="' + value.Agent_code + '" selected>' + value.Agent_code + '</option></select>';
                } else if (value.role = 'AGENTE') {
                    event_data3 += '<input class="campoAgente2" name="agent_code" type="text" value="' + value.Agent_code + '" readonly/>';
                }
                event_data4 += '<p>Descrizione ordine</p>';
                event_data4 += '<textarea id="textarea" class="campoDescrizione" name="ord_description" maxlength="60" placeholder="Descrizione ordine..." required>' + value.Description + '</textarea>';
            });
            $("#ord_num").append(event_data);
            $("#prezzi").append(event_data1);
            $("#data").append(event_data2);
            $("#codiceCA").append(event_data3);
            $("#descrizione").append(event_data4);
        },
        error: function (data) {
            alert('Caricamento Impossibile!')
        }
    })
})
