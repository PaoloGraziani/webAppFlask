import src.ManageDatabases.ApplicationDatabase.Agents.agents
from src.ManageDatabases.settingDatabase import connectDatabase, Application_HOST, Application_DATABASE, \
    Application_USERNAME, Application_PASSWORD, closeCursor, closeConnection

def customer_list(role,connection):
    payload = []
    content = {}
    print(connection)
    if connection == None:
        connessione = connectDatabase(Application_HOST, Application_DATABASE, Application_USERNAME, Application_PASSWORD)
    else:
        connessione = connection
    with connessione.cursor() as cust_ord:

        cust_ord.execute("SELECT cust_code from CUSTOMER ")
        sel_orders = cust_ord.fetchall()
        content = {'role':role,'cust_code':sel_orders}
        payload.append(content)
        closeCursor(cust_ord)
    closeConnection(connessione)
    return payload

def select_orders_custumer(custId):
    payload = []
    content = {}
    connessione = connectDatabase(Application_HOST, Application_DATABASE, Application_USERNAME, Application_PASSWORD)

    with connessione.cursor() as cust_ord:

        cust_ord.execute("SELECT * from ORDERS WHERE cust_code = %s", (str(custId),))
        sel_orders = cust_ord.fetchall()

        for result in sel_orders:
            from src.ManageDatabases.ApplicationDatabase.Agents.agents import agentOrderByID
            agent_info =agentOrderByID(result[5], connessione)

            for res in agent_info:
                info = {'agent_code': res[0], 'agent_name': res[1], "working_area": res[2],
                        "commission": "{:.2f}".format(float(res[3])), "phone_no": res[4], "country": res[5]}

            # num decimale, importOrder decimale advance_ord decimali
            content = {'num_ord': float(result[0]), 'importOrder': "{:.2f}".format(float(result[1])),
                       'advance_ord': "{:.2f}".format(float(result[2])), 'ordDate': result[3].strftime("%d/%m/%y"),
                       'Agent_code': info, 'Description': result[6]}

            payload.append(content)
            content = {}

        closeCursor(cust_ord)

    closeConnection(connessione)
    return payload

def customersInformation():
    connessione = connectDatabase(Application_HOST, Application_DATABASE, Application_USERNAME, Application_PASSWORD)
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