beforeSubmit = function(){
    var acconto = document.getElementById('advance_amount').value;
    var prezzo = document.getElementById('ord_amount').value;
    console.log(acconto)
    console.log(parseFloat(acconto)>parseFloat(prezzo));
    if(parseFloat(acconto) > parseFloat(prezzo) || parseFloat(prezzo)==0.00) {
        if((prezzo == '0.00')){
            document.getElementById('errore').innerHTML = "Il prezzo deve essere maggiore di 0.00 €";
            return false;
        }
        if(parseFloat(acconto) > parseFloat(prezzo)){
        console.log('sono qui!');
        document.getElementById('errore').innerHTML = "Errore nell'inserimento: Importo < acconto o Ordine già presente";
        }
        return false;
    }
}

document.addEventListener('DOMContentLoaded', function (data) {
    $("#campoCliente").empty();
    var event_data = '';
    var event_data1 = '';
    var event_data2 = '';
    var event_data3 = '';
    var event_data4 = '';

    event_data += '<p>N° ordine</p>';
    event_data += '<input class="campo" name="ord_num" type="text" placeholder="000000" pattern="[0-9]{6}" required />';

    event_data1 += '<p>Prezzo&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; Anticipo</p>';
    event_data1 += '<input class="campo" id="ord_amount" name="ord_amount" type="text" placeholder="0.00" maxlength="15" pattern="[0-9]+\.[0-9]{2}" required/>';
    event_data1 += '<input class="campo" id="advance_amount" name="advance_amount" type="text" placeholder="0.00" maxlength="15" pattern="[0-9]+\.[0-9]{2}" required/>';

    event_data2 += '<p>Data ordine</p>';
    event_data2 += '<input class="campo" name="ord_date" type="date" min="2000-01-02" max="2100-12-31" required/>';

    event_data4 += '<p>Descrizione ordine</p>';
    event_data4 += '<textarea class="campoDescrizione" name="ord_description" maxlength="60" placeholder="Descrizione ordine..." required></textarea>';

    $("#ord_num").append(event_data);
    $("#prezzi").append(event_data1);
    $("#data").append(event_data2);
    $("#descrizione").append(event_data4);

    $.ajax({
        url: "/api/customers",
        method: 'GET',
        dataType: 'json',
        success: function (data) {

            $.each(data, function (index, value) {

                event_data3 += '<p>Codice cliente&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; Codice agente</p>';
                event_data3 += '<select class="campoCliente" name="cust_code" required>';
                for(i = 0;i<value.cust_code.length;i++) {
                    cust_code = value.cust_code[i][0];
                    console.log(cust_code);
                    event_data3+='<option value="'+cust_code+'">'+cust_code+'</option>';
                }
                event_data3+='</select>';

                event_data3 += '<input class="campoAgente2" name="agent_code" type="text" value="'+value.role+'" readonly/>';

            })
            $("#codiceCA").append(event_data3);
        }
    })
}, false);

