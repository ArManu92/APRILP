from flask import Flask, request, jsonify
import sqlite3
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)

@app.route('/')
def home():
    return "¡Hola! La aplicación Flask está funcionando."

# Función para conectar a la base de datos
def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'Aprilp.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Ruta para iniciar sesión
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Usuarios WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        access_token = create_access_token(identity={'username': username, 'is_superuser': user['is_superuser']})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'msg': 'Usuario o contraseña incorrectos'}), 401

# Ruta para registrar un nuevo usuario
@app.route('/register', methods=['POST'])
@jwt_required()
def register():
    current_user = get_jwt_identity()
    if not current_user['is_superuser']:
        return jsonify({'msg': 'No tienes permisos para registrar usuarios'}), 403

    data = request.get_json()
    username = data['username']
    password = data['password']
    is_superuser = data['is_superuser']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Usuarios (username, password, is_superuser) VALUES (?, ?, ?)",
                   (username, password, is_superuser))
    conn.commit()
    conn.close()
    return jsonify({'status': 'Usuario registrado exitosamente'}), 201

# Ruta para agregar un paciente
@app.route('/add_patient', methods=['POST'])
@jwt_required()
def add_patient():
    data = request.get_json()
    nombre = data['nombre']
    apellido = data['apellido']
    fecha_nacimiento = data['fecha_nacimiento']
    direccion = data['direccion']
    telefono = data['telefono']
    dni = data['dni']
    obra_social = data['obra_social']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Pacientes (nombre, apellido, fecha_nacimiento, direccion, telefono, dni, obra_social) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (nombre, apellido, fecha_nacimiento, direccion, telefono, dni, obra_social))
    conn.commit()
    conn.close()
    return jsonify({'status': 'Paciente agregado exitosamente'}), 201

# Ruta para obtener todos los pacientes
@app.route('/get_patients', methods=['GET'])
@jwt_required()
def get_patients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Pacientes")
    patients = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in patients])

# Ruta para agregar un médico
@app.route('/add_doctor', methods=['POST'])
@jwt_required()
def add_doctor():
    data = request.get_json()
    nombre = data['nombre']
    apellido = data['apellido']
    especialidad = data['especialidad']
    telefono = data['telefono']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Medicos (nombre, apellido, especialidad, telefono) VALUES (?, ?, ?, ?)",
                   (nombre, apellido, especialidad, telefono))
    conn.commit()
    conn.close()
    return jsonify({'status': 'Médico agregado exitosamente'}), 201

# Ruta para asignar un turno
@app.route('/add_appointment', methods=['POST'])
@jwt_required()
def add_appointment():
    data = request.get_json()
    paciente_dni = data['paciente_dni']
    medico_nombre_apellido = data['medico_nombre_apellido']
    fecha = data['fecha']
    hora = data['hora']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM Pacientes WHERE dni = ?", (paciente_dni,))
    paciente_id = cursor.fetchone()
    
    if not paciente_id:
        conn.close()
        return jsonify({'msg': 'No se encontró un paciente con ese DNI'}), 404

    paciente_id = paciente_id['id']

    nombre, apellido = medico_nombre_apellido.split(" ", 1)
    cursor.execute("SELECT id FROM Medicos WHERE nombre = ? AND apellido = ?", (nombre, apellido))
    medico_id = cursor.fetchone()

    if not medico_id:
        conn.close()
        return jsonify({'msg': 'No se encontró un médico con ese nombre y apellido'}), 404

    medico_id = medico_id['id']
    cursor.execute("INSERT INTO Turnos (paciente_id, medico_id, fecha, hora) VALUES (?, ?, ?, ?)",
                   (paciente_id, medico_id, fecha, hora))
    conn.commit()
    conn.close()
    return jsonify({'status': 'Turno asignado exitosamente'}), 201

# Ruta para obtener todos los turnos
@app.route('/get_appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Turnos")
    appointments = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in appointments])

# Ruta para editar un paciente
@app.route('/edit_patient', methods=['PUT'])
@jwt_required()
def edit_patient():
    data = request.get_json()
    dni_paciente = data['dni']
    nombre = data['nombre']
    apellido = data['apellido']
    fecha_nacimiento = data['fecha_nacimiento']
    direccion = data['direccion']
    telefono = data['telefono']
    obra_social = data['obra_social']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""UPDATE Pacientes SET nombre = ?, apellido = ?, fecha_nacimiento = ?, direccion = ?, 
                      telefono = ?, obra_social = ? WHERE dni = ?""",
                   (nombre, apellido, fecha_nacimiento, direccion, telefono, obra_social, dni_paciente))
    conn.commit()
    conn.close()
    return jsonify({'status': 'Paciente actualizado exitosamente'}), 200

# Ruta para eliminar un paciente
@app.route('/delete_patient', methods=['DELETE'])
@jwt_required()
def delete_patient():
    current_user = get_jwt_identity()
    if not current_user['is_superuser']:
        return jsonify({'msg': 'No tienes permisos para eliminar registros'}), 403

    data = request.get_json()
    dni_paciente = data['dni']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Pacientes WHERE dni = ?", (dni_paciente,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'Paciente eliminado exitosamente'}), 200

# Ruta para cambiar el estado de super usuario
@app.route('/update_superuser', methods=['PUT'])
@jwt_required()
def update_superuser():
    current_user = get_jwt_identity()
    if not current_user['is_superuser']:
        return jsonify({'msg': 'No tienes permisos para modificar el estado de super usuario'}), 403

    data = request.get_json()
    username = data['username']
    is_superuser = data['is_superuser']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Usuarios SET is_superuser = ? WHERE username = ?", (is_superuser, username))
    conn.commit()
    conn.close()
    return jsonify({'status': 'Estado de super usuario actualizado exitosamente'}), 200

if __name__ == '__main__':
    app.run(debug=True)

