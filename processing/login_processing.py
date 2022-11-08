# Login 
# Forget password
from processing.model import Model
def infor_login(user, password):
    return Model('./database/qlsv.db').query(f"select * from taikhoan where username= '{user}' AND pass = '{password}'", all= False)

def status_email(email):
    return Model('./database/qlsv.db').query(f"select * from taikhoan where email= '{email}'", all= False)
    
def status_login(user, password):
    if infor_login(user, password): 
        return True
    else:
        return False 

