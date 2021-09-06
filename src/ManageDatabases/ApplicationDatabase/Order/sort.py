from flask import jsonify

from src.ManageDatabases.ApplicationDatabase.Agents.agents import agentOrderByID
from src.ManageDatabases.ApplicationDatabase.Customer.customer import OrderByIDCustomer
from src.ManageDatabases.SettingDatabase import connectDatabase, Application_HOST, Application_DATABASE, \
    Application_USERNAME, Application_PASSWORD


def sort_orders(par, role, username):
    payload = []
    content = {}
    connection = connectDatabase(Application_HOST, Application_DATABASE, Application_USERNAME, Application_PASSWORD)

    if par[0] == '-':
        par = par[1:]
        if role == 'AGENTE':
            query = "SELECT * from ORDERS WHERE agent_code = %s ORDER BY " + par + " DESC"
        elif role == 'CLIENTE':
            query = "SELECT * from ORDERS WHERE cust_code= %s ORDER BY " + par + " DESC"
        else:
            query = "SELECT * from ORDERS ORDER BY " + par + " DESC"
    else:
        if role == 'AGENTE':
            query = "SELECT * from ORDERS WHERE agent_code = %s ORDER BY " + par + " ASC"
        elif role == 'CLIENTE':
            query = "SELECT * from ORDERS WHERE cust_code = %s ORDER BY " + par + " ASC"
        else:
            query = "SELECT * from ORDERS ORDER BY " + par + " ASC"

    with connection.cursor() as ordini:

        if role == 'AGENTE' or role == 'CLIENTE':
            ordini.execute(query, (username,))
        else:
            ordini.execute(query)

        sel_orders = ordini.fetchall()

        for result in sel_orders:

            cust_info = OrderByIDCustomer(result[4], connection)
            agent_info = agentOrderByID(result[5], connection)

            for res in cust_info:
                info = {'id': res[0], 'cust_name': res[1], 'cust_city': res[2], 'working_area': res[3],
                        'cust_country': res[4], 'grade': float(res[5]), 'opening_amt': "{:.2f}".format(float(res[6])),
                        'receive_amt': "{:.2f}".format(float(res[7])), 'payment_amt': "{:.2f}".format(float(res[8])),
                        'outstanding_amt': "{:.2f}".format(float(res[9])), 'phone_no': res[10], 'agent_code': res[11]}

            for res in agent_info:
                agent_info = {'id': res[0], 'agent_name': res[1], "working_area": res[2],
                              "commission": "{:.2f}".format(float(res[3])), "phone_no": res[4], "country": res[5]}

            # num decimale, importOrder decimale advance_ord decimali
            content = {'num_ord': float(result[0]), 'importOrder': "{:.2f}".format(float(result[1])),
                       'advance_ord': "{:.2f}".format(float(result[2])), 'ordDate': result[3].strftime("%d/%m/%y"),
                       'Cust_id': info, 'Agent_code': agent_info, 'Description': result[6]}

            payload.append(content)
            content = {}

    return jsonify(payload)