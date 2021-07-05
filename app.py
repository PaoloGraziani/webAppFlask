
from flask import Flask, render_template, request, redirect, session

from src.ManageDatabases.ApplicationDatabase import select_orders, select_orders_custumer, select_orders_agent, \
    insert_order, delete_order, agentInformation, customersInformation, select_orderByID
from src.ManageDatabases.userAdmin import username_password_confirm, role_user

app = Flask(__name__)

@app.route('/api/orders')
def orders():
    return select_orders()


@app.route('/')
def index():
    return render_template('index.html', error=None)


@app.route('/login', methods=['POST', 'GET'])
def submit():
    try:
        username = request.form['username']
        password = request.form['password']

        if username_password_confirm(username, password):
            role = role_user(username, password)
            session['username'] = username
            session['role']     = role

            if role == "DIRETTORE":
                return render_template('ordersAgeMan.html', orders=select_orders(), ruolo=role_user(username, password),
                                       customerInfo=customersInformation(), agentInfo=agentInformation())
            if role == "AGENTE":
                #loginData = {'username': username, 'password': password, 'ruolo': role_user(username, password)}
                return render_template('ordersAgeMan.html', orders=select_orders_agent(username),
                                       ruolo= role_user(username, password), customerInfo=customersInformation())
            if role == "CLIENTE":
                return render_template('ordersCustomer.html', orders=select_orders_custumer(username),
                                       ruolo=role_user(username, password), agentInfo=agentInformation())
        else:
            error = 'Yes'
            return render_template("index.html", error=error)
    except:
        return render_template("error.html")


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
    if session['role'] == 'DIRETTORE':
        return render_template("order.html", function=function, ord_data=select_orderByID(ordNum),
                               customers=customersInformation(), agents=agentInformation())
    if session['role'] == 'AGENTE':
        return render_template("order.html", function=function, ord_data=select_orderByID(ordNum),
                               customers=customersInformation())


@app.route('/update',methods=['POST'])
def update() :
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
        return render_template('ordersAgeMan.html', orders=select_orders(), ruolo=session['role'],
                               customerInfo=customersInformation(), agentInfo=agentInformation())
    if session['role'] == 'AGENTE':
        insert_order(ord_num, ord_amount, advance_amount, ord_date, cust_code, agent_code, ord_description)
        return render_template('ordersAgeMan.html', orders=select_orders_agent(username),
                               ruolo=session['role'], customerInfo=customersInformation())


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
    app.secret_key = 'super secret key' #metti in un file di configurazione
    app.config['SESSION_TYPE'] = 'filesystem' # metti su un file di configurazione
    app.run(debug=True)
