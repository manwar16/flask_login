from flask import Flask, redirect , render_template, request, sessions, url_for
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager , UserMixin, login_required ,login_user, logout_user,current_user

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.db'
app.config['SECRET_KEY']='062124'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))




@login_manager.user_loader
def get(id):
    return User.query.get(id)

@app.route('/',methods=['GET'])
@login_required
def get_home():
    return render_template('home.html')

@app.route('/login',methods=['GET'])
def get_login():
    return render_template('login.html')


@app.route('/signup',methods=['GET'])
def get_signup():
    return render_template('signup.html')

@app.route('/login',methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    login_user(user)
    return redirect('/profile')

@app.route('/signup',methods=['POST'])
def signup_post():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    user = User(username=username,email=email,password=password)
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(email=email).first()
    login_user(user)
    return redirect('/')

@app.route('/logout',methods=['GET'])
def logout():
    logout_user()
    return redirect('/login')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', username=current_user.username, email=current_user.email, password=current_user.password)



if __name__=='__main__':
    app.run(debug=True)