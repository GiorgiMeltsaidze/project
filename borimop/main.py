from flask import Flask, render_template, request, session, redirect, url_for
from datetime import timedelta
import sqlite3

app = Flask(__name__)
app.secret_key = 'hello'
app.permanent_session_lifetime = timedelta(minutes=5)
tasks = []

@app.route('/home')
def home():
    return render_template('home.html', tasks=tasks)

@app.route('/')
def home1():
    return render_template('base.html', tasks=tasks)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.permanent = False
        user = request.form['user']
        session['user'] = user
        return redirect(url_for('user'))
    else:
        if 'user' in session:
            return redirect(url_for('user'))
        return render_template('login.html')



@app.route('/user')
def user():
    if 'user' in session:
        user = session['user']
        return render_template('home.html', username=user)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/user2')
def user1():
    if 'user' in session:
        user = session['user']
        return render_template('add_task.html', username=user)

@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.form['task']
    tasks.append(task)
    return redirect(url_for('home'))



@app.route("/enternew")
def enternew():
    return render_template("books.html")

@app.route("/addrec", methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            name = request.form['name']
            author = request.form['author']
            year = request.form['year']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO books (name, author, year) VALUES (?,?,?)",(name, author, year))

                con.commit()
                msg = "Record successfully added to database"
        except:
            con.rollback()
            msg = "Error in the INSERT"

        finally:
            con.close()
            return render_template('result.html',msg=msg)

@app.route('/list')
def list():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT rowid, * FROM books")

    rows = cur.fetchall()
    con.close()
    return render_template("list.html",rows=rows)

@app.route("/edit", methods=['POST','GET'])
def edit():
    if request.method == 'POST':
        try:
            id = request.form['id']
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT rowid, * FROM books WHERE rowid = " + id)

            rows = cur.fetchall()
        except:
            id=None
        finally:
            con.close()
            return render_template("edit.html",rows=rows)

@app.route("/editrec", methods=['POST','GET'])
def editrec():
    if request.method == 'POST':
        try:
            rowid = request.form['rowid']
            name = request.form['name']
            author = request.form['author']
            year = request.form['year']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE books SET name='"+name+"', author='"+author+"', year='"+year+"' WHERE rowid="+rowid)

                con.commit()
                msg = "Record successfully edited in the database"
        except:
            con.rollback()
            msg = "Error in the Edit: UPDATE students SET name="+name+", author="+author+", year="+year+"' WHERE rowid="+rowid+""

        finally:
            con.close()
            return render_template('result.html',msg=msg)

@app.route("/delete", methods=['POST','GET'])
def delete():
    if request.method == 'POST':
        try:
            rowid = request.form['id']
            with sqlite3.connect('database.db') as con:
                    cur = con.cursor()
                    cur.execute("DELETE FROM books WHERE rowid="+rowid)

                    con.commit()
                    msg = "Record successfully deleted from the database"
        except:
            con.rollback()
            msg = "Error in the DELETE"

        finally:
            con.close()
            return render_template('result.html',msg=msg)
if __name__ == '__main__':
    app.run(debug=True)