import psycopg2
from flask import jsonify

from src.ManageDatabases.SettingDatabase import Application_HOST, Application_DATABASE, Application_USERNAME, \
    Application_PASSWORD, closeCursor, connectDatabase, closeConnection


def select_orders():
    payload = []
    content = {}
    connection = connectDatabase(Application_HOST, Application_DATABASE, Application_USERNAME, Application_PASSWORD)
    with connection.cursor() as ordini:
        ordini.execute("SELECT * from ORDERS")
        sel_orders = ordini.fetchall()

        for result in sel_orders:
            cust_info = custumersInformation(result[4])
            for res in cust_info:
                info = {'id': result[4], 'cust_name': res[1], 'cust_city': res[2], 'working_area': res[3],
                        'cust_country': res[4], 'grade': res[5], 'opening_amt': res[6], 'receive_amt': res[7],
                        'payment_amt': res[8], 'outstanding_amt': res[9], 'phone_no': res[10], 'agent_code': res[11]}

            content = {'num_ord': result[0], 'importOrder': result[1], 'advance_ord': result[2], 'ordDate': result[3],
                       'Cust_id':
                           info
                , 'Agent_code': result[5], 'Description': result[6]}
            payload.append(content)
            content = {}
        closeCursor(ordini)
    closeConnection(connection)
    return jsonify(payload)


def select_orders_custumer(custId):
    connection = connectDatabase(Application_HOST, Application_DATABASE, Application_USERNAME, Application_PASSWORD)
    with connection.cursor() as cust_ord:
        cust_ord.execute("SELECT * from ORDERS WHERE cust_code = %s", (str(custId),))
        sel_orders = cust_ord.fetchall()
        closeCursor(cust_ord)
    closeConnection(connection)
    return sel_orders


def select_orders_agent(agentId):
    connection = connectDatabase(Application_HOST, Application_DATABASE, Application_USERNAME, Application_PASSWORD)
    with connection.cursor() as agent_ord:
        agent_ord.execute("SELECT * from ORDERS WHERE agent_code = %s", (str(agentId),))
        sel_orders = agent_ord.fetchall()
        closeCursor(agent_ord)
    closeConnection(connection)
    return sel_orders


def select_orderByID(ord_num):
    connection = connectDatabase(Application_HOST, Application_DATABASE, Application_USERNAME, Application_PASSWORD)
    with connection.cursor() as ord_id:
        ord_id.execute("SELECT * from ORDERS WHERE ord_num = %s", (str(ord_num),))
        sel_orders = ord_id.fetchall()
        closeCursor(ord_id)
    closeConnection(connection)
    return sel_orders


def insert_order(ord_num, import_order, order_amount, date_order, cust_id, agent_code, description):
    connection = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="postgres")
    with connection.cursor() as ord:
        ord.execute("SELECT * FROM ORDERS WHERE ord_num = %s", (str(ord_num),))
        if ord.rowcount == 0:
            ord.execute("INSERT INTO ORDERS VALUES(%s,%s,%s,%s,%s,%s,%s)",
                        (ord_num, import_order, order_amount, date_order, cust_id, agent_code, description))
            connection.commit()
        closeCursor(ord)
    closeConnection(connection)


def delete_order(ord_num):
    connection = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="postgres")
    with connection.cursor() as delete_ord:
        delete_ord.execute("DELETE FROM ORDERS WHERE ord_num=%s", (ord_num,))
        connection.commit()
        closeCursor(delete_ord)
    closeConnection(connection)


def update_order(ord_num, import_order, order_amount, date_order, cust_id, agent_code, description):
    connection = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="postgres")
    with connection.cursor() as update_ord:
        update_ord.execute(
            "UPDATE INTO ORDERS SET ord_num = ? SET ord_amount = ? SET advance_amount = ? SET ord_date=? SET agent_code = ? SET ord_description = ? ",
            (ord_num, import_order, order_amount, date_order, cust_id, agent_code, description))
        connection.commit()
        ord.close()
    closeConnection(connection)


def agentInformation():
    connessione = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="postgres")
    with connessione.cursor() as agentInfo:
        agentInfo.execute("SELECT * from AGENTS ")
        infoAgent = agentInfo.fetchall()
        agentInfo.close()
    connessione.close()
    return infoAgent


def agentInformation(id_agent):
    connessione = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="postgres")
    with connessione.cursor() as agentInfo:
        agentInfo.execute("SELECT * from AGENTS WHERE agent_code = %s", id_agent)
        infoAgent = agentInfo.fetchall()
        agentInfo.close()
    connessione.close()
    return infoAgent


def costumersInformation():
    connessione = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="postgres")
    with connessione.cursor() as custInfo:
        custInfo.execute("SELECT * from CUSTOMER ")
        infocust = custInfo.fetchall()
        connessione.close()
        return infocust


def custumersInformation(id_cust):
    connessione = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="postgres")
    with connessione.cursor() as agentInfo:
        agentInfo.execute("SELECT * from CUSTOMER WHERE cust_code = %s", (id_cust,))
        infoCustumer = agentInfo.fetchall()
        agentInfo.close()
    connessione.close()
    return infoCustumer
