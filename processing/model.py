import sqlite3

class Model: 
    def __init__(self, link_db) -> None:
        self.conn = sqlite3.connect(link_db)
    
    def query(self, sql, all= True): 
        c= self.conn.cursor()
        c.execute(sql)
        self.conn.commit() 
        result = c.fetchall() if all else c.fetchone()
        return result
    def action(self, sql):
        # Update, Delete 
        c= self.conn.cursor()
        c.execute(sql)
        self.conn.commit()
    def __del__(self): 
        self.conn.close()

    
