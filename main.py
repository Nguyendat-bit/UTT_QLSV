from flask import (
    Flask,
    request, 
    render_template, 
    url_for, 
    redirect, 
    session, 
)
from flask_session import Session 
from processing.login_processing import status_email, status_login 

app= Flask(__name__, template_folder= './templates', static_folder= './static')
app.config["SESSION_PERMANENT"]= False
app.config['SESSION_TYPE']= 'filesystem'

Session(app)

#main 
@app.route('/', methods= ['GET'])
def index():
    return redirect(url_for('dangnhap'))

# login
@app.route('/dangnhap', methods= ['GET', 'POST'])
def dangnhap():
    if request.method== 'POST': 
        user= request.form['email']
        password= request.form['password']
        if status_login(user, password) == 0: 
            return render_template('login/login.html', notify= 'Không đăng nhập được')
        else:
            # login thành công 
            session['name']= user
            return redirect('/')

    else: 
        return render_template('login/login.html', notify= None)

@app.route('/quenmatkhau', methods= ['GET', 'POST'])
def quenmatkhau():
    if request.method== 'POST': 
        email= request.form['email']
        if status_email(email):
            render_template('login/forgot-password.html', notify= 'Email không tồn tại !')
        else:
            # tìm đc email 
            return render_template('login/forgot-password.html', notify= None, title= 'Quenmatkhau')
    else:
        return render_template('login/forgot-password.html', notify= None, title= 'Quenmatkhau')

# 404 error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404/404.html')

if __name__== '__main__':
    app.run(port= 5501, debug= True)