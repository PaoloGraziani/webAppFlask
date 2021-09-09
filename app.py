from flask import Flask, jsonify, render_template, request, session, redirect

from src.ManageDatabases.ApplicationDatabase.Agents.agents import select_orders_agent, agentInformation
from src.ManageDatabases.ApplicationDatabase.Customer.customer import select_orders_custumer, customersInformation, \
    customer_list
from src.ManageDatabases.ApplicationDatabase.Manager.manager import select_orders
from src.ManageDatabases.ApplicationDatabase.Order.order import select_orderByID, update_order, insert_order, \
    delete_order
from src.ManageDatabases.ApplicationDatabase.Order.sort import sort_orders
from src.ManageDatabases.AuthDatabase.userAdmin import username_password_confirm, role_user
from src.configuration import SECRET, SESSION_TYPE

app = Flask(__name__)

'''API RESTITUISCE TUTTI I CLIENTI'''


@app.route('/api/customers', methods=['GET'])
def customers():
    try:
        role = session['role']
        username = session['username']
        if role == 'DIRETTORE' or role == 'AGENTE':
            print(username)
            return jsonify(customer_list(username, None))
        else:
            return jsonify('[]')
    except:
        return jsonify('[]')


'''
API PER ORDINI DIRETTORE
'''


@app.route('/api/orders', methods=['GET'])
def orders():
    try:
        if session['role'] == 'DIRETTORE':
            orders = select_orders()
            return jsonify(orders)
        else:
            return jsonify('[]')
    except:
        return jsonify('[]')


'''
API PER ORDINI AGENTE
'''


@app.route('/api/orders/agent/', methods=['GET'])
def agentOrders():
  try:
    if session['role'] == 'AGENTE':
        id_agent = request.args.get("id_agent")
        return jsonify(select_orders_agent(id_agent))
    else:
        return jsonify('[]')
  except:
      return jsonify('[]')

'''
API PER ORDINI CLIENTE
'''


@app.route('/api/orders/costumers', methods=['GET'])
def costumers_orders():
    try:
        if session['role'] == 'CLIENTE':
            id_custumer = request.args.get("cust_id")
            return jsonify(select_orders_custumer(id_custumer))
        else:
            return jsonify('[]')
    except:
        return jsonify('[]')


'''
API RESTITUISCE IN OUTPUT GLI ORDINI CON UN CERTO ORDINE ASCENDENTE DISCENDENTE
'''


@app.route('/api/orders/sort_by/<param>')
def sort_order(param):
  try:
    if session['role'] == 'DIRETTORE' or session['role'] == 'AGENTE' or session['role'] == 'CLIENTE':
        ruolo = session['role']
        username = session['username']
        print(ruolo)
        if param in ['ord_num', 'ord_amount', 'advance_amount', 'ord_date', 'cust_code', 'agent_code',
                     'ord_description'] or param in ['-ord_num', '-ord_amount', '-advance_amount', '-ord_date',
                                                     '-cust_code', '-agent_code', '-ord_description']:
            return sort_orders(param, ruolo, username)
        else:
            return jsonify('[]')
  except:
      return  jsonify('[]')

'''
API RESTITUISCE I DATI DI UN ORDINE[USO IN MODIFICA)
'''


@app.route('/api/orders/dataorder', methods=['GET'])
def data_ord():
    try:
       if session['role'] == 'AGENTE' or session['role']=='DIRETTORE':
            ord_num = request.args.get("ordNum")
            return jsonify(select_orderByID(ord_num, session['role'], session['username']))
       else:
           return jsonify('[]')
    except:
        return jsonify('[]')


'''
API PER INSERIMENTO ORDINE
'''


@app.route('/api/insert', methods=['POST'])
def api_insert():
     try:
        if session['role'] == 'AGENTE':
            ord_num = request.form['ord_num']
            ord_amount = request.form['ord_amount']
            advance_amount = request.form['advance_amount']
            ord_date = request.form['ord_date']
            cust_code = request.form['cust_code']
            agent_code = request.form['agent_code']
            ord_description = request.form['ord_description']
            return jsonify(
                insert_order(ord_num, ord_amount, advance_amount, ord_date, cust_code, agent_code, ord_description))
        else:
            return jsonify('[]')
     except:
        return jsonify('[]')

'''
API PER ELIMINAZIONE DI UN ORDINE
'''
@app.route('/api/delete', methods=['GET'])
def api_delete():
    try:
        ord_num = request.args.get('ord_num')
        print(session['role'])
        if session['role'] == 'AGENTE':
            return jsonify(delete_order(ord_num))
        else:
            return jsonify('[]')
    except:
        return jsonify('[]')


'''
API PER LA MODIFICA DI UN ORDINE
'''


