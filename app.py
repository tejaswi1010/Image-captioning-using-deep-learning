import PIL
from flask import Flask, render_template, request
import sqlite3
import time 
import generator

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/sign")
def sign():
    return render_template("signup-in.html")

@app.route("/signup")
def signup():
    
    
    name = request.args.get('user','')
    password = request.args.get('pass','')
    password1 = request.args.get('pass1','')
    email = request.args.get('email','')
    number = request.args.get('num','')

    if password1 == password:
        con = sqlite3.connect('signup.db')
        cur = con.cursor()
        cur.execute("insert into `datas` (`name`, `password`,`password1`,`email`,`mobile`) VALUES (?, ?, ?, ?, ?)",(name,password,password1,email,number))
        con.commit()
        con.close()

        return render_template("signup-in.html")
    
    else:
        
        return render_template("signup-in.html")


@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('pass','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `name`, `password` from datas where `name` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signup-in.html")    

    elif mail1 == 'admin' and password1 == 'admin':
        return render_template("index.html")

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("index.html")
    else:
        return render_template("signup-in.html")

@app.route('/prediction',methods=["POST"])
def prediction():
    if request.method=="POST":
        f = request.files['userfile']
        path = 'static/{}'.format(f.filename)
        f.save(path)
        caption = generator.caption_image(path)
        result = {'image':path,'cap':caption}
    return render_template('index.html',your_caption = result)


if __name__== '__main__':
    app.run(debug=True)

