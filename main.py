import sqlite3

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

    def modificar(self,nuevo_nombre, nuevo_propietario, nuevo_direccion, nuevo_rubro):
        self.nombre = nuevo_nombre
        self.propietario = nuevo_propietario
        self.direccion = nuevo_direccion
        self.rubro = nuevo_rubro

#------------------------------------------------
class ListaProveedores:
    def __init__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor()

    def agregar_proveedor(self, codigo, nombre, propietario, direccion, rubro):
        proveedor_existente = self.consultar_proveedor(codigo)
        if proveedor_existente:
            print("Ese proveedor ya fue dado de alta.")
            return False

        
        self.cursor.execute("INSERT INTO proveedores VALUES (?, ?, ?, ?,?)", (codigo, nombre, propietario, direccion, rubro))
        self.conexion.commit()
        return True

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

    def listar_proveedores(self):
        print("-" * 30)
        self.cursor.execute("SELECT * FROM proveedores")
        rows = self.cursor.fetchall()
        for row in rows:
            codigo, nombre, propietario, direccion, rubro  = row
            print(f"Código: {codigo}")
            print(f"Nombre: {nombre}")
            print(f"Propietario: {propietario}")
            print(f"Dirección: {direccion}")
            print(f"Rubro: {rubro}")
            print("-" * 30)

    def eliminar_proveedor(self, codigo):
        self.cursor.execute("DELETE FROM proveedores WHERE codigo = ?", (codigo,))
        if self.cursor.rowcount > 0:
            print("Proveedor eliminado.")
            self.conexion.commit()
        else:
            print("Proveedor no encontrado.")   
#..........................................................................................
lista = ListaProveedores()

lista.agregar_proveedor(1, "La fonda del tío", "Juan Gomez", "Lavalle 747", "Restaurante")

lista.listar_proveedores()
