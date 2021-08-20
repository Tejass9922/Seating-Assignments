from flask import Flask,render_template,url_for,redirect,request,session,jsonify,json

import csv 
import sys
app = Flask(__name__)
app.secret_key= "tejas_is_very_cool"

@app.route('/')
def home():
    session.clear()
    last_names = list(fetch_last_names())
    print(last_names)
    return render_template('login.html', last_names = json.dumps(last_names))

@app.route('/seating/success')
def success():
    if "table_number" in session and "user" in session:
        number = int(session["table_number"])
        name = str(session["user"])
        session.pop("user")
        session.pop("table_number")
        return render_template("homepage.html",first_name=name,table_number=number)
       #return 'welcome %s your table number is: %d' % (name,number)
    else:
       return redirect(url_for('home'))

@app.route('/seating/fail')
def failure():
    if "user" in session:
        name = str(session["user"])
        session.pop("user")
     #   return render_template("homepage.html")
        return render_template("altHomepage.html",first_name=name)
    else:
        return redirect(url_for('home'))

@app.route('/seating/chartView')
def chart_view():
    (headers,table_data) = fetch_table_format()
    return render_template("seatingAssignment.html",headers=headers,table_data=table_data)

@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        first = str(request.form['firstname'])
        last = str(request.form['lastname'])
        print((first,last))
        name = (first,last)
        table_number = find_table(name)
        session["user"] = first
        if table_number == -1:
            return redirect(url_for('failure'))

        session["table_number"] = (table_number)
        
        print(session["table_number"])
        return redirect(url_for('success'))
    else: 
        return render_template('login.html')
     
       

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
            return row[2]

    return -1

def fetch_table_format():
    csv_file = csv.reader(open('test.csv', "r"), delimiter=",")
    headers = ("First Name", "Last Name", "Table Number")
    data = []
    for row in csv_file:
        data.append([row[0],row[1],row[2]])
    
    return (headers,data)
      

if __name__ == '__main__':
  

    app.run(threaded=True,host='0.0.0.0') 