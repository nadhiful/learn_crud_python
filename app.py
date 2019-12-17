import mysql.connector
import json
from flask import Flask
from flask import request
from flask import redirect,url_for,flash
from flask import render_template
from mysql.connector import Error
from mysql.connector import errorcode

app = Flask(__name__)
app.secret_key = 'many random bytes'

conn = mysql.connector.connect(host='localhost', database='exam', user='root', password='')
cursor = conn.cursor()

@app.route('/')
def index():
    query = "SELECT * from kontak"
    cursor.execute(query)
    rv = cursor.fetchall()
    return render_template('index.html', contact=rv)

@app.route('/simpan', methods=['GET','POST'])
def simpan():
    if request.method == 'POST':
        flash("Data Inserted Successfully")
        nama = request.form['name']
        num_kontak = request.form['nomor'] 
        data = [nama,num_kontak]
        query = "INSERT INTO kontak(nama,num_kontak) VALUES(%s,%s)"
        cursor.execute(query,data)
        conn.commit()
    return redirect(url_for("index"))

@app.route('/update',methods=['GET','POST'])
def update():
    if request.method == 'POST':
        id_kontak = request.form['id_kontak']
        nama = request.form['name_update']
        num_kontak = request.form['nomor_update']
        data = [nama,num_kontak,id_kontak]
        query = "UPDATE kontak SET nama=%s, num_kontak=%s WHERE id_kontak=%s"
        cursor.execute(query,data)
        conn.commit()
        flash("Data Updated Successfully")
    return redirect(url_for("index"))

@app.route('/delete/<string:id_kontak>', methods=['GET'])
def delete(id_kontak):
    flash("Record Has Been Deleted Successfully")
    query = "DELETE FROM kontak WHERE id_kontak=%s"
    data = [id_kontak]
    cursor.execute(query,data)
    conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug = True)