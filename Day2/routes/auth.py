from flask import Blueprint,render_template,request,redirect,session
from utils.auth import hash_password,check_password
from models.user import create_user,get_user

auth_bp = Blueprint('auth',__name__)

@auth_bp.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        create_user(
            request.form['name'],
            request.form['email'],
            hash_password(request.form['password']),
            request.form['role']
        )
        return redirect('/login')
    return render_template('register.html')

@auth_bp.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        user = get_user(request.form['email'])

        if user and check_password(user[3],request.form['password']):
            session['user']=user[0]
            session['role']=user[4]
            return redirect('/dashboard')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')