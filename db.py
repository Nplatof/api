import mysql.connector
import hashlib
from flask import jsonify

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        mydb = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database
            )
        return mydb
    
    def readAll(self):
        conn = self.connect()
        cursor = conn.cursor()
        req = "SELECT * FROM etudiant"
        cursor.execute(req)
        #print(req)
        data = cursor.fetchall()
        conn.close()
        return data
    
    def readOne(self, id):
        conn = self.connect()
        cursor = conn.cursor()
        req = f"SELECT * FROM etudiant WHERE idetudiant ='{id}'"
        cursor.execute(req)
        #print(req)
        data = cursor.fetchone()
        conn.close()
        return data
    
    def create(self, nom, prenom, email, telephone):
        conn = self.connect()
        cursor = conn.cursor()
        req = f"INSERT INTO etudiant (nom, prenom, email, telephone) VALUES ('{nom}','{prenom}','{email}','{telephone}')"
        cursor.execute(req)
        #print(req)
        conn.commit()
        conn.close()

    def delete(self, id):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            req = f"DELETE FROM `etudiant` WHERE `idetudiant`='{id}'"
            cursor.execute(req)
            conn.commit()
            return cursor.rowcount  
        except mysql.connector.Error as err:
            conn.rollback()  
            return 0  
        finally:
            conn.close()  

    def update(self, nom, prenom, email, telephone, id):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            req = f"UPDATE `etudiant` SET `nom`= '{nom}',`prenom`= '{prenom}',`email`= '{email}',`telephone`= '{telephone}' WHERE idetudiant = '{id}'"
            cursor.execute(req)
            conn.commit()
            return cursor.rowcount  
        except mysql.connector.Error as err:
            conn.rollback()  
            return 0  
        finally:
            conn.close()  
    
    def authorized(self, request):
        auth = request.authorization
        username = auth.username
        password = auth.password
        conn = self.connect()
        cursor = conn.cursor()
        req = f"SELECT password FROM user WHERE login = '{username}'"
        #print(req)
        cursor.execute(req)
        data = cursor.fetchone()
        conn.close()
        if data and (data[0] == hashlib.sha256(password.encode('utf-8')).hexdigest()):
            return True
        else:
            return False
        
    def log(self, request):
        try:
            auth = request.authorization
            username = auth.username
            password = auth.password
        except:
            return 401
        try:
            conn = self.connect()
            curs = conn.cursor()
        except:
            return 500
        try:
            curs.execute(f"SELECT * FROM user WHERE login = '{username}' AND password = '{password}'")
            data = curs.fetchone()
            if data:
                return data
            else:
                return 401
        except:
            return(401)
        finally:
            conn.close()

    def has_no_spaces(input_string):
        return ' ' not in input_string
        