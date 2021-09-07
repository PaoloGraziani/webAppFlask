$(document).ready(function () {
    $.ajax({
        url: "/api/orders/costumers?cust_id="+username,
        method: 'GET',
        dataType: 'json',
        success: function (data) {
            console.log(data);
            var event_data = '';
            $.each(data, function (index, value) {
                event_data += '<tr>';
                event_data += '<td class="tdCliente">' + value.num_ord + '</td>';
                event_data += '<td class="tdCliente">' + value.importOrder + '</td>';
                event_data += '<td class="tdCliente">' + value.advance_ord + '</td>';
                event_data += '<td class="tdCliente">' + value.ordDate + '</td>';
                event_data += '<td class="tdCliente"><details><summary>' + value.Agent_code.agent_name + '</summary>' +
                    '<div>' + 'Id: ' + value.Agent_code.agent_code + '<br>Area di lavoro: ' + value.Agent_code.working_area + '<br>Commissione: ' +
                    value.Agent_code.commission + '<br>Numero di telefono: ' + value.Agent_code.phone_no + '<br>Nazione: ' + value.Agent_code.country +
                    '</div></details></td>';
                event_data += '<td class="tdCliente">' + value.Description + '</td>';
                event_data += '</tr>';
            });
            $("#datiTab").append(event_data);
        }
    })
})
