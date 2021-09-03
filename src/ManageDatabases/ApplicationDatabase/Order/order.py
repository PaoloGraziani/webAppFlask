from src.ManageDatabases.SettingDatabase import connectDatabase, Application_HOST, Application_DATABASE, \
    Application_USERNAME, Application_PASSWORD, closeCursor, closeConnection
from src.ManageDatabases.ApplicationDatabase.Agents.agents import agents
from src.ManageDatabases.ApplicationDatabase.Customer.customer import customer_list



def select_orderByID(ord_num, role,username):
    payload = []
    connection = connectDatabase(Application_HOST, Application_DATABASE, Application_USERNAME, Application_PASSWORD)

    with connection.cursor() as ord_id:
        ord_id.execute("SELECT * from ORDERS WHERE ord_num = %s", (str(ord_num),))
        sel_orders = ord_id.fetchall()
        list_agent= agents(connection)
        custumers = customer_list(role,connection)
        for result in sel_orders:

            content = {'username':username,'role': role, 'num_ord': float(result[0]), 'importOrder': "{:.2f}".format(float(result[1])),
                       'advance_ord': "{:.2f}".format(float(result[2])), 'ordDate': result[3].strftime("%Y-%m-%d"),
                       'Cust_id': result[4], 'Agent_code': result[5], 'Description': result[6],'agents':list_agent,'customers':custumers}

            payload.append(content)
        closeCursor(ord_id)
    closeConnection(connection)
    return payload


def insert_order(ord_num, import_order, order_amount, date_order, cust_id, agent_code, description):
    payload = []
    success = False
    if import_order < order_amount:
        success = False

    else:
        connection = connectDatabase(Application_HOST, Application_DATABASE, Application_USERNAME, Application_PASSWORD)
        with connection.cursor() as ord:
            ord.execute("SELECT * FROM ORDERS WHERE ord_num = %s", (str(ord_num),))

            if ord.rowcount == 0:
                ord.execute("INSERT INTO ORDERS VALUES(%s,%s,%s,%s,%s,%s,%s)",
                            (ord_num, import_order, order_amount, date_order, cust_id, agent_code, description))
                connection.commit()
                success = True
            else:
                success = "0"
            closeCursor(ord)
        closeConnection(connection)

    payload.append({'success': success})
    return payload


def delete_order(ord_num):
    try:
        connection = connectDatabase(Application_HOST, Application_DATABASE, Application_USERNAME, Application_PASSWORD)
        with connection.cursor() as delete_ord:
            delete_ord.execute("DELETE FROM ORDERS WHERE ord_num=%s", (ord_num,))
            connection.commit()
            payload = [{'success': 'True', 'message': 'Delete with Success'}]
            closeCursor(delete_ord)
        closeConnection(connection)
    except:
        payload = [{'success': 'False', 'message': 'Delete failed!'}]
    return payload


def update_order(ord_num, import_order, order_amount, date_order, cust_id, agent_code, description):
    payload =[]
    context = {}
    connection = connectDatabase(Application_HOST, Application_DATABASE, Application_USERNAME, Application_PASSWORD)
    with connection.cursor() as update_ord:
            update_ord.execute(
                "UPDATE  ORDERS SET ord_amount =%s,advance_amount = %s,ord_date=%s,cust_code=%s,agent_code = %s,ord_description = %s WHERE ord_num=%s",
                (import_order, order_amount, date_order, cust_id, agent_code, description, ord_num))

            connection.commit()
            closeCursor(update_ord)
    closeConnection(connection)
    context = {'success':True,'message': 'Modifica effettuata correttamente!'}
    payload.append(context)
    return payload
