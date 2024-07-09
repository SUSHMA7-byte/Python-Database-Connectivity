from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = b'*123*'

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "Login"      #Mysql Workbench Login name
app.config["MYSQL_PASSWORD"] = "1234"   #Password (my pwd is in integer I should give it as string)
app.config["MYSQL_DB"] = "sush"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

#display the table results
@app.route('/')
def main():
    try:
        con = mysql.connection.cursor()
        sql = "SELECT * FROM StudentManagement"
        con.execute(sql)
        res = con.fetchall()
        con.close()
        return render_template("home.htm", datas=res)
    except Exception as e:
        return str(e)

#Add Student Details 
@app.route("/addUsers", methods=['GET', 'POST'])
def addUsers():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']
        try:
            con = mysql.connection.cursor()
            sql = "INSERT INTO StudentManagement(Name, Age, Course) VALUES (%s, %s, %s)"
            con.execute(sql, (name, age, course))
            mysql.connection.commit()
            con.close()
            flash('User Details Added', 'success')
            return redirect(url_for("main"))
        except Exception as e:
            flash(f'Failed to add user details: {str(e)}', 'error')
            return redirect(url_for("addUsers"))
    return render_template("addUsers.htm")

#Update/change the records of student details
@app.route("/editUsers/<string:id>", methods=['GET', 'POST'])
def editUsers(id):
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']
        try:
            con = mysql.connection.cursor()
            sql = "UPDATE StudentManagement SET Name=%s, Age=%s, Course=%s WHERE ID=%s"
            con.execute(sql, (name, age, course, id))
            mysql.connection.commit()
            con.close()
            flash('User Details Edited', 'success')
            return redirect(url_for("main"))
        except Exception as e:
            flash(f'Failed to edit user details: {str(e)}', 'error')
            return redirect(url_for("editUsers", id=id))
    else:
        try:
            con = mysql.connection.cursor()
            sql = "SELECT * FROM StudentManagement WHERE ID=%s"
            con.execute(sql, [id])
            res = con.fetchone()
            con.close()
            return render_template("editUsers.htm", datas=res)
        except Exception as e:
            flash(f'Failed to fetch user details: {str(e)}', 'error')
            return redirect(url_for("main"))

#Delete the unwanted records
@app.route("/deleteUsers/<string:id>", methods=['GET', 'POST'])
def deleteUsers(id):
    try:
        con = mysql.connection.cursor()
        sql = "DELETE FROM StudentManagement WHERE ID=%s"
        con.execute(sql, [id])
        mysql.connection.commit()
        con.close()
        flash('User Details Deleted', 'success')
        return redirect(url_for("main"))
    except Exception as e:
        flash(f'Failed to delete user details: {str(e)}', 'error')
        return redirect(url_for("main"))

if __name__ == '__main__':
    app.run(debug=True)
