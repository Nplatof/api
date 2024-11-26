from flask import Flask, request, jsonify
import mysql.connector



mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="ciel2025"
)
cursor = mydb.cursor()

app = Flask(__name__)



@app.route('/v1/etudiants/', methods=['GET'])
def getEtudiants():
    etudiants = []
    request = "SELECT * FROM etudiant"
    cursor.execute(request)
    result = cursor.fetchall()
    for raw in result:
        etudiant = {
            "etudiant": raw[0],
            "nom": raw[1],
            "prenom": raw [2],
            "email": raw [3],
            "telephone": raw[4]
        }
        etudiants.append(etudiant)
    return jsonify(etudiants), 200



# Fetch a specific student (GET - retrieval still uses GET)
@app.route('/v1/etudiant/<int:id>', methods=['GET'])
def getEtudiant(id):
    request_query = f"SELECT * FROM etudiant WHERE idetudiant ='{id}'"
    cursor.execute(request_query)
    raw = cursor.fetchone()

    if raw:
        etudiant = {
            "etudiant": raw[0],
            "nom": raw[1],
            "prenom": raw[2],
            "email": raw[3],
            "telephone": raw[4]
        }
        return jsonify(etudiant),200
    else:
        return jsonify('Il n\'y a pas d\'élève avec cet id'),404
    


# Create new student (POST)
@app.route('/v1/etudiants/', methods=['POST'])
def createEtudiant():
    data = request.json
    nom = data['nom']
    prenom = data['prenom']
    email = data['email']
    telephone = data['telephone']

    # Insert query
    request_query = f"INSERT INTO etudiant (nom, prenom, email, telephone) VALUES ('{nom}','{prenom}','{email}','{telephone}')"
    

# Delete student
@app.route('/v1/etudiant/<int:id>', methods=['DELETE'])
def deleteEtudiant(id):
    request_query = f"DELETE FROM `etudiant` WHERE `idetudiant`='{id}'"
    cursor.execute(request_query)
    mydb.commit()

    if cursor.rowcount > 0:
        return jsonify({"message": "Étudiant supprimé avec succès"}), 200
    else:
        return jsonify({"message": "Étudiant Supprimé"}), 404



# Modify student
@app.route('/v1/etudiant/<int:id>', methods=['PUT'])
def updateEtudiant(id):
    data = request.json
    nom = data['nom']
    prenom = data['prenom']
    email = data['email']
    telephone = data['telephone']
    
    request_query = f"UPDATE `etudiant` SET `nom`= '{nom}',`prenom`= '{prenom}',`email`= '{email}',`telephone`= '{telephone}' WHERE idetudiant = '{id}'"
    
    cursor.execute(request_query)
    mydb.commit()

    if cursor.rowcount > 0:
        return jsonify({"message": "Étudiant mis à jour avec succès"}), 200
    else:
        return jsonify({"message": "Étudiant non trouvé"}), 404


if __name__ == '__main__':
    app.run(debug=True)