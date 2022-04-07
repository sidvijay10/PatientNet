#!/usr/bin/env python

"""
Columbia's COMS W4111.003 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, url_for
import random
import string

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


# Database URI
DATABASEURI = "postgresql://ss6415:sv2637ss6415@35.211.155.104/proj1part2"
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#

#engine.execute("""CREATE TABLE IF NOT EXISTS test (
#  id serial,
#  name text
#);""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print ("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


@app.route('/')
def landing():
  return render_template("landing.html")


@app.route('/organization_register', methods=['GET', 'POST'])
def organization_register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            organization_name = request.form['organization_name']
            deposit = request.form['organization_balance']
            password = request.form['password']

            letter = string.ascii_lowercase
            random_id = ''.join(random.choice(letter) for i in range(24))
            print(random_id)

            engine.execute("INSERT INTO credentials(username, password, id, type) VALUES ('{}', '{}', '{}','organization')".format(username, password, random_id))
            engine.execute("INSERT INTO organization(organization_ID,organization_name,organization_balance) VALUES ('{}', '{}', '{}')".format(random_id,organization_name,deposit))
            engine.commit()
            return redirect("/login")

        except Exception as e:
            print(e)
            #engine.rollback()
            return render_template('organization_register.html', error='Servor Error')
    else:
        return render_template('organization_register.html')



@app.route('/hospital_register', methods=['GET', 'POST'])
def hospital_register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            hospital_name = request.form['hospital_name']
            hospital_city = request.form['hospital_city']
            hospital_address = request.form['hospital_address']
            deposit = request.form['hospital_balance']
            password = request.form['password']

            letter = string.ascii_lowercase
            random_id = ''.join(random.choice(letter) for i in range(24))
            print(random_id)

            engine.execute("INSERT INTO credentials(username, password, id, type) VALUES ('{}', '{}', '{}', 'hospital')".format(username, password, random_id))
            engine.execute("INSERT INTO hospital(hospital_ID,hospital_name,hospital_address,hospital_city,hospital_balance) VALUES ('{}', '{}', '{}', '{}', {})".format(random_id,hospital_name,hospital_address,hospital_city,deposit))
            engine.commit()
            return redirect("/login")

        except Exception as e:
            print(e)
            #engine.rollback()
            return render_template('hospital_register.html', error='Servor Error')
    else:
        return render_template('hospital_register.html')


@app.route('/researcher_register', methods=['GET', 'POST'])
def researcher_register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            organization = request.form['organization']
            deposit = request.form['deposit']
            password = request.form['password']

            exec1 = engine.execute("SELECT c.id FROM credentials c WHERE c.username='%s'" % (username,))
            if exec1.fetchone() is not None:
                return render_template('researcher_register.html', error='User Already Exists')


            exec = engine.execute("SELECT o.organization_ID FROM organization o WHERE o.organization_name='%s'" % (organization,))
            hosp_ID = exec.fetchone()[0]
            print(hosp_ID)
            letter = string.ascii_lowercase
            random_id = ''.join(random.choice(letter) for i in range(24))
            print(random_id)

            eng1 = engine.execute("INSERT INTO researcher(researcher_ID, researcher_Balance, organization_id) VALUES ('{}', '{}', '{}')".format(random_id, deposit, hosp_ID))
            eng2 = engine.execute("INSERT INTO credentials(username, password, id, type) VALUES ('{}', '{}', '{}', 'researcher')".format(username, password, random_id))
            #eng1.commit()
            #eng2.commit()
            return redirect("/login")

        except Exception as e:

            print(e)
            #engine.rollback()
            return render_template('researcher_register.html', error='Servor Error')
    else:
        return render_template('researcher_register.html')


@app.route('/patient_register', methods=['GET', 'POST'])
def patient_register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            insurance_provider = request.form['insurance_provider']
            insurance_provider_address = request.form['insurance_provider_address']
            hospital = request.form['hospital']
            race = request.form['race']
            age = request.form['age']
            blood_group = request.form['blood_group']
            height = request.form['height']
            weight = request.form['weight']
            current_city = request.form['current_city']
            gender = request.form['gender']
            password = request.form['password']

            exec = engine.execute("SELECT i.insurer_id FROM insurance_Provider i WHERE i.insurer_name='%s'" % (insurance_provider,))
            ins_ID = exec.fetchone()[0]
            print(ins_ID)
            exec2 = engine.execute("SELECT h.hospital_ID FROM hospital h WHERE h.hospital_name='%s'" % (hospital,))
            hosp_ID = exec.fetchone()[0]
            print(hosp_ID)
            letter = string.ascii_lowercase
            random_id = ''.join(random.choice(letter) for i in range(24))
            print(random_id)

            engine.execute("INSERT INTO credentials(username, password, id, type) VALUES ({}, '{}', '{}','patient')".format(username, password, random_id))
            #DOB might be problem
            engine.execute("INSERT INTO patient(patient_ID,date_of_birth,race,height,weight,gender,current_city,blood_group,patient_balance,hospital_ID,insurer_ID) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', 0, '{}', '{}')".format(random_id,age,race,height,weight,gender,current_city,blood_group,hosp_ID,ins_ID))
            engine.commit()
            return redirect("/login")

        except Exception as e:
            print(e)
            #engine.rollback()
            return render_template('patient_register.html', error='Servor Error')
    else:
        return render_template('patient_register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            exec = engine.execute("SELECT c.password FROM credentials c WHERE c.username='%s'" % (username,))
            actual_password = exec.fetchone()[0]
            print(actual_password)
            if actual_password == password:
                exec2 = engine.execute("SELECT c.type FROM credentials c WHERE c.username='%s'" % (username,))
                dashboard = exec2.fetchone()[0]
                print(dashboard)
                redirection = "/{}_dashboard".format(dashboard)
                return redirect(redirection)
            else:
                render_template('login.html', error='Incorrect Password')

        except Exception as e:
            print(e)
            #engine.rollback()
            return render_template('login.html', error='Servor Error')
    else:
        return render_template('login.html')


@app.route('/another')
def another():
  return render_template("another.html")

@app.route('/researcher_dashboard')
def researcher_dashboard():
  return render_template("researcher_dashboard.html")



# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
  return redirect('/')


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print ("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
