from flask import Flask,render_template,url_for,redirect,request,session,jsonify,json
import k_closest
import csv 
import sys
app = Flask(__name__)
app.secret_key= "tejas_is_very_cool"
SHA_SECRET_KEY = 'b37e50cedcd3e3f1ff64f4afc0422084ae694253cf399326868e07a35f4a45fb'
guest_list = "Medha_Sangeeth_Guest_List_Tejas_Updated_V5.csv"
@app.route('/'+ SHA_SECRET_KEY)
def home():
    session.clear()
    last_names = list(fetch_last_names())
    return render_template('login.html', last_names = json.dumps(last_names))

@app.route('/seating/success/' + SHA_SECRET_KEY)
def success():
    if "table_number" in session and "user" in session:
        number = int(session["table_number"])
        name = str(session["user"])
        party_indicator = int(session['party_indicator'])
        return render_template("homepage.html",first_name=name,table_number=number,party_indicator=party_indicator)
     
    else:
       return redirect(url_for('home'))

@app.route('/seating/approximate/' + SHA_SECRET_KEY)
def list_approx_users():
    if "approx_users" in session:
        headers = ("First Name", "Last Name", "Table Number")
        users = session['approx_users']
        session.pop('approx_users')
        return render_template("potentialUsers.html", headers = headers, table_data = users )
    else:
        return redirect(url_for('home'))

@app.route('/seating/fail/' + SHA_SECRET_KEY)
def failure():
    if "user" in session:
        name = str(session["user"])
        session.pop("user")
        return render_template("altHomepage.html",first_name=name)
    else:
        return redirect(url_for('home'))

@app.route('/seating/chartView/' + SHA_SECRET_KEY)
def chart_view():
        (headers,table_data) = fetch_table_format()
        return render_template("seatingAssignment.html",headers=headers,table_data=table_data)
   

@app.route('/seating/partyInfo/' + SHA_SECRET_KEY,methods = ['POST', 'GET'])
def party_info():
    if request.method == 'POST':
        party_indicator = int(request.form['partyIndicator'])
        name = str(request.form['name'])
        (headers,data) = query_party_assignment(party_indicator)
        return render_template('partyData.html',headers=headers,party_data=data,name=name)

@app.route('/seating/tableInfo/' + SHA_SECRET_KEY,methods = ['POST', 'GET'])
def table_info():
    if request.method == 'POST':
        table =  int(request.form['tableNumber'])
        name = str(request.form['name'])
        (headers,data) = query_table_data(table)
        return render_template('tableData.html',headers = headers, table_data = data,table_number=table, name =name)
    else:
        return redirect(url_for('home'))

@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        first = str(request.form['firstname'])
        last = str(request.form['lastname'])
        name = (first,last)
        (formatted_name,table_number,party_indicator) = find_table(name)
        approximate_users = []
        if formatted_name == "FAIL_CASE":
            approximate_users = find_approximate_users(first,last)
        
        if len(approximate_users) == 0:
            session["user"] = first if formatted_name == 'FAIL_CASE' else formatted_name
            if table_number == -1:
                return redirect(url_for('failure'))

            session["table_number"] = (table_number)
            session["party_indicator"] = party_indicator
            return redirect(url_for('success'))
        else:
            session['approx_users'] = list(approximate_users)
            return redirect(url_for('list_approx_users'))
    else: 
        return render_template('login.html')
     

