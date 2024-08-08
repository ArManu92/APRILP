import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from tkinter import Tk, Label, Entry, Button, IntVar, Checkbutton, messagebox
import sqlite3


# Variables globales para el superusuario y la ventana principal
is_superuser = False
main_window = None

def login(): # Función para login
    global main_window

    def autenticar():
        global is_superuser

        username = entry_username.get()
        password = entry_password.get()

        conn = sqlite3.connect('/Users/manuarlei/Library/CloudStorage/OneDrive-Personal/PROYECTOS PERSONALES/ENTORNO2/Clinica/db/Aprilp.db')
        c = conn.cursor()
        c.execute("SELECT * FROM Usuarios WHERE username = ? AND password = ?", (username, password))
        usuario = c.fetchone()
        conn.close()

        if usuario:
            is_superuser = usuario[3]  # Suponiendo que la columna is_superuser es la cuarta columna
            main_window.destroy()  # Cerrar la ventana principal de login
            iniciar_aplicacion()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    login_window = tk.Toplevel()
    login_window.title("Login")

    tk.Label(login_window, text="Username").grid(row=0, column=0)
    entry_username = tk.Entry(login_window)
    entry_username.grid(row=0, column=1)

    tk.Label(login_window, text="Password").grid(row=1, column=0)
    entry_password = tk.Entry(login_window, show='*')
    entry_password.grid(row=1, column=1)

    tk.Button(login_window, text="Login", command=autenticar).grid(row=2, column=1)

def registrar_usuario(): # Función para registrar un nuevo usuario
    if not is_superuser:
        messagebox.showerror("Error", "No tienes permisos para registrar usuarios")
        return

    def guardar_usuario():
        username = entry_username.get()
        password = entry_password.get()
        is_superuser_value = var_is_superuser.get()

        conn = sqlite3.connect('/Users/manuarlei/Library/CloudStorage/OneDrive-Personal/PROYECTOS PERSONALES/ENTORNO2/Clinica/db/Aprilp.db')
        c = conn.cursor()
        c.execute("INSERT INTO Usuarios (username, password, is_superuser) VALUES (?, ?, ?)",
                  (username, password, is_superuser_value))
        conn.commit()
        conn.close()

        messagebox.showinfo("Info", "Usuario registrado exitosamente")
        registrar_window.destroy()

    registrar_window = tk.Toplevel()
    registrar_window.title("Registrar Usuario")

    tk.Label(registrar_window, text="Username").grid(row=0, column=0)
    entry_username = tk.Entry(registrar_window)
    entry_username.grid(row=0, column=1)

    tk.Label(registrar_window, text="Password").grid(row=1, column=0)
    entry_password = tk.Entry(registrar_window, show='*')
    entry_password.grid(row=1, column=1)

    tk.Label(registrar_window, text="Super Usuario").grid(row=2, column=0)
    var_is_superuser = tk.IntVar()
    check_is_superuser = tk.Checkbutton(registrar_window, variable=var_is_superuser)
    check_is_superuser.grid(row=2, column=1)

    tk.Button(registrar_window, text="Registrar", command=guardar_usuario).grid(row=3, column=1)

