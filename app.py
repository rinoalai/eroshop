from flask import Flask, render_template, request, redirect, url_for, session, flash

from data import *

app = Flask(__name__)
app.secret_key="123"

con=sqlite3.connect(db_path)
con.execute("create table if not exists user(pid integer primary key,username text,name text,email text,password text)")
con.close()

@app.route('/')
def home ():
    return render_template('home.html')

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        con=sqlite3.connect(db_path)
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("SELECT * FROM user WHERE username=? and password=?",(username,password))
        data=cur.fetchone()

        if data:
            session["username"]=data["username"]
            session["password"]=data["password"]
            return redirect("user")
        else:
            flash("Username and Password Mismatch","danger")
    return redirect(url_for("home"))

@app.route('/user',methods=["GET","POST"])
def user():
    return render_template('user.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        try:
            username=request.form['username']
            name=request.form['name']
            email=request.form['email']
            password=request.form['password']
            con=sqlite3.connect(db_path)
            cur=con.cursor()
            cur.execute("INSERT INTO user(username,name,email,password) values(?,?,?,?)",(username,name,email,password))
            con.commit()
            flash("Record Added Successfully","success")
        except:
            flash("Error in Insert Operation.","danger")
        finally:
            return redirect(url_for("home"))
            con.close()

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route('/index')
def index():
    return render_template('index.html')
            
@app.route('/erosstories/<story_type>')            
def erosstories(story_type):
    stories_list = read_stories_by_story_type(story_type)
    return render_template('erosstories.html',story_type=story_type, stories=stories_list)

@app.route('/erosstories/<int:story_number>')
def story(story_number):
    story = read_story_by_story_number(story_number)
    return render_template('story.html', story=story)

@app.route('/cstories')
def cstories():
    return render_template('cstories.html')

@app.route('/oghstories')
def oghstories():
    return render_template('oghstories.html')

@app.route('/upstories')
def upstories():
    return render_template('upstories.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/processing', methods=['post'])
def processing():
    story_data = {
        "story_type": request.form['story_type'],
        "title": request.form['story_title'],
        "genre": request.form['story_genre'],
        "status": request.form['story_status'],
        "description": request.form['story_desc'],
        "url": request.form['story_url']
    }
    insert_story(story_data)
    return redirect(url_for('erosstories', story_type=request.form['story_type']))

@app.route('/modify', methods=['post'])
def modify():
    if request.form["modify"] == "edit":
        story_number = request.form["story_number"] 
        story = read_story_by_story_number(story_number)
        return render_template('update.html', story=story)
    elif request.form["modify"] == "delete":
        story_number = request.form["story_number"]
        story = read_story_by_story_number(story_number)
        delete_story(story_number)
        return redirect(url_for("erosstories", story_type=story["story_kind"]))

@app.route('/update', methods=['post'])
def update():
    story_data = {
        "story_number" : request.form["story_number"],
        "story_type": request.form['story_type'],
        "title": request.form['story_title'],
        "genre": request.form['story_genre'],
        "status": request.form['story_status'],
        "description": request.form['story_desc'],
        "url": request.form['story_url']
    }
    update_story(story_data)
    return redirect(url_for('story',story_number = request.form['story_number']))
        
if __name__ == '__main__':
    app.run(debug=True)