def find_approximate_users(first_name, last_name):
    approx_users = set()
    if len(first_name) == 0 and len(last_name) == 0:
        return approx_users
    csv_file = csv.reader(open(guest_list, "r"), delimiter=",")
    for row in csv_file: 
        if first_name.strip() == '':
            if (row[0].lower() == last_name.lower() or row[1].lower() == last_name.lower()):
                approx_users.add((row[0], row[1], row[2])) 
        elif last_name.strip() == '':
            if (row[0].lower() == first_name.lower() or row[1].lower() == first_name.lower()):
                approx_users.add((row[0], row[1], row[2])) 
        elif (row[0].lower() == first_name.lower() or row[0].lower() == last_name.lower() or row[1].lower() == last_name.lower() or row[1].lower() == first_name.lower()):
            approx_users.add((row[0], row[1], row[2])) 
    
    last_names = fetch_last_names_2()
    first_names = fetch_first_names()

    k_closest_neighbors_v1 = []
    k_closest_neighbors_v2 = []
    k_closest_neighbors_v3 = []
    k_closest_neighbors_v4 = []
    
    if len(last_name) > 0:
        k_closest_neighbors_v1 = k_closest.find_close_words(last_names,last_name,4,2)
        k_closest_neighbors_v4 = k_closest.find_close_words(first_names,last_name,3,1)
    if len(first_name) > 0:
        k_closest_neighbors_v2 = k_closest.find_close_words(first_names,first_name,4,2)
        k_closest_neighbors_v3 = k_closest.find_close_words(last_names,first_name,3,1)

   
    k_closest_neighbors = set()
    if len(k_closest_neighbors_v1) > 0:
        k_closest_neighbors.update(k_closest_neighbors_v1)
    if len(k_closest_neighbors_v2) > 0:
        k_closest_neighbors.update(k_closest_neighbors_v2)
    if len(k_closest_neighbors_v3) > 0:
        k_closest_neighbors.update(k_closest_neighbors_v3) 
    if len(k_closest_neighbors_v4) > 0:
        k_closest_neighbors.update(k_closest_neighbors_v4)

    if '' in k_closest_neighbors:
        k_closest_neighbors.remove('')
    print(k_closest_neighbors)
    csv_file = csv.reader(open(guest_list, "r"), delimiter=",")
    for row in csv_file:
        if row[0].lower() in k_closest_neighbors or row[1].lower() in k_closest_neighbors:
            user = (row[0], row[1], row[2])
            if not user in approx_users:
                approx_users.add(user) 
    return approx_users


def query_table_data(table_number):
    headers = ("First Name", "Last Name")
    csv_file = csv.reader(open(guest_list, "r"), delimiter=",")
    data = []
    for row in csv_file:
        if int(row[2]) == table_number:
            data.append([row[0],row[1]])
    return (headers,data)

def query_party_assignment(party_identifier):
    headers = ("First Name", "Last Name", "Table Number")
    data = []
    csv_file = csv.reader(open(guest_list, "r"), delimiter=",")
    for row in csv_file:
        if int(row[3]) == party_identifier:
             data.append([row[0],row[1],row[2]])
    return (headers,data)


def fetch_last_names():
    csv_file = csv.reader(open(guest_list, "r"), delimiter=",")
    last_names = set()
    for row in csv_file:
         last_name = str(row[1].strip())
         if not last_name in last_names:
             last_names.add(last_name)
    return last_names

def fetch_last_names_2():
    csv_file = csv.reader(open(guest_list, "r"), delimiter=",")
    last_names = set()
    for row in csv_file:
         last_name = str(row[1]).lower().strip()
         if not last_name in last_names:
             last_names.add(last_name)

    return last_names

def fetch_first_names():
    csv_file = csv.reader(open(guest_list, "r"), delimiter=",")
    first_names = set()
    for row in csv_file:
         first_name = str(row[0])
         if not first_name in first_names:
             first_names.add(first_name)

    return first_names

def find_table(name):
    first = name[0].strip()
    last = name[1].strip()

    csv_file = csv.reader(open(guest_list, "r"), delimiter=",")
    for row in csv_file:  
        if row[0].lower() == first.lower() and row[1].lower() == last.lower():
            return (row[0],row[2],row[3])
    return ('FAIL_CASE',-1, -1)

def fetch_table_format():
    csv_file = csv.reader(open(guest_list, "r"), delimiter=",")
    headers = ("First Name", "Last Name", "Table Number")
    data = []
    for row in csv_file:
        data.append([row[0],row[1],row[2]])
    
    return (headers,data)

if __name__ == '__main__':
    app.run(threaded=True,host='0.0.0.0') 