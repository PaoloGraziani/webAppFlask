import psycopg2

from src.ManageDatabases.settingDatabase  import connectDatabase, Application_HOST, Application_DATABASE, \
    Application_USERNAME, Application_PASSWORD, closeCursor, closeConnection

def agents(connection):
    payload = []
    content = {}
    with connection.cursor() as cust_ord:
        cust_ord.execute("SELECT agent_code from AGENTS ")
        sel_orders = cust_ord.fetchall()
        content = {'agent_code': sel_orders}
        payload.append(content)
        closeCursor(cust_ord)
    return payload


def select_orders_agent(agentId):
    from src.ManageDatabases.ApplicationDatabase.Customer.customer import OrderByIDCustomer
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

            # num decimale, importOrder decimale advance_ord decimali
            content = {'num_ord': float(result[0]), 'importOrder': "{:.2f}".format(float(result[1])),
                       'advance_ord': "{:.2f}".format(float(result[2])), 'ordDate': result[3].strftime("%d/%m/%y"),
                       'Cust_id': info, 'Description': result[6]}

            payload.append(content)
            content = {}

        closeCursor(ordini)

    closeConnection(connection)
    return payload


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