# Funciones para la base de datos
def agregar_paciente():
    def guardar_paciente():
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        fecha_nacimiento = entry_fecha_nacimiento.get()
        direccion = entry_direccion.get()
        telefono = entry_telefono.get()
        dni = entry_dni.get()
        obra_social = entry_obra_social.get()

        conn = sqlite3.connect('/Users/manuarlei/Library/CloudStorage/OneDrive-Personal/PROYECTOS PERSONALES/ENTORNO2/Clinica/db/Aprilp.db')
        c = conn.cursor()
        c.execute("INSERT INTO Pacientes (nombre, apellido, fecha_nacimiento, direccion, telefono, dni, obra_social) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (nombre, apellido, fecha_nacimiento, direccion, telefono, dni, obra_social))
        conn.commit()
        conn.close()

        messagebox.showinfo("Info", "Paciente agregado exitosamente")
        paciente_window.destroy()

    paciente_window = tk.Toplevel()
    paciente_window.title("Agregar Paciente")

    tk.Label(paciente_window, text="Nombre").grid(row=0, column=0)
    entry_nombre = tk.Entry(paciente_window)
    entry_nombre.grid(row=0, column=1)

    tk.Label(paciente_window, text="Apellido").grid(row=1, column=0)
    entry_apellido = tk.Entry(paciente_window)
    entry_apellido.grid(row=1, column=1)

    tk.Label(paciente_window, text="Fecha de Nacimiento").grid(row=2, column=0)
    entry_fecha_nacimiento = tk.Entry(paciente_window)
    entry_fecha_nacimiento.grid(row=2, column=1)

    tk.Label(paciente_window, text="Dirección").grid(row=3, column=0)
    entry_direccion = tk.Entry(paciente_window)
    entry_direccion.grid(row=3, column=1)

    tk.Label(paciente_window, text="Teléfono").grid(row=4, column=0)
    entry_telefono = tk.Entry(paciente_window)
    entry_telefono.grid(row=4, column=1)

    tk.Label(paciente_window, text="DNI").grid(row=5, column=0)
    entry_dni = tk.Entry(paciente_window)
    entry_dni.grid(row=5, column=1)

    tk.Label(paciente_window, text="Obra Social").grid(row=6, column=0)
    entry_obra_social = tk.Entry(paciente_window)
    entry_obra_social.grid(row=6, column=1)

    tk.Button(paciente_window, text="Guardar", command=guardar_paciente).grid(row=7, column=1)

def agregar_medico():
    def guardar_medico():
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        especialidad = entry_especialidad.get()
        telefono = entry_telefono.get()

        conn = sqlite3.connect('/Users/manuarlei/Library/CloudStorage/OneDrive-Personal/PROYECTOS PERSONALES/ENTORNO2/Clinica/db/Aprilp.db')
        c = conn.cursor()
        c.execute("INSERT INTO Medicos (nombre, apellido, especialidad, telefono) VALUES (?, ?, ?, ?)",
                  (nombre, apellido, especialidad, telefono))
        conn.commit()
        conn.close()

        messagebox.showinfo("Info", "Médico agregado exitosamente")
        medico_window.destroy()

    medico_window = tk.Toplevel()
    medico_window.title("Agregar Médico")

    tk.Label(medico_window, text="Nombre").grid(row=0, column=0)
    entry_nombre = tk.Entry(medico_window)
    entry_nombre.grid(row=0, column=1)

    tk.Label(medico_window, text="Apellido").grid(row=1, column=0)
    entry_apellido = tk.Entry(medico_window)
    entry_apellido.grid(row=1, column=1)

    tk.Label(medico_window, text="Especialidad").grid(row=2, column=0)
    entry_especialidad = tk.Entry(medico_window)
    entry_especialidad.grid(row=2, column=1)

    tk.Label(medico_window, text="Teléfono").grid(row=3, column=0)
    entry_telefono = tk.Entry(medico_window)
    entry_telefono.grid(row=3, column=1)

    tk.Button(medico_window, text="Guardar", command=guardar_medico).grid(row=4, column=1)

def asignar_turno():
    def guardar_turno():
        paciente_dni = entry_paciente_dni.get()
        medico_nombre_apellido = combo_medico.get()
        fecha = entry_fecha.get()
        hora = entry_hora.get()

        conn = sqlite3.connect('/Users/manuarlei/Library/CloudStorage/OneDrive-Personal/PROYECTOS PERSONALES/ENTORNO2/Clinica/db/Aprilp.db')
        c = conn.cursor()

        # Obtener el id del paciente usando el dni
        c.execute("SELECT id FROM Pacientes WHERE dni = ?", (paciente_dni,))
        paciente_id = c.fetchone()
        
        if paciente_id:
            paciente_id = paciente_id[0]

            # Obtener el id del médico usando el nombre y apellido
            nombre, apellido = medico_nombre_apellido.split(" ", 1)
            c.execute("SELECT id FROM Medicos WHERE nombre = ? AND apellido = ?", (nombre, apellido))
            medico_id = c.fetchone()

            if medico_id:
                medico_id = medico_id[0]
                c.execute("INSERT INTO Turnos (paciente_id, medico_id, fecha, hora) VALUES (?, ?, ?, ?)",
                          (paciente_id, medico_id, fecha, hora))
                conn.commit()
                messagebox.showinfo("Info", "Turno asignado exitosamente")
            else:
                messagebox.showerror("Error", "No se encontró un médico con ese nombre y apellido")
        else:
            messagebox.showerror("Error", "No se encontró un paciente con ese DNI")
        
        conn.close()
        turno_window.destroy()

    turno_window = tk.Toplevel()
    turno_window.title("Asignar Turno")

    tk.Label(turno_window, text="DNI Paciente").grid(row=0, column=0)
    entry_paciente_dni = tk.Entry(turno_window)
    entry_paciente_dni.grid(row=0, column=1)

    tk.Label(turno_window, text="Médico").grid(row=1, column=0)
    combo_medico = ttk.Combobox(turno_window)
    combo_medico.grid(row=1, column=1)

    # Poblar el combobox con nombres y apellidos de los médicos
    conn = sqlite3.connect('/Users/manuarlei/Library/CloudStorage/OneDrive-Personal/PROYECTOS PERSONALES/ENTORNO2/Clinica/db/Aprilp.db')
    c = conn.cursor()
    c.execute("SELECT nombre, apellido FROM Medicos")
    medicos = c.fetchall()
    conn.close()

    combo_medico['values'] = [" ".join(medico) for medico in medicos]

    tk.Label(turno_window, text="Fecha").grid(row=2, column=0)
    entry_fecha = DateEntry(turno_window, selectmode='day')
    entry_fecha.grid(row=2, column=1)

    tk.Label(turno_window, text="Hora").grid(row=3, column=0)
    entry_hora = tk.Entry(turno_window)
    entry_hora.grid(row=3, column=1)

    tk.Button(turno_window, text="Guardar", command=guardar_turno).grid(row=4, column=1)

def editar_paciente():
    def buscar_paciente():
        dni_paciente = entry_dni.get()
        
        conn = sqlite3.connect('/Users/manuarlei/Library/CloudStorage/OneDrive-Personal/PROYECTOS PERSONALES/ENTORNO2/Clinica/db/Aprilp.db')
        c = conn.cursor()
        c.execute("SELECT * FROM Pacientes WHERE dni = ?", (dni_paciente,))
        paciente = c.fetchone()
        conn.close()
        
        if paciente:
            entry_nombre.insert(0, paciente[1])
            entry_apellido.insert(0, paciente[2])
            entry_fecha_nacimiento.insert(0, paciente[3])
            entry_direccion.insert(0, paciente[4])
            entry_telefono.insert(0, paciente[5])
            entry_dni.config(state='disabled')
            entry_obra_social.insert(0, paciente[7])
        else:
            messagebox.showerror("Error", "No se encontró un paciente con ese DNI")

    def guardar_cambios():
        dni_paciente = entry_dni.get()
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        fecha_nacimiento = entry_fecha_nacimiento.get()
        direccion = entry_direccion.get()
        telefono = entry_telefono.get()
        obra_social = entry_obra_social.get()

        conn = sqlite3.connect('/Users/manuarlei/Library/CloudStorage/OneDrive-Personal/PROYECTOS PERSONALES/ENTORNO2/Clinica/db/Aprilp.db')
        c = conn.cursor()
        c.execute("""UPDATE Pacientes SET nombre = ?, apellido = ?, fecha_nacimiento = ?, direccion = ?, 
                     telefono = ?, obra_social = ? WHERE dni = ?""",
                  (nombre, apellido, fecha_nacimiento, direccion, telefono, obra_social, dni_paciente))
        conn.commit()
        conn.close()

        messagebox.showinfo("Info", "Paciente actualizado exitosamente")
        editar_window.destroy()

    editar_window = tk.Toplevel()
    editar_window.title("Editar Paciente")

    tk.Label(editar_window, text="DNI Paciente").grid(row=0, column=0)
    entry_dni = tk.Entry(editar_window)
    entry_dni.grid(row=0, column=1)

    tk.Button(editar_window, text="Buscar", command=buscar_paciente).grid(row=0, column=2)

    tk.Label(editar_window, text="Nombre").grid(row=1, column=0)
    entry_nombre = tk.Entry(editar_window)
    entry_nombre.grid(row=1, column=1)

    tk.Label(editar_window, text="Apellido").grid(row=2, column=0)
    entry_apellido = tk.Entry(editar_window)
    entry_apellido.grid(row=2, column=1)

    tk.Label(editar_window, text="Fecha de Nacimiento").grid(row=3, column=0)
    entry_fecha_nacimiento = tk.Entry(editar_window)
    entry_fecha_nacimiento.grid(row=3, column=1)

    tk.Label(editar_window, text="Dirección").grid(row=4, column=0)
    entry_direccion = tk.Entry(editar_window)
    entry_direccion.grid(row=4, column=1)

    tk.Label(editar_window, text="Teléfono").grid(row=5, column=0)
    entry_telefono = tk.Entry(editar_window)
    entry_telefono.grid(row=5, column=1)

    tk.Label(editar_window, text="Obra Social").grid(row=6, column=0)
    entry_obra_social = tk.Entry(editar_window)
    entry_obra_social.grid(row=6, column=1)

    tk.Button(editar_window, text="Guardar", command=guardar_cambios).grid(row=7, column=1)

def eliminar_paciente():
    if not is_superuser:
        messagebox.showerror("Error", "No tienes permisos para eliminar registros")
        return

    def eliminar():
        dni_paciente = entry_dni.get()

        conn = sqlite3.connect('/Users/manuarlei/Library/CloudStorage/OneDrive-Personal/PROYECTOS PERSONALES/ENTORNO2/Clinica/db/Aprilp.db')
        c = conn.cursor()
        c.execute("DELETE FROM Pacientes WHERE dni = ?", (dni_paciente,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Info", "Paciente eliminado exitosamente")
        eliminar_window.destroy()

    eliminar_window = tk.Toplevel()
    eliminar_window.title("Eliminar Paciente")

    tk.Label(eliminar_window, text="DNI Paciente").grid(row=0, column=0)
    entry_dni = tk.Entry(eliminar_window)
    entry_dni.grid(row=0, column=1)

    tk.Button(eliminar_window, text="Eliminar", command=eliminar).grid(row=1, column=1)


def cambiar_super_usuario():
    def actualizar_super_usuario():
        username = entry_username.get()
        is_superuser_value = var_is_superuser.get()

        conn = sqlite3.connect('/Users/manuarlei/Library/CloudStorage/OneDrive-Personal/PROYECTOS PERSONALES/ENTORNO2/Clinica/db/Aprilp.db')
        c = conn.cursor()
        c.execute("UPDATE Usuarios SET is_superuser = ? WHERE username = ?", (is_superuser_value, username))
        conn.commit()
        conn.close()

        messagebox.showinfo("Info", "Estado de super usuario actualizado exitosamente")
        cambiar_window.destroy()

    cambiar_window = Tk()
    cambiar_window.title("Cambiar Super Usuario")

    Label(cambiar_window, text="Username").grid(row=0, column=0)
    entry_username = Entry(cambiar_window)
    entry_username.grid(row=0, column=1)

    Label(cambiar_window, text="Super Usuario").grid(row=1, column=0)
    var_is_superuser = IntVar()
    check_is_superuser = Checkbutton(cambiar_window, variable=var_is_superuser)
    check_is_superuser.grid(row=1, column=1)

    Button(cambiar_window, text="Actualizar", command=actualizar_super_usuario).grid(row=2, column=1)


def iniciar_aplicacion():
    root = tk.Tk()
    root.title("Gestión de Clínica")

    tk.Button(root, text="Agregar Paciente", command=agregar_paciente).grid(row=0, column=0, padx=10, pady=10)
    tk.Button(root, text="Agregar Médico", command=agregar_medico).grid(row=0, column=1, padx=10, pady=10)
    tk.Button(root, text="Asignar Turno", command=asignar_turno).grid(row=0, column=2, padx=10, pady=10)
    tk.Button(root, text="Mostrar Turnos", command=mostrar_turnos).grid(row=0, column=3, padx=10, pady=10)
    tk.Button(root, text="Editar Paciente", command=editar_paciente).grid(row=1, column=0, padx=10, pady=10)
    #tk.Button(root, text="Eliminar Paciente", command=eliminar_paciente).grid(row=1, column=1, padx=10, pady=10)

    if is_superuser:
        tk.Button(root, text="Registrar Usuario", command=registrar_usuario).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(root, text="Modificar Usuario", command=cambiar_super_usuario).grid(row=1, column=2, padx=10, pady=10)
        tk.Button(root, text="Eliminar Paciente", command=eliminar_paciente).grid(row=1, column=3, padx=10, pady=10)

    root.mainloop()

def mostrar_turnos():
    def buscar_turnos():
        fecha = entry_fecha.get()

        conn = sqlite3.connect('/Users/manuarlei/Library/CloudStorage/OneDrive-Personal/PROYECTOS PERSONALES/ENTORNO2/Clinica/db/Aprilp.db')
        c = conn.cursor()
        c.execute("SELECT Pacientes.nombre, Pacientes.apellido, Turnos.hora, Medicos.nombre, Medicos.apellido "
                  "FROM Turnos "
                  "JOIN Pacientes ON Turnos.paciente_id = Pacientes.id "
                  "JOIN Medicos ON Turnos.medico_id = Medicos.id "
                  "WHERE Turnos.fecha = ?", (fecha,))
        turnos = c.fetchall()
        conn.close()

        for turno in turnos:
            tree.insert("", "end", values=turno)

    turnos_window = tk.Toplevel()
    turnos_window.title("Turnos Asignados")

    tk.Label(turnos_window, text="Fecha").grid(row=0, column=0)
    entry_fecha = DateEntry(turnos_window, selectmode='day')
    entry_fecha.grid(row=0, column=1)

    tk.Button(turnos_window, text="Buscar", command=buscar_turnos).grid(row=0, column=2)

    columns = ("Nombre Paciente", "Apellido Paciente", "Hora", "Nombre Medico", "Apellido Medico")
    tree = ttk.Treeview(turnos_window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
    tree.grid(row=1, column=0, columnspan=3)

# Crear la ventana principal de login/registro
main_window = tk.Tk()
main_window.title("Sistema de Login")

tk.Button(main_window, text="Login", command=login).grid(row=0, column=0, padx=10, pady=10)
#tk.Button(main_window, text="Registrar", command=registrar_usuario).grid(row=0, column=1, padx=10, pady=10)

main_window.mainloop()

