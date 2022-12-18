from flask import (
    Flask,
    request, 
    render_template, 
    url_for, 
    redirect, 
    session,
    flash 
)
from flask_session import Session 
from processing.login_processing import status_email, status_login 
from processing.model import Model

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
            print('Thành công')
            session['name']= user
            return redirect('/qlsv')

    else: 
        return render_template('login/login.html', notify= None)

# dang xuat 
@app.route('/logout')
def dangxuat(): 
    session.pop('name')
    return redirect('/')

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

# QLSV 
@app.route('/qlsv', methods= ['GET'])
def qlsv():
    # list_sv= Model('./database/qlsv.db').query("select * from sinhvien")
    # list_sv id, hoten, lop, khoa, diachi , tuoi, gpa,
    # flash('Đăng nhập thành công')
    list_sv= Model('./database/qlsv.db').query('select * from sinhvien;', all= True)
    
    return render_template('qlsv/qlsv_table.html', list_sv= list_sv, title= 'QLSV', username= session['name'])

@app.route('/deleteqlsv/<int:id>')
def delete_qlsv(id):
    try:
        Model('./database/qlsv.db').action(f"delete from sinhvien where id= '{id}'")
        
        flash('Xoá thành công')
        return redirect(url_for('qlsv'))
    except:
        
        flash('Không xoá được')
        return redirect(url_for('qlsv'))

@app.route('/updatesqlsv/<int:id>', methods= ['GET','POST'])
def update_qlsv(id):
    if request.method== 'POST': 
        hovaten= request.form['username']
        age= request.form['email']
        lop= request.form['first_name']
        diachi= request.form['last_name']

        try: 
            Model('./database/qlsv.db').action(f"update sinhvien set hoten= '{hovaten}', lop= '{lop}', tuoi= '{age}', diachi= '{diachi}' where id = '{id}'; ")
            flash('Cập nhật thành công')
            return redirect(url_for('qlsv'))
        except:
            flash('Cập nhật không thành công')
            return redirect(url_for('qlsv'))
    else:
        sinhvien= Model('./database/qlsv.db').query(f"select * from sinhvien where id = '{id}';", all= False)
        return render_template('qlsv/qlsv_update.html',title= 'QLSV', hoten= sinhvien[1],
                age= sinhvien[5], lop= sinhvien[2], diachi= sinhvien[4],  username= session['name'])

@app.route('/addqlsv', methods=['GET', 'POST'])
def add_qlsv():
    if request.method== 'POST': 
        hovaten= request.form['username']
        age= request.form['email']
        lop= request.form['first_name']
        diachi= request.form['last_name']

        id = str(hash(hovaten + age + lop + diachi))[:3]
        
        try: 
            Model('./database/qlsv.db').action(f"insert into sinhvien values('{id}', '{hovaten}', '{lop}', 'CNTT', '{age}', '{diachi}', ''); ")
            flash('Thêm thành công' )
            list_sv= Model('./database/qlsv.db').query('select * from sinhvien;', all= True)
            return render_template('qlsv/qlsv_table.html', list_sv= list_sv, title= 'QLSV')
        except:
            flash('Thêm không thành công')
            list_sv= Model('./database/qlsv.db').query('select * from sinhvien;', all= True)
            return render_template('qlsv/qlsv_table.html', list_sv= list_sv, title= 'QLSV', username= session['name'])
    else:
        
        sinhvien= ['Nguyễn Văn A', '21', '70DCTT24','Hà Nội']

        return render_template('qlsv/qlsv_update.html',title= 'QLSV', hoten= sinhvien[0],
                age= sinhvien[1], lop= sinhvien[2], diachi= sinhvien[3])

if __name__== '__main__':
    app.run(port= 5502, debug= True)