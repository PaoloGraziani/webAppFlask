import psycopg2
from flask import jsonify
from src.ManageDatabases.settingDatabase import Application_HOST, Application_DATABASE, Application_USERNAME, \
                                                Application_PASSWORD, closeCursor, connectDatabase, closeConnection

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
                info = {'id': result[4], 'cust_name': res[1], 'cust_city': res[2], 'working_area': res[3],
                        'cust_country': res[4], 'grade': float(res[5]), 'opening_amt': "{:.2f}".format(float(res[6])),
                        'receive_amt': "{:.2f}".format(float(res[7])), 'payment_amt': "{:.2f}".format(float(res[8])),
                        'outstanding_amt': "{:.2f}".format(float(res[9])), 'phone_no': res[10], 'agent_code': res[11]}

            for res in agent_info:
                agent_info = {'agent_code': res[0], 'agent_name': res[1], "working_area": res[2],
                              "commission": "{:.2f}".format(float(res[3])), "phone_no": res[4], "country": res[5]}

            #num decimale, importOrder decimale advance_ord decimali
            content = {'num_ord': float(result[0]), 'importOrder': "{:.2f}".format(float(result[1])),
                       'advance_ord': "{:.2f}".format(float(result[2])), 'ordDate': result[3].strftime("%d/%m/%y"),
                       'Cust_id': info, 'Agent_code': agent_info, 'Description': result[6]}

            payload.append(content)
            content = {}

    return jsonify(payload)

def select_orders():

    payload = []
    content = {}
    connection = connectDatabase(Application_HOST, Application_DATABASE, Application_USERNAME, Application_PASSWORD)

    with connection.cursor() as ordini:

        ordini.execute("SELECT * from ORDERS")
        sel_orders = ordini.fetchall()

        for result in sel_orders:
            agent_info = agentOrderByID(result[5], connection)
            cust_info = OrderByIDCustomer(result[4], connection)
            for res in cust_info:
                info = {'id': result[4], 'cust_name': res[1], 'cust_city': res[2], 'working_area': res[3],
                        'cust_country': res[4], 'grade': float(res[5]), 'opening_amt': "{:.2f}".format(float(res[6])),
                        'receive_amt': "{:.2f}".format(float(res[7])), 'payment_amt': "{:.2f}".format(float(res[8])),
                        'outstanding_amt': "{:.2f}".format(float(res[9])), 'phone_no': res[10], 'agent_code': res[11]}

            for res in agent_info:
                agent_info = {'agent_code': res[0], 'agent_name': res[1], "working_area": res[2],
                              "commission": "{:.2f}".format(float(res[3])), "phone_no": res[4], "country": res[5]}

            #num decimale, importOrder decimale advance_ord decimali
            content = {'num_ord': float(result[0]), 'importOrder': "{:.2f}".format(float(result[1])),
                       'advance_ord': "{:.2f}".format(float(result[2])), 'ordDate': result[3].strftime("%d/%m/%y"),
                       'Cust_id': info, 'Agent_code': agent_info, 'Description': result[6]}

            payload.append(content)
            content = {}

        closeCursor(ordini)

    closeConnection(connection)
    return payload

def select_orders_custumer(custId):

    payload = []
    content = {}
    connection = connectDatabase(Application_HOST, Application_DATABASE, Application_USERNAME, Application_PASSWORD)

    with connection.cursor() as cust_ord:

        cust_ord.execute("SELECT * from ORDERS WHERE cust_code = %s", (str(custId),))
        sel_orders = cust_ord.fetchall()

        for result in sel_orders:

            agent_info = agentOrderByID(result[5], connection)

            for res in agent_info:
                info = {'agent_code': res[0], 'agent_name': res[1], "working_area": res[2],
                        "commission": "{:.2f}".format(float(res[3])), "phone_no": res[4], "country": res[5]}

            #num decimale, importOrder decimale advance_ord decimali
            content = {'num_ord': float(result[0]), 'importOrder': "{:.2f}".format(float(result[1])),
                       'advance_ord': "{:.2f}".format(float(result[2])), 'ordDate': result[3].strftime("%d/%m/%y"),
                       'Agent_code': info, 'Description': result[6]}

            payload.append(content)
            content = {}

        closeCursor(cust_ord)

    closeConnection(connection)
    return payload

