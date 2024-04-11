import sys
import io
from os.path import expanduser
from PyQt5 import uic, QtGui


from tkinter import messagebox
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QFileDialog,
    QLabel,
)
from uitaller import Ui_TALLERUTC
from PyQt6.QtCore import QStringListModel

from PyQt6 import QtWidgets  # responsive
from PyQt6 import QtCore  # respinsive
from PyQt6.QtWidgets import QTableWidgetItem
from conexiondb import Registro_datos  # NO


class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_TALLERUTC()
        self.ui.setupUi(self)  # Configurar la interfaz de usuario

        self.datosTotal = Registro_datos()

        self.ui.frame_lateral.setVisible(False)
        self.frame_lateral = False  # Definir la variable frame_lateral
        # Por defecto, el inicamos en login no está visible
        self.mostrar_pagina_login()
        self.ui.btn_descargar_archivo.clicked.connect(self.descargar_archivo)
        # Conectar los botones a sus funciones correspondientes
        """ botones paginas """
        self.ui.btn_home.clicked.connect(self.mostrar_pagina_home)
        self.ui.btn_agregar.clicked.connect(self.mostrar_pagina_agregar)
        self.ui.btn_alumno.clicked.connect(self.mostrar_pagina_alumnos)
        self.ui.btn_editar.clicked.connect(self.mostrar_pagina_editar)
        self.ui.btn_eliminar.clicked.connect(self.mostrar_pagina_eliminar)
        self.ui.btn_mostrar.clicked.connect(self.mostrar_pagina_mostrar)
        self.ui.btn_user.clicked.connect(self.mostrar_pagina_login)
        self.ui.btn_archivo.clicked.connect(self.mostrar_pagina_archivo)
        self.ui.btn_tutoria.clicked.connect(self.mostrar_pagina_compus)

        """ botones funciones """
        self.ui.btn_menu.clicked.connect(self.toggle_menu)
        self.ui.btn_refrescar.clicked.connect(
            self.actualizar_tabla_talleres
        )  # Conectar botón de refrescar
        self.ui.btn_guardar.clicked.connect(self.insertar_taller)
        self.ui.btn_taller_eliminar.clicked.connect(self.eliminar_taller)
        self.ui.btn_taller_buscar.clicked.connect(self.buscar_taller)
        self.ui.btn_taller_editar.clicked.connect(self.editar_taller)
        self.ui.btn_alumno_buscar.clicked.connect(self.buscar_alumnos_talleres)
        self.ui.btn_alumno_buscar_2.clicked.connect(self.agregar_alumno_taller)
        self.ui.btn_ingresar.clicked.connect(self.iniciar_sesion)
        self.ui.btn_abrir_explorador.clicked.connect(self.abrir_explorador)
        self.ui.btn_abrir_archivo.clicked.connect(self.guardar_en_bd)
        self.ui.btn_buscar_archivo.clicked.connect(self.seleccionar_archivo)
        self.ui.lineEdit.textChanged.connect(self.buscar_alumnos)

        """ AQUI COMPUS """

        compus = self.datosTotal.obtener_compus()
        self.ui.status1.setText(compus[0][0])
        self.ui.status2.setText(compus[1][0])
        self.ui.status3.setText(compus[2][0])
        # Conectar los botones a las funciones correspondientes
        self.ui.btnOcupar1.clicked.connect(lambda: self.actualizar_estado(1))
        self.ui.btnOcupar2.clicked.connect(lambda: self.actualizar_estado(2))
        self.ui.btnOcupar3.clicked.connect(lambda: self.actualizar_estado(3))

    def actualizar_estado(self, num_compu):
        compus = self.datosTotal.obtener_compus()
        estado_actual = compus[num_compu - 1][0]  # Índices de lista comienzan en 0
        nuevo_estado = "libre" if estado_actual == "ocupada" else "ocupada"

        # Actualizar el estado en la base de datos
        self.datosTotal.actualizar_estado_compu(num_compu, nuevo_estado)

        # Actualizar la interfaz de usuario
        if num_compu == 1:
            self.ui.status1.setText(nuevo_estado)
        elif num_compu == 2:
            self.ui.status2.setText(nuevo_estado)
        elif num_compu == 3:
            self.ui.status3.setText(nuevo_estado)

    def toggle_menu(self):
        # Alternar la visibilidad del frame lateral
        self.ui.frame_lateral.setVisible(not self.frame_lateral)

        # Actualizar el estado de visibilidad del frame lateral
        self.frame_lateral = not self.frame_lateral

        screen_width = QtWidgets.QApplication.primaryScreen().size().width()

        screen_height = QtWidgets.QApplication.primaryScreen().size().height()

        if self.frame_lateral:
            # Si el menú lateral está visible, ajusta la geometría del QLabel
            self.ui.label_7.setGeometry(QtCore.QRect(-10, 300, 581, 221))
            self.ui.label_8.setGeometry(QtCore.QRect(440, 10, 91, 101))
            self.ui.label_6.setGeometry(QtCore.QRect(30, 70, 521, 181))
            self.ui.label_2.setGeometry(QtCore.QRect(18, 10, 501, 41))
        else:
            # Si el menú lateral no está visible, expande el QLabel para que ocupe toda la pantalla
            self.ui.label_7.setGeometry(QtCore.QRect(-10, 300, screen_width - 500, 221))
            self.ui.label_8.setGeometry(QtCore.QRect(650, 10, 91, 101))
            self.ui.label_6.setGeometry(QtCore.QRect(150, 70, 500, 181))
            self.ui.label_2.setGeometry(QtCore.QRect(150, 10, 501, 41))

    def mostrar_pagina_home(self):
        # Mostrar la página de inicio (page_home)
        index = self.ui.pages.indexOf(self.ui.page_home)
        self.ui.pages.setCurrentIndex(index)

    def mostrar_pagina_agregar(self):
        # Mostrar la página de agregar (page_agregar)
        index = self.ui.pages.indexOf(self.ui.page_agregar)
        self.ui.pages.setCurrentIndex(index)

    def mostrar_pagina_alumnos(self):
        # Mostrar la página de alumnos (page_alumno)
        index = self.ui.pages.indexOf(self.ui.page_alumnos)
        self.ui.pages.setCurrentIndex(index)

    def mostrar_pagina_compus(self):
        # Mostrar la página de alumnos (page_alumno)
        index = self.ui.pages.indexOf(self.ui.page_compus)
        self.ui.pages.setCurrentIndex(index)

    def mostrar_pagina_editar(self):
        # Mostrar la página de editar (page_editar)
        index = self.ui.pages.indexOf(self.ui.page_editar)
        self.ui.pages.setCurrentIndex(index)

    def mostrar_pagina_eliminar(self):
        # Mostrar la página de eliminar (page_eliminar)
        index = self.ui.pages.indexOf(self.ui.page_eliminar)
        self.ui.pages.setCurrentIndex(index)

    def mostrar_pagina_mostrar(self):
        # Mostrar la página de mostrar (page_mostrar)
        index = self.ui.pages.indexOf(self.ui.page_mostrar)
        self.ui.pages.setCurrentIndex(index)

    def mostrar_pagina_login(self):
        # Mostrar la página de mostrar (page_mostrar)
        index = self.ui.pages.indexOf(self.ui.page_login)
        self.ui.pages.setCurrentIndex(index)

    def mostrar_pagina_archivo(self):
        # Mostrar la página de mostrar (page_mostrar)
        index = self.ui.pages.indexOf(self.ui.page_archivos)
        self.ui.pages.setCurrentIndex(index)

    """ OBTENER DATOS DE LOS TALLERES """

    def actualizar_tabla_talleres(self):
        # Limpiar la tabla antes de rellenarla
        self.ui.tb_taller.clearContents()
        self.ui.tb_taller.setRowCount(0)

        # Obtener los talleres desde la base de datos
        talleres = self.datosTotal.obtener_talleres()

        # Rellenar la tabla con los d
        # atos de los talleres
        for fila, datos_taller in enumerate(talleres):
            self.ui.tb_taller.insertRow(fila)
            for columna, dato in enumerate(datos_taller):
                item = QTableWidgetItem(str(dato))
                self.ui.tb_taller.setItem(fila, columna, item)

    """ INSERTAR TALLER FORMULARIO """

    def insertar_taller(self):
        # Obtener los datos de los campos de texto
        nombre = self.ui.nombre_agregar.text()
        descripcion = self.ui.descripcion_agregar.text()
        instructor = self.ui.instructor_agregar.text()
        horario = self.ui.horario_agregar.text()

        # Insertar los datos en la base de datos
        self.datosTotal.inserta_taller(nombre, descripcion, instructor, horario)

        # Mostrar un mensaje de éxito
        QMessageBox.information(
            self,
            "Éxito",
            "El taller se ha agregado correctamente a la base de datos.",
            QMessageBox.StandardButton.Ok,
        )

        # Limpiar los campos de texto después de la inserción
        self.ui.nombre_agregar.clear()
        self.ui.descripcion_agregar.clear()
        self.ui.instructor_agregar.clear()
        self.ui.horario_agregar.clear()

    """ ELIMINAR TALLERES  """

    def eliminar_taller(self):
        # Obtener el ID del taller a eliminar desde el campo de texto
        id_taller = self.ui.id_taller_eliminar.text()

        # Verificar si se ingresó un ID válido
        if not id_taller:
            QMessageBox.warning(
                self,
                "Advertencia",
                "Por favor, ingresa el ID del taller a eliminar.",
                QMessageBox.StandardButton.Ok,
            )
            return

        # Confirmar si el usuario realmente desea eliminar el taller
        respuesta = QMessageBox.question(
            self,
            "Confirmación",
            "¿Estás seguro de que deseas eliminar este taller?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if respuesta == QMessageBox.StandardButton.No:
            return

        # Intentar eliminar el taller de la base de datos
        eliminado = self.datosTotal.eliminar_taller(id_taller)

        if eliminado:
            # Mostrar un mensaje de éxito
            QMessageBox.information(
                self,
                "Éxito",
                f"El taller con ID {id_taller} ha sido eliminado correctamente.",
                QMessageBox.StandardButton.Ok,
            )
            self.ui.lbl_respuesta.setText(f"Taller eliminado :) ")
        else:
            # Mostrar un mensaje de error si no se pudo eliminar el taller
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo eliminar el taller con ID {id_taller}.",
                QMessageBox.StandardButton.Ok,
            )

        # Limpiar el campo de texto después de la eliminación
        self.ui.id_taller_eliminar.clear()

    """ BUSCAR TALLERES """

    def buscar_taller(self):
        id_taller = self.ui.id_taller_editar.text()
        taller = self.datosTotal.buscar_taller(id_taller)
        if taller:

            self.ui.nombre_editar.setText(taller["nombre"])
            self.ui.descripcion_editar.setText(taller["descripcion"])
            self.ui.instructor_editar.setText(taller["instructor"])
            self.ui.horario_editar.setText(taller["horario"])
        else:
            # Mostrar un mensaje de error si el taller no se encuentra
            QtWidgets.QMessageBox.critical(self, "Error", "Taller no encontrado")

    """ EDITAR O ACTUALIZAR TALLERES """

    def editar_taller(self):
        id_taller = self.ui.id_taller_editar.text()
        nombre = self.ui.nombre_editar.text()
        descripcion = self.ui.descripcion_editar.text()
        instructor = self.ui.instructor_editar.text()
        horario = self.ui.horario_editar.text()

        # Aquí llamas a la función que actualiza los datos del taller en la base de datos
        num_filas_afectadas = self.datosTotal.actualizar_taller(
            id_taller, nombre, descripcion, instructor, horario
        )

        if num_filas_afectadas > 0:
            # Mostrar un mensaje de éxito si se actualiza correctamente
            QtWidgets.QMessageBox.information(
                self, "Éxito", "Taller actualizado correctamente"
            )
        else:
            # Mostrar un mensaje de error si no se actualiza correctamente
            QtWidgets.QMessageBox.critical(
                self, "Error", "No se pudo actualizar el taller"
            )

    """ ALUMNOS Y TALLER RELACIONALES """

    def buscar_alumnos_talleres(self):
        id_alumno = self.ui.id_alumno_buscar.text()
        datos_alumno, talleres_alumno = self.datosTotal.buscar_alumnos_talleres(
            id_alumno
        )

        if datos_alumno:

            self.ui.tb_alumno.setRowCount(0)

            self.ui.tb_alumno.insertRow(0)
            for column_number, data in enumerate(datos_alumno):
                self.ui.tb_alumno.setItem(
                    0, column_number, QtWidgets.QTableWidgetItem(str(data))
                )
        else:

            QtWidgets.QMessageBox.critical(self, "Error", "Alumno no encontrado")

        if talleres_alumno:

            self.ui.tb_alumno_taller.setRowCount(0)

            for row_number, taller in enumerate(talleres_alumno):
                self.ui.tb_alumno_taller.insertRow(row_number)
                for column_number, data in enumerate(taller):
                    self.ui.tb_alumno_taller.setItem(
                        row_number, column_number, QtWidgets.QTableWidgetItem(str(data))
                    )
        else:

            QtWidgets.QMessageBox.information(
                self, "Información", "El alumno no está inscrito en ningún taller"
            )
        nombres_talleres = self.datosTotal.obtener_nombres_talleres()

        self.ui.lista_taller.clear()

        for taller in nombres_talleres:
            self.ui.lista_taller.addItem(taller[0])

    """ AGREGAR ALUMNO A TALLER """

    def agregar_alumno_taller(self):
        id_alumno = self.ui.id_alumno_buscar.text()

        # Verificar si se ha seleccionado un elemento de la lista de talleres
        if self.ui.lista_taller.currentItem() is None:
            QtWidgets.QMessageBox.critical(
                self, "Error", "Por favor selecciona un taller"
            )
            return

        nombre_taller = self.ui.lista_taller.currentItem().text()

        id_taller = self.datosTotal.obtener_id_taller_por_nombre(nombre_taller)

        # Verificar si se seleccionó un taller válido
        if id_taller is None:
            QtWidgets.QMessageBox.critical(
                self, "Error", "Por favor selecciona un taller válido"
            )
            return

        # Realizar la inserción en la tabla alumnos_talleres
        num_filas_afectadas = self.datosTotal.insertar_alumno_taller(
            id_alumno, id_taller
        )

        if num_filas_afectadas > 0:
            QtWidgets.QMessageBox.information(
                self, "Éxito", "Alumno inscrito correctamente en el taller"
            )
        else:
            QtWidgets.QMessageBox.critical(
                self, "Error", "Error al inscribir al alumno en el taller"
            )

    def iniciar_sesion(self):
        # Obtener los datos ingresados por el usuario
        username = self.ui.usuario_login.text()
        password = self.ui.contrasena_login.text()

        # Buscar el usuario en la base de datos
        usuario = self.datosTotal.buscar_usuario(username)

        if usuario:
            # Verificar si la contraseña ingresada coincide con la almacenada en la base de datos
            if password == usuario["password"]:
                QMessageBox.information(
                    self.ui.page_login,
                    "Inicio de Sesión Exitoso",
                    "¡Bienvenido!",
                    QMessageBox.StandardButton.Ok,
                )
                index = self.ui.pages.indexOf(self.ui.page_home)
                self.ui.label_2.setText(username)
                self.ui.pages.setCurrentIndex(index)
            else:
                QMessageBox.warning(
                    self.ui.page_login,
                    "Error de Inicio de Sesión",
                    "La contraseña es incorrecta",
                    QMessageBox.StandardButton.Ok,
                )
        else:
            QMessageBox.warning(
                self.ui.page_login,
                "Error de Inicio de Sesión",
                "El usuario no existe",
                QMessageBox.StandardButton.Ok,
            )

    def abrir_explorador(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Arvo",
            "",
            "Archivos (*.pdf *.txt *.docx);;Todos los archivos (*.*)",
        )
        if file_path:
            self.ruta_archivo = file_path

    def guardar_en_bd(self):
        if hasattr(self, "ruta_archivo"):
            self.datosTotal.guardar_archivo(self.ruta_archivo)
        else:
            print("Primero selecciona un archivo.")

    def descargar_archivo(self):
        id_archivo = 6  # ID des descargar
        archivo = self.datosTotal.obtener_archivo(id_archivo)
        if archivo:
            # Abrir archivos
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Guardar Archivo", "", "Archivos WORD (*.docx)"
            )
            if file_name:
                # Guardar el archivo eada
                with open(file_name, "wb") as file:
                    file.write(archivo)
                print("Archivo guardado exitosamente en:", file_name)
                
            else:
                print("La operación fue cancelada.")
        else:
            print("No se encontró el archivo en la base de datos.")

    def seleccionar_archivo(self):
        # Abrir el diálogo de selección de archivos
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar Archivo", "", "Archivos WORD (*.docx)"
        )
        if file_name:
            # Leer el archivo seleccionado
            with open(file_name, "rb") as file:
                archivo = file.read()

            # Guardar el archivo en la base de datos
            id_archivo = self.datosTotal.guardar_archivo(archivo)
            if id_archivo:
                print("Archivo guardado en la base de datos con ID:", id_archivo)
            else:
                print("Error al guardar el archivo en la base de datos.")
        else:
            print("No se seleccionó ningún archivo.")

    """ AQUI ES PA el buscador"""

    def buscar_alumnos(self, texto):
        texto_busqueda = texto.strip()

        if texto_busqueda:

            nombres_alumnos = self.datosTotal.buscar_alumnos(texto_busqueda)
            model = QStringListModel(nombres_alumnos)
            self.ui.listView.setModel(model)

            height = self.ui.listView.sizeHintForRow(0) * len(nombres_alumnos)
            self.ui.listView.setMinimumSize(self.ui.listView.width(), height)
            #Awqui es para que me cambie el tamano pero no funciono
            self.ui.page_compus.setMinimumSize(self.ui.page_compus.width(), height)
        else:
            self.ui.listView.setModel(None)


def main():
    app = QApplication(sys.argv)
    ventana = MiVentana()
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
