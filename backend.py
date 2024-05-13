from flask import Flask,render_template,url_for,redirect,request,session,jsonify,json

import csv 
import sys
app = Flask(__name__)
app.secret_key= "tejas_is_very_cool"
SHA_SECRET_KEY = 'b37e50cedcd3e3f1ff64f4afc0422084ae694253cf399326868e07a35f4a45fb'
@app.route('/'+ SHA_SECRET_KEY)
def home():
    session.clear()
    last_names = list(fetch_last_names())
    print(last_names)
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
       # print(data)
        return render_template('tableData.html',headers = headers, table_data = data,table_number=table, name =name)
    else:
        return redirect(url_for('home'))

@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        first = str(request.form['firstname'])
        last = str(request.form['lastname'])
        print((first,last))
        name = (first,last)
        (formatted_name,table_number,party_indicator) = find_table(name)
        session["user"] = first if formatted_name == 'FAIL_CASE' else formatted_name
        if table_number == -1:
            return redirect(url_for('failure'))

        session["table_number"] = (table_number)
        session["party_indicator"] = party_indicator
        print(session["table_number"])
        return redirect(url_for('success'))
    else: 
        return render_template('login.html')
     

def query_table_data(table_number):
    headers = ("First Name", "Last Name")
    csv_file = csv.reader(open('test.csv', "r"), delimiter=",")
    data = []
    for row in csv_file:
        if int(row[2]) == table_number:
            data.append([row[0],row[1]])
   # print(data)
    return (headers,data)

def query_party_assignment(party_identifier):
    headers = ("First Name", "Last Name", "Table Number")
    data = []
    csv_file = csv.reader(open('test.csv', "r"), delimiter=",")
    for row in csv_file:
        if int(row[3]) == party_identifier:
             data.append([row[0],row[1],row[2]])
    print("party identifier %d" % party_identifier)
    print(data)
    return (headers,data)


def fetch_last_names():
    csv_file = csv.reader(open('test.csv', "r"), delimiter=",")
    last_names = set()
    for row in csv_file:
         last_name = str(row[1])
         if not last_name in last_names:
             last_names.add(last_name)

    return last_names

def find_table(name):
    first = name[0].strip()
    last = name[1].strip()

    csv_file = csv.reader(open('test.csv', "r"), delimiter=",")

    for row in csv_file:  
        if row[0].lower() == first.lower() and row[1].lower() == last.lower():
            return (row[0],row[2],row[3])

    return ('FAIL_CASE',-1, -1)

def fetch_table_format():
    csv_file = csv.reader(open('test.csv', "r"), delimiter=",")
    headers = ("First Name", "Last Name", "Table Number")
    data = []
    for row in csv_file:
        data.append([row[0],row[1],row[2]])
    
    return (headers,data)
      

if __name__ == '__main__':
  

    app.run(threaded=True,host='0.0.0.0') 