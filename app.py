from flask import Flask, render_template, request, redirect, session, jsonify

from src.ManageDatabases.ApplicationDatabase import select_orders, select_orders_custumer, select_orders_agent, \
    insert_order, delete_order, agentInformation, customersInformation, select_orderByID, sort_orders, agentOrderByID
from src.ManageDatabases.userAdmin import username_password_confirm, role_user

app = Flask(__name__)


@app.route('/api/orders', methods=['GET'])
def orders():
    if session['role'] == 'DIRETTORE':
        orders = select_orders()
        return jsonify(orders)
    else:
        return render_template('index.html', error=None)


@app.route('/api/orders/agent/', methods=['GET'])
def agentOrders():
    id_agent = request.args.get("id_agent")
    return jsonify(select_orders_agent(id_agent))

@app.route('/api/orders/costumers',methods=['GET'])
def costumers_orders():
    print(select_orders_custumer('C00013'))
    id_custumer = request.args.get("cust_id")
    return jsonify(select_orders_custumer(id_custumer))


@app.route('/api/orders/sort_by/<param>')
def sort_order(param):
    if param in ['ord_num', 'ord_amount', 'advance_amount', 'ord_date', 'cust_code', 'agent_code',
                 'ord_description'] or param in ['-ord_num', '-ord_amount', '-advance_amount', '-ord_date',
                                                 '-cust_code', '-agent_code', '-ord_description']:
        return sort_orders(param)
    else:
        return render_template("index.html")


@app.route('/api/orders/dataorder', methods=['GET'])
def data_ord():
    ord_num = request.args.get("ord_num")
    return jsonify(select_orderByID(ord_num))


@app.route('/')
def index():
    return render_template('index.html', error=None)


@app.route('/login', methods=['POST', 'GET'])
def submit():
    username = request.form['username']
    password = request.form['password']

    if username_password_confirm(username, password):
        role = role_user(username, password)
        session['username'] = username
        session['role'] = role

        if role == "DIRETTORE":
            return render_template('ordersAgeMan.html')
        if role == "AGENTE":
            return render_template('orderAgent.html', username=username)
        if role == "CLIENTE":
            return render_template('ordersCustomer.html',username=username)
    else:
        error = 'Yes'
        return render_template("index.html", error=error)


@app.route('/insertOrder', methods=['POST'])
def insertOrder():
    function = 'Inserisci'
    if session['role'] == 'DIRETTORE':
        return render_template("order.html", function=function, customers=customersInformation(),
                               agents=agentInformation())
    if session['role'] == 'AGENTE':
        return render_template("order.html", function=function, customers=customersInformation())


@app.route('/changeOrder')
def changeOrder():
    ordNum = request.args.get("ordNum")
    function = 'Modifica'
    username= session['username']
    if session['role'] == 'DIRETTORE':

        return render_template("modify_order.html",username=username)
    if session['role'] == 'AGENTE':
        return render_template("modify_order.html",username=username)


@app.route('/update', methods=['POST'])
def update():
    ord_num = request.form['ord_num']
    ord_amount = request.form['ord_amount']
    advance_amount = request.form['advance_amount']
    ord_date = request.form['ord_date']
    cust_code = request.form['cust_code']
    agent_code = request.form['agent_code']
    ord_description = request.form['ord_description']
    return


@app.route('/logout')
def logout():
    return render_template("index.html")


@app.route('/insert', methods=['POST'])
def insert():
    ord_num = request.form['ord_num']
    ord_amount = request.form['ord_amount']
    advance_amount = request.form['advance_amount']
    ord_date = request.form['ord_date']
    cust_code = request.form['cust_code']
    agent_code = request.form['agent_code']
    ord_description = request.form['ord_description']
    username = session['username']
    if session['role'] == 'DIRETTORE':
        insert_order(ord_num, ord_amount, advance_amount, ord_date, cust_code, agent_code, ord_description)
        return render_template('ordersAgeMan.html')
    if session['role'] == 'AGENTE':
        insert_order(ord_num, ord_amount, advance_amount, ord_date, cust_code, agent_code, ord_description)
        return render_template('ordersAgeMan.html')


@app.route('/deleteOrder')
def delete():
    id_ord = request.args.get("ordNum")
    print(id_ord)
    username = session['username']
    if session['role'] == 'DIRETTORE':
        delete_order(id_ord)
        return render_template('ordersAgeMan.html', orders=select_orders(), ruolo=session['role'],
                               customerInfo=customersInformation(), agentInfo=agentInformation())
    if session['role'] == 'AGENTE':
        delete_order(id_ord)
        return render_template('ordersAgeMan.html', orders=select_orders_agent(username),
                               ruolo=session['role'], customerInfo=customersInformation())


if __name__ == '__main__':  # python interpreter assigns "__main__" to the file you run
    app.secret_key = 'super secret key'  # metti in un file di configurazione
    app.config['SESSION_TYPE'] = 'filesystem'  # metti su un file di configurazione
    app.run(debug=True)
