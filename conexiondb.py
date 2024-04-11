import mysql.connector


class Registro_datos:
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Inserta tu contraseña aquí
            database="talleres",
        )

    def inserta_taller(self, nombre, descripcion, instructor, horario):
        cur = self.conexion.cursor()
        sql = """INSERT INTO talleres (nombre, descripcion, instructor, horario) 
                 VALUES (%s, %s, %s, %s)"""
        val = (nombre, descripcion, instructor, horario)
        cur.execute(sql, val)
        self.conexion.commit()
        cur.close()

    def obtener_talleres(self):
        cursor = self.conexion.cursor()
        sql = "SELECT * FROM talleres "
        cursor.execute(sql)
        talleres = cursor.fetchall()
        return talleres

    def obtener_compus(self):
        cursor = self.conexion.cursor()
        sql = "SELECT ocupada FROM compus "
        cursor.execute(sql)
        talleres = cursor.fetchall()
        return talleres

    def actualizar_estado_compu(self, num_compu, nuevo_estado):
        query = "UPDATE compus SET ocupada = %s WHERE numero = %s"
        cursor = self.conexion.cursor()
        cursor.execute(query, (nuevo_estado, num_compu))
        self.conexion.commit()

    def buscar_taller(self, id_taller):
        cur = self.conexion.cursor()
        sql = "SELECT * FROM talleres WHERE id_taller = %s"
        cur.execute(sql, (id_taller,))
        taller = cur.fetchone()
        cur.close()
        if taller:
            # Convertir la tupla a un diccionario
            taller_dict = {
                "id_taller": taller[0],
                "nombre": taller[1],
                "descripcion": taller[2],
                "instructor": taller[3],
                "horario": taller[4],
            }
            return taller_dict
        else:
            return None

    def eliminar_taller(self, id_taller):
        cur = self.conexion.cursor()
        sql = """DELETE FROM talleres WHERE id_taller = %s"""
        cur.execute(sql, (id_taller,))
        num_filas_afectadas = cur.rowcount
        self.conexion.commit()
        cur.close()
        return num_filas_afectadas

    def actualizar_taller(self, id_taller, nombre, descripcion, instructor, horario):
        cur = self.conexion.cursor()
        sql = """UPDATE talleres 
                 SET nombre = %s, descripcion = %s, instructor = %s, horario = %s 
                 WHERE id_taller = %s"""
        val = (nombre, descripcion, instructor, horario, id_taller)
        cur.execute(sql, val)
        num_filas_afectadas = cur.rowcount
        self.conexion.commit()
        cur.close()
        return num_filas_afectadas

    def buscar_alumnos_talleres(self, id_alumno):
        cur = self.conexion.cursor()

        # Consulta para obtener los detalles del alumno
        sql_alumno = "SELECT id_alumno, nombre, correo, telefono FROM alumnos WHERE id_alumno = %s"
        cur.execute(sql_alumno, (id_alumno,))
        datos_alumno = cur.fetchone()

        # Consulta para obtener los talleres en los que está inscrito el alumno (ESTA ES LA RELACIONAL)
        sql_talleres = "SELECT alumnos.nombre, talleres.nombre FROM alumnos_talleres INNER JOIN alumnos ON alumnos_talleres.id_alumno = alumnos.id_alumno INNER JOIN talleres ON alumnos_talleres.id_taller = talleres.id_taller WHERE alumnos_talleres.id_alumno = %s"
        cur.execute(sql_talleres, (id_alumno,))
        talleres_alumno = cur.fetchall()

        cur.close()

        return datos_alumno, talleres_alumno

    def obtener_nombres_talleres(self):
        cur = self.conexion.cursor()
        sql = "SELECT nombre FROM talleres"
        cur.execute(sql)
        nombres_talleres = cur.fetchall()
        cur.close()
        return nombres_talleres

    def obtener_id_taller_por_nombre(self, nombre_taller):
        cur = self.conexion.cursor()
        sql = "SELECT id_taller FROM talleres WHERE nombre = %s"
        cur.execute(sql, (nombre_taller,))
        result = cur.fetchone()
        cur.close()
        return result[0] if result else None

    def insertar_alumno_taller(self, id_alumno, id_taller):
        cur = self.conexion.cursor()
        sql = "INSERT INTO alumnos_talleres (id_alumno, id_taller) VALUES (%s, %s)"
        cur.execute(sql, (id_alumno, id_taller))
        num_filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
        self.conexion.commit()
        cur.close()
        return num_filas_afectadas  # Devolver el número de filas afectadas

    def buscar_usuario(self, username):
        cur = self.conexion.cursor()
        sql = "SELECT * FROM usuarios WHERE username = %s"
        cur.execute(sql, (username,))
        usuario = cur.fetchone()
        cur.close()
        if usuario:
            # Convertir la tupla a un diccionario
            usuario_dict = {
                "id_usuario": usuario[0],
                "username": usuario[1],
                "password": usuario[2],
                # Otros datos del usuario si es necesario
            }
            return usuario_dict
        else:
            return None

    """ PARA EL ARCHIVO SUBIR,O A LA BD """

    def guardar_archivo(self, nombre_corto, datos_archivo):
        try:
            cursor = self.conexion.cursor()

            sql = "INSERT INTO formatos (nombre_corto, archivo) VALUES (%s, %s)"
            cursor.execute(sql, (nombre_corto, datos_archivo))

            self.conexion.commit()
            cursor.close()

            print("Archivo guardado correctamente en la base de datos.")
        except Exception as e:
            print(f"Error al guardar el archivo en la base de datos: {e}")

    def guardar_archivo(self, ruta_archivo):
        if self.conexion:
            try:
                cursor = self.conexion.cursor()
                sql = "INSERT INTO formatos (archivo) VALUES (%s)"
                cursor.execute(sql, (ruta_archivo,))
                self.conexion.commit()
                cursor.close()
                print("Archivo guardado en la base de datos correctamente.")
            except mysql.connector.Error as error:
                print(f"Error al guardar el archivo en la base de datos: {error}")
        else:
            print("No hay conexión a la base de datos.")

    def obtener_archivo(self, id_archivo):
        query = "SELECT archivo FROM formatos WHERE id = %s"
        cursor = self.conexion.cursor()
        cursor.execute(query, (id_archivo,))
        archivo = cursor.fetchone()
        return archivo[0] if archivo else None

    def guardar_archivo(self, archivo):
        query = "INSERT INTO formatos (archivo) VALUES (%s)"
        cursor = self.conexion.cursor()
        cursor.execute(query, (archivo,))
        self.conexion.commit()
        cursor.close()

        return cursor.lastrowid  # Devuelve el ID del último archivo insertado

    def buscar_alumnos(self, texto_busqueda):
        query = "SELECT nombre FROM alumnos WHERE nombre LIKE %s"
        cursor = self.conexion.cursor()
        cursor.execute(query, (f"%{texto_busqueda}%",))
        resultados = cursor.fetchall()
        nombres_alumnos = [result[0] for result in resultados]
        return nombres_alumnos