def select_orders_agent(agentId):

    payload = []
    content = {}
    connection = connectDatabase(Application_HOST, Application_DATABASE, Application_USERNAME, Application_PASSWORD)

    with connection.cursor() as ordini:

        ordini.execute("SELECT * from ORDERS WHERE agent_code = %s", (agentId,))
        sel_orders = ordini.fetchall()

        for result in sel_orders:

            cust_info = OrderByIDCustomer(result[4], connection)

            for res in cust_info:
                info = {'id': result[4], 'cust_name': res[1], 'cust_city': res[2], 'working_area': res[3],
                        'cust_country': res[4], 'grade': float(res[5]), 'opening_amt': "{:.2f}".format(float(res[6])),
                        'receive_amt': "{:.2f}".format(float(res[7])), 'payment_amt': "{:.2f}".format(float(res[8])),
                        'outstanding_amt': "{:.2f}".format(float(res[9])), 'phone_no': res[10], 'agent_code': res[11]}

            #num decimale, importOrder decimale advance_ord decimali
            content = {'num_ord': float(result[0]), 'importOrder': "{:.2f}".format(float(result[1])),
                       'advance_ord': "{:.2f}".format(float(result[2])), 'ordDate': result[3].strftime("%d/%m/%y"),
                       'Cust_id': info, 'Description': result[6]}

            payload.append(content)
            content = {}

        closeCursor(ordini)

    closeConnection(connection)
    return payload

def select_orderByID(ord_num):

    payload = []
    connection = connectDatabase(Application_HOST, Application_DATABASE, Application_USERNAME, Application_PASSWORD)

    with connection.cursor() as ord_id:

        ord_id.execute("SELECT * from ORDERS WHERE ord_num = %s", (str(ord_num),))
        sel_orders = ord_id.fetchall()

        for result in sel_orders:
            #num decimale, importOrder decimale advance_ord decimali
            content = {'num_ord': float(result[0]), 'importOrder': "{:.2f}".format(float(result[1])),
                       'advance_ord': "{:.2f}".format(float(result[2])), 'ordDate': result[3].strftime("%d/%m/%y"),
                       'Cust_id': result[4], 'Agent_code': result[5], 'Description': result[6]}

            payload.append(content)

        closeCursor(ord_id)

    closeConnection(connection)
    return payload

def insert_order(ord_num, import_order, order_amount, date_order, cust_id, agent_code, description):
    connection = psycopg2.connect(host=Application_HOST, database=Application_DATABASE, user=Application_USERNAME,
                                  password=Application_PASSWORD)
    with connection.cursor() as ord:
        ord.execute("SELECT * FROM ORDERS WHERE ord_num = %s", (str(ord_num),))
        if ord.rowcount == 0:
            ord.execute("INSERT INTO ORDERS VALUES(%s,%s,%s,%s,%s,%s,%s)",
                        (ord_num, import_order, order_amount, date_order, cust_id, agent_code, description))
            connection.commit()
        closeCursor(ord)
    closeConnection(connection)


def delete_order(ord_num):
    connection = psycopg2.connect(host=Application_HOST, database=Application_DATABASE, user=Application_USERNAME,
                                  password=Application_PASSWORD)
    with connection.cursor() as delete_ord:
        delete_ord.execute("DELETE FROM ORDERS WHERE ord_num=%s", (ord_num,))
        connection.commit()
        closeCursor(delete_ord)
    closeConnection(connection)


def update_order(ord_num, import_order, order_amount, date_order, cust_id, agent_code, description):
    connection = psycopg2.connect(host=Application_HOST, database=Application_DATABASE, user=Application_USERNAME,
                                  password=Application_PASSWORD)
    with connection.cursor() as update_ord:
        update_ord.execute(
            "UPDATE  ORDERS SET ord_amount =%s,advance_amount = %s,ord_date=%s,agent_code = %s,ord_description = %s WHERE ord_num=%s",
            (import_order, order_amount, date_order,agent_code, description,ord_num))
        connection.commit()
        closeCursor(update_ord)
    closeConnection(connection)


def agentInformation():
    connessione = psycopg2.connect(host=Application_HOST, database=Application_DATABASE, user=Application_USERNAME,
                                   password=Application_PASSWORD)
    with connessione.cursor() as agentInfo:
        agentInfo.execute("SELECT * from AGENTS ")
        infoAgent = agentInfo.fetchall()
        agentInfo.close()
    connessione.close()
    return infoAgent


def agentOrderByID(id_agent, connessione):
    with connessione.cursor() as agentInfo:
        agentInfo.execute("SELECT * from AGENTS WHERE agent_code = %s", (id_agent,))
        infoAgent = agentInfo.fetchall()
        agentInfo.close()
        return infoAgent


def customersInformation():
    connessione = psycopg2.connect(host=Application_HOST, database=Application_DATABASE, user=Application_USERNAME,
                                   password=Application_PASSWORD)
    with connessione.cursor() as custInfo:
        custInfo.execute("SELECT * from CUSTOMER ")
        infocust = custInfo.fetchall()
        connessione.close()
        return infocust


def OrderByIDCustomer(id_cust, connessione):
    with connessione.cursor() as agentInfo:
        agentInfo.execute("SELECT * from CUSTOMER WHERE cust_code = %s", (id_cust,))
        infoCustumer = agentInfo.fetchall()
        agentInfo.close()

    return infoCustumer