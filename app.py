from select import select
from sqlite3 import Cursor
from flask import Flask,render_template, request,redirect
import psycopg2

app = Flask(__name__)


def connection():
    host = 'localhost' 
    database = 'sql_demo' 
    user = 'postgres' 
    password = '12345'
    conn = psycopg2.connect(host=host, user=user, password=password, database=database)
    return conn



@app.route('/')
def list():
    cars =[]
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Cars")
    for row in cursor.fetchall():
        cars.append({"id": row[0], "name": row[1], "year": row[2], "price": row[3]})
    conn.close()
    return render_template("list.html", cars = cars)
    

@app.route('/create' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')

    if request.method=='POST':
        id=request.form['id']
        name=request.form['name']
        year=request.form['year']
        price=request.form['price']

        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Cars (id, name, year, price) VALUES (%s, %s, %s, %s)", (id, name, year, price))
        conn.commit()
        conn.close()
        return redirect('/')


@app.route('/update/<int:id>' , methods = ['GET','POST'])
def update(id):
    cars=[]
    conn = connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM Cars where id=%s",(str(id)))
        for row in cursor.fetchall():
            cars.append({"id": row[0], "name": row[1], "year": row[2], "price": row[3]})
        conn.close()
        return render_template("update.html",cars=cars[0])  

    if request.method=='POST':
        id=request.form['id']
        name=request.form['name']
        year=request.form['year']
        price=request.form['price']

       
        cursor.execute("update Cars set name=%s, year=%s, price=%s where id=%s",(name,year,price,id))
        conn.commit()
        conn.close()
        return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Cars WHERE id = %s", (str(id)))
    conn.commit()
    conn.close()
    return redirect('/')


@app.route('/datalist/<int:id>' , methods = ['GET','POST'])
def datalist(id):
    cars =[]
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Cars where id=%s",(str(id)))
    for row in cursor.fetchall():
        cars.append({"id": row[0], "name": row[1], "year": row[2], "price": row[3]})
    conn.close()
    return render_template("list.html", cars = cars)

if __name__ == '__main__':
    app.run(debug=True)