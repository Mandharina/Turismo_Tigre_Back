import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

DATABASE = 'listaProvedores.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

#crea una tabla en la base de datos
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS proveedores (
    codigo INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    propietario TEXT NOT NULL,
    direccion TEXT NOT NULL,
    rubro TEXT NOT NULL
)
''')
    conn.commit()
    cursor.close()
    conn.close()

def create_database():
    conn = sqlite3.connect(DATABASE)
    conn.close()
    create_table()
# Crear la base de datos y la tabla si no existen
create_database()



#-----------------------------------------------------------------

class Proveedor:
    def __init__(self, codigo, nombre, propietario, direccion, rubro):
        self.codigo = codigo
        self.nombre = nombre
        self.propietario = propietario
        self.direccion = direccion
        self.rubro = rubro

    def modificar(self,nuevo_nombre, nuevo_propietario, nueva_direccion, nuevo_rubro):
        self.nombre = nuevo_nombre
        self.propietario = nuevo_propietario
        self.direccion = nueva_direccion
        self.rubro = nuevo_rubro

#------------------------------------------------
class ListaProveedores:
    def __init__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor()

    def agregar_proveedor(self, codigo, nombre, propietario, direccion, rubro):
        proveedor_existente = self.consultar_proveedor(codigo)
        if proveedor_existente:
            return jsonify({'message':'Ese proveedor ya fue dado de alta.'}),400

        nuevo_proveedor = Proveedor(codigo, nombre, propietario, direccion, rubro)
        self.cursor.execute("INSERT INTO proveedores VALUES (?, ?, ?, ?,?)", (codigo, nombre, propietario, direccion, rubro))
        self.conexion.commit()
        return jsonify ({'message':'Proveedor agregado con éxito'}), 200

    def consultar_proveedor(self, codigo):
        self.cursor.execute("SELECT * FROM proveedores WHERE codigo = ?", (codigo,))
        row = self.cursor.fetchone()
        if row:
            codigo, nombre, propietario, direccion, rubro = row
            return Proveedor(codigo, nombre, propietario, direccion, rubro)
        return False

    def modificar_proveedor(self, codigo, nuevo_nombre, nuevo_propietario, nuevo_direccion, nuevo_rubro):
        proveedor = self.consultar_proveedor(codigo)
        if proveedor:
            proveedor.modificar(nuevo_nombre, nuevo_propietario, nuevo_direccion, nuevo_rubro)
            self.cursor.execute("UPDATE proveedores SET nombre = ?, propietario = ?, direccion = ?, rubro = ? WHERE codigo = ?",
                                (nuevo_nombre, nuevo_propietario, nuevo_direccion, nuevo_rubro))
            self.conexion.commit()
            return jsonify({'message':'Proveedor modificado con éxito'}), 200
        return jsonify({'message':'Proveedor no encontrado'})

    def listar_proveedores(self):
        self.cursor.execute("SELECT * FROM proveedores")
        rows = self.cursor.fetchall()
        proveedores = []
        for row in rows:
            codigo, nombre, propietario, direccion, rubro  = row
            proveedor = {'codigo': codigo, 'nombre':nombre, 'propietario':propietario, 'dirección':direccion, 'rubro':rubro}
            proveedores.append(proveedor)
        return jsonify(proveedores), 200

    def eliminar_proveedor(self, codigo):
        self.cursor.execute("DELETE FROM proveedores WHERE codigo = ?", (codigo,))
        if self.cursor.rowcount > 0:            
            self.conexion.commit()
            return jsonify({'message': 'Proveedor eliminado definitivamente.'}), 200
        return jsonify ({'message': 'Proveedor no encontrado'}), 404 
#..........................................................................................
app = Flask(__name__)
CORS(app)

lista = ListaProveedores()
#-----------------------------------------------------------------------------------------------
#Ruta para buscar un producto según rubro, ver si esto devuelve 1 solo campo o todos los 
#coincidentes 

@app.route('/proveedores/<int:codigo>', methods=['GET'])
def buscar_proveedor(codigo):
    resultados = lista.consultar_proveedor(codigo)
    if resultados:
        return jsonify({
            'nombre' : resultados.nombre,
            'direccion' : resultados.direccion,
            'rubro' : resultados.rubro
        }), 200
    return jsonify({'message': 'Actualmente no contamos con infomación de ese rubro'}), 404

#---------------------------------------------------------------------------------------------------
#Lista de proveedores

@app.route('/proveedores', methods=['GET'])
def lista_de_proveedores():
    return lista.listar_proveedores()

#-------------------------------------------------------------------------------
#Agregar proveedor a la lista

@app.route('/proveedores', methods=['POST'])
def agregar_proveedor():
        codigo = request.json.get('codigo')
        nombre = request.json.get('nombre')
        propietario = request.json.get('propietario')
        direccion = request.json.get('direccion')
        rubro = request.json.get('rubro')
        return lista.agregar_proveedor(codigo, nombre, propietario,direccion, rubro), 200


#------------------------------------------------------------------------------------
#Modificar proveedor
@app.route('/proveedores/<int:codigo>', methods=['PUT'])
def modificar_proveedor(codigo):
    nuevo_nombre = request.json.get('nombre')
    nuevo_propietario = request.json.get('propietario')
    nueva_direccion = request.json.get('direccion')
    nuevo_rubro = request.json.get('rubro')
    return lista.modificar_proveedor(codigo, nuevo_nombre, nuevo_propietario, nueva_direccion, nuevo_rubro)

#--------------------------------------------------------------------------------------
#Eliminar proveedor
@app.route('/proveedores/<int:codigo>', methods=['DELETE'])
def eliminar_proveedor(codigo):
    return lista.eliminar_proveedor(codigo)

