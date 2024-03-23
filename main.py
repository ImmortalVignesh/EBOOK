from flask import Flask, render_template, request, session,redirect,url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from config import Config



app = Flask(__name__)
app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ebook'

mysql = MySQL(app)



@app.route('/index')

def index():
 return render_template('index.html')
@app.route('/deletebooks/<string:id>', methods=['GET', 'POST'])
def deletebooks(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql="delete from books where id = %s"
    cursor.execute(sql,[id])
    cursor.execute("SELECT * FROM books")
    row = cursor.fetchall()
    mysql.connection.commit()
    cursor.close
    return  render_template('adminbook.html',row=row)
@app.route('/changebooks/<string:id>', methods=['GET', 'POST'])
def changebooks(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM books WHERE id = % s', (id,))


    if request.method == 'POST':
        isbn=request.form['isbn']
        title = request.form['title']
        author = request.form['author']
        des = request.form['des']
        price = request.form['price']
        pub=request.form['pub']
        pdf=request.form['pdf']
        sql = "update books set isbn=%s ,title=%s,author=%s ,des=%s,price=%s,pub=%s,pdf=%s where id =%s"
        cursor.execute(sql, [isbn, title, author, des,price,pub,pdf,id])
        mysql.connection.commit()
        cursor.execute("SELECT * FROM books")
        data = cursor.fetchall()

        cursor.close()

    return render_template('adminbook.html',row=data)


@app.route('/trans/<string:price>', methods=['GET', 'POST'])
def trans(price):
    msg=" "
    email=request.form['email']
    password = request.form['password']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM transtraction WHERE email = % s AND password = % s', (email, password,))
    account = cursor.fetchone()
    """cursor.execute("SELECT * FROM books")
    row = cursor.fetchall()"""

    if account:

        cost =int(price)
        bal =cursor.execute('SELECT amount from transtraction where email=% s',(email,))
        bal =int(bal)
        if (bal>cost):
            print("welcome")
            amt=bal-cost

            sql = "update transtraction set amount=%s where email =%s"
            cursor.execute(sql, [amt,email])
            mysql.connection.commit()

            cursor.close()
            msg = "paid successfully"
            return render_template('viewpage.html', msg=msg)

        else:
            msg="Amount greater than balance"
            return  render_template('viewpage.html',msg=msg)

    else:
        msg="Invalid username or password"
        return render_template('viewpage.html',msg=msg)

    return render_template('viewpage.html',row=row,msg=msg)

@app.route('/addbooks', methods=['GET', 'POST'])
def addbooks():
    return  render_template('addbooks.html')
@app.route('/admin_add', methods=['GET', 'POST'])
def admin_add():
    msg =''

    if request.method == 'POST' and 'isbn' in request.form and 'title' in request.form and 'author' in request.form   and 'des' in request.form and 'price' in request.form and 'pub' in request.form and 'pdf' in request.form:
        isbn = request.form['isbn']
        title = request.form['title']
        author  = request.form['author']

        des = request.form['des']
        price= request.form['price']
        pub = request.form['pub']
        pdf = request.form['pdf']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO books VALUES (%s,%s, %s, %s,%s ,%s,%s,%s)', (id,isbn , title , author, des, price, pub , pdf,))

        mysql.connection.commit()
        msg = 'uploaded successfully'
    return render_template('addbooks.html', msg=msg)

@app.route('/view',methods=['GET','POST'])
def view():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM books")
    data = cursor.fetchall()

    cursor.close()

    return render_template('viewpage.html', data=data)


@app.route('/viewbooks', methods=['GET', 'POST'])
def viewbooks():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM books")
    data = cursor.fetchall()
    cursor.close()
    return render_template('viewbooks.html', data=data)

@app.route('/viewusers', methods=['GET', 'POST'])
def viewusers():
    cursor= mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    cursor.close()
    return render_template('viewusers.html', data=data )

@app.route('/editprofile/<string:id>', methods=['GET', 'POST'])

def editprofile(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE email = % s', (id,))


    if request.method == 'POST' :
        msg=''

        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        passwordcon = request.form['passwordcon']
        sql = "update users set name=%s ,email=%s,password=%s ,phone=%s where id =%s"
        account=cursor.execute(sql, [name, email, password, phone,id])
        mysql.connection.commit()

        cursor.close()
        msg = 'You have successfully updated !'
        return render_template('view.html',msg=msg,account=account
                               )
    sql="select * from users where id = %s"
    cursor.execute(sql,[id])
    account = cursor.fetchone()
    return render_template("view.html",account = account)

"""
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif passwordcon != password:
            msg = 'Password Wrong'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        else:"""





"""


    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #cursor.execute('SELECT * FROM users WHERE email = % s AND password = % s', (email, password,))
    cursor.execute('SELECT * from users')
    data = cursor.fetchone()
    return render_template('editprofile.html',account=account)



   cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
   post=Post.query.filter(Post.slug==slug).first()

   if request.method=='POST':
       form= PostForm(formdata=request.form,obj=post)
       form.populate_obj(post)
       cursor.session.commit()
    return render_template('view.html',slug=post.slug)
"""
@app.route('/deleteaccount<string:id>', methods=['GET', 'POST'])
def deleteaccount(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql="delete  from users where id= %s";
    cursor.execute(sql,[id])
    mysql.connection.commit()
    cursor.close()
    return render_template('index.html')



@app.route('/editadmin<string:id>', methods=['GET', 'POST'])
def editadmin(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    account=cursor.execute('SELECT * FROM admin WHERE id = % s', (id,))
    if request.method == 'POST':
        msg = ''

        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        passwordcon = request.form['passwordcon']
        sql = "update admin set name=%s ,email=%s,password=%s ,phone=%s where id =%s"
        cursor.execute(sql, [name, email, password, phone, id])
        mysql.connection.commit()

        cursor.close()
        msg = 'You have successfully updated !'
        return render_template('adminview.html',msg=msg,account=account)
    sql = "select * from admin where id = %s"
    cursor.execute(sql, [id])
    account = cursor.fetchone()
    return render_template("adminview.html",account=account)

@app.route('/adminpage', methods=['GET', 'POST'])
def adminpage():
 return render_template('adminpage.html')
@app.route('/adminlogin', methods=['GET','POST'])
def adminlogin():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE email = % s AND password = % s', (email, password,))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['email'] = account['email']
            session['password'] = account['password']
            msg = 'Logged in successfully !'


            return render_template('adminview.html', account=account,msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('admin.html', msg=msg)
@app.route('/adminsignout',methods=['GET','POST'])
def adminsignout():
    session['loggedin']=False
    return render_template('index.html')
@app.route('/viewpage',methods=['GET','POST'])
def viewpage():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM books")
    data = cursor.fetchall()

    cursor.close()

    return render_template('viewpage.html', data=data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = % s AND password = % s', (email, password,))
        account = cursor.fetchone()

        #print(account)
        #print(account['id'])

        if account:
            session['loggedin'] = True
            session['myvar']=account
            session['email'] = account['email']
            session['password'] = account['password']
            msg = 'Logged in successfully !'




            return render_template('view.html',account=account)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)
@app.route('/download/<string:id>',methods=['GET','POST'])
def download(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql="select pdf from student where id =%s";


    return

@app.route('/adminbook',methods=['GET','POST'])
def adminbook():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM books")
    data = cursor.fetchall()

    cursor.close()

    return render_template('adminbook.html', data=data)


@app.route('/registration',methods=['GET','POST'])

def registration():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form and 'phone' in request.form and 'photo' in request.form  and 'passwordcon' in request.form:


        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        photo = request.form['photo']
        passwordcon = request.form['passwordcon']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = % s', (id,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif len(phone)!=10:
            msg='your mobile number is invalid'" "
        elif passwordcon != password:
            msg='Password Wrong'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'Username must contain only characters and numbers !'
        elif not name or not password or not email or  not phone :
            msg = 'Please fill out the form !'
        else:

            cursor.execute('INSERT INTO users VALUES (%s,%s, % s, % s, % s ,% s)', (id,name,email, password, phone , photo,))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('registration.html', msg=msg)

@app.route('/home')
def home():
    return  render_template('home.html')
@app.route('/admin')
def admin():
    return render_template('admin.html')
"""@app.route('/login_validation', methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    return "The email is {} ant the password is {}".format(email , password)


@app.route('/dispaly',methods=['POST','GET'])
def dispaly():


    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM books")
    data= cursor.fetchall()

    return render_template("adminpage.html",data=data)"""

if __name__ == '__main__':
    app.run(port=5000, debug=True)