@app.route('/api/update', methods=['GET'])
def api_update():
   try:
        if session['role'] == 'AGENTE' or session['role'] == 'DIRETTORE':
            ord_num = request.args.get('ord_num')
            ord_amount = request.args.get('ord_amount')
            advance_amount = request.args.get('advance_amount')
            ord_date = request.args.get('ord_date')
            cust_code = request.args.get('cust_code')
            agent_code = request.args.get('agent_code')
            ord_description = request.args.get('ord_description')
            return jsonify(
                update_order(ord_num, ord_amount, advance_amount, ord_date, cust_code, agent_code, ord_description))
        else:
            return jsonify('[]')
   except:
       return jsonify('[]')


'''
FUNZIONE DI INIZIALIZZAZIONE DELL'APPLICAZIONE
'''


@app.route('/')
def index():
    return render_template('login.html', error=None)


'''
AUTENTICAZIONE
'''


@app.route('/login', methods=['POST'])
def submit():

    username = request.form['username']
    password = request.form['password']
    if username_password_confirm(username, password):
        role = role_user(username, password)
        session['username'] = username
        session['role'] = role

        if role == "DIRETTORE":
            return render_template('ordersManager.html', role=session['role'])
        if role == "AGENTE":
            return render_template('ordersAgent.html', username=username, role=role)
        if role == "CLIENTE":
            return render_template('ordersCustomer.html', username=username, role=role)
    else:
        error = 'Yes'
        return render_template("login.html", error=error)


'''
INSERIMENTO ORDINI INDIRIZZAMENTO
'''


@app.route('/insertOrder', methods=['POST'])
def insertOrder():
    return render_template("insertOrder.html", username=session['username'])


'''
INSERIMENTO ORDINE: FUNZIONE ESECUTIVA
'''


@app.route('/insert', methods=['POST'])
def insert():
    if session['role'] == 'AGENTE':
        ord_num = request.form['ord_num']
        ord_amount = request.form['ord_amount']
        advance_amount = request.form['advance_amount']
        ord_date = request.form['ord_date']
        cust_code = request.form['cust_code']
        agent_code = request.form['agent_code']
        ord_description = request.form['ord_description']
        username = session['username']
        infoCustomer = customersInformation()
        if float(ord_amount) < float(advance_amount):
            return render_template('insertOrder.html', error='yes', username=username, infoCustomer=infoCustomer)
        success = insert_order(ord_num, ord_amount, advance_amount, ord_date, cust_code, agent_code, ord_description)
        print(success)
        if success[0]['success'] == '0':
            return render_template('insertOrder.html', username=username, error='Ordine già presente!')
        else:
            return render_template('ordersAgent.html', username=username, role=session['role'])


'''
MODIFICA ORDINE - INDIRIZZAMENTO IN BASE AL RUOLO
'''


@app.route('/changeOrder')
def changeOrder():
    ordNum = request.args.get("ordNum")
    infoCustomer = customersInformation()
    infoAgent = agentInformation()

    if session['role'] == 'DIRETTORE':
        return render_template("modifyOrder.html", ordNum=ordNum, role=session['role'])
    if session['role'] == 'AGENTE':
        return render_template("modifyOrder.html", ordNum=ordNum, role=session['role'])


'''
FUNZIONE DI MODIFICA - PARTE ESECUTIVA
'''


@app.route('/update', methods=['POST'])
def update():
    ord_num = request.form['ord_num']
    ord_amount = request.form['ord_amount']
    advance_amount = request.form['advance_amount']
    ord_date = request.form['ord_date']
    cust_code = request.form['cust_code']
    agent_code = request.form['agent_code']
    ord_description = request.form['ord_description']
    username = session['username']

    if session['role'] == 'DIRETTORE':
        update_order(ord_num, ord_amount, advance_amount, ord_date, cust_code, agent_code, ord_description)

        return render_template('ordersManager.html', username=username, role=session['role'])
    elif session['role'] == 'AGENTE':
        update_order(ord_num, ord_amount, advance_amount, ord_date, cust_code, agent_code, ord_description)
        return render_template('ordersAgent.html', username=username, role=session['role'])


'''
ELIMINAZIONE DI UN ORDINE
'''


@app.route('/deleteOrder', methods=['GET'])
def delete():
    username = session['username']
    ord_num= request.args.get('ord_num')
    if session['role'] == 'AGENTE':
        delete_order(ord_num)
        return render_template('ordersAgent.html',
                               role=session['role'], username=username)


'''
LOGOUT
'''


@app.route('/logout')
def logout():
    session['role'] = None
    return redirect('/')


'''
INDIETRO
'''


@app.route('/back', methods=['POST'])
def back():
    role = session['role']
    username = session['username']
    print(role)
    if role == 'AGENTE':
        return render_template('ordersAgent.html', username=username, role=role)
    if role == 'DIRETTORE':
        return render_template('ordersManager.html', username=username, role=role)


if __name__ == '__main__':
    app.secret_key = SECRET()
    app.config['SESSION_TYPE'] = SESSION_TYPE
    app.run(debug=True)
