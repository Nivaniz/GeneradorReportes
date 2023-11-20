from PySide6 import QtWidgets, QtCore
from ui_monitor import Ui_MainWindow
from functools import partial
from helpers import absPath
import os
import random
import pyqtgraph as pg
import pyqtgraph.exporters
import pandas as pd
import jinja2
import pdfkit  # Linux: sudo apt-get install wkhtmltopdf
# Windows: https://wkhtmltopdf.org/downloads.html#stable (Descargar y guardar en variables del sistema agregando \bin)
# Reiniciar VSCODE
import webbrowser


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Lista de diccionarios que contiene información sobre los valores y su representación en el gráfico.
        self.valores = [
            {"nombre": "Valor 1", "valores": [], "color": "r", "simbolo": "o"},
            {"nombre": "Valor 2", "valores": [], "color": "b", "simbolo": "o"},
            {"nombre": "Valor 3", "valores": [], "color": "g", "simbolo": "o"},
            {"nombre": "Valor 4", "valores": [], "color": "y", "simbolo": "o"},
        ]

        # Agregar nombres de valores al ComboBox en la interfaz gráfica.
        for valor in self.valores:
            self.comboBox.addItem(valor["nombre"])

        # Configuración inicial del gráfico.
        self.construirGrafico()

        # Configuración estática de la tabla.
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setRowCount(len(self.valores))
        self.tableWidget.setVerticalHeaderLabels([valor["nombre"] for valor in self.valores])

        # Conectar botones a funciones correspondientes.
        self.pushButton.clicked.connect(self.AgregarTemperatura)
        self.pushButton_2.clicked.connect(partial(self.AgregarTemperatura, True))
        self.pushButton_3.clicked.connect(partial(self.generarReporte))
        self.pushButton_4.clicked.connect(partial(self.exportarPDF))


    def construirGrafico(self):
        # Configuración inicial del gráfico con PyqtGraph.
        self.widget.addLegend()
        self.widget.setBackground("w")
        self.graficos = []
        for valor in self.valores:
            plot = self.widget.plot(valor["valores"], name=valor["nombre"],
                                    pen=pg.mkPen(valor["color"], width=3),
                                    symbol=valor["simbolo"],
                                    symbolBrush=valor["color"], symbolSize=12)
            self.graficos.append(plot)

        self.widget.showGrid(x=True, y=True)
        self.widget.setYRange(-40, 60)
        self.widget.setTitle("Reporte de Temperaturas", size="20px")
        styles = {"color": "#000", "font-size": "15px"}
        self.widget.setLabel("left", "Temperaturas (ºC)", **styles)
        self.widget.setLabel("bottom", "Horas (H)", **styles)


    def AgregarTemperatura(self, autogenerar=False):
        # Función para agregar temperaturas al gráfico y la tabla.
        if not autogenerar:
            indice = self.comboBox.currentIndex()
            temperatura = self.spinBox.value()
            self.valores[indice]["valores"].append(temperatura)
            self.graficos[indice].setData(self.valores[indice]["valores"])
        else:
            for indice, valor in enumerate(self.valores):
                temperatura = random.randint(-20, 50)
                valor["valores"].append(temperatura)
                self.graficos[indice].setData(valor["valores"])

        self.dibujarTabla()


    def dibujarTabla(self):
        # Función para actualizar la tabla con los datos actuales.
        n_columnas = max([len(valor["valores"]) for valor in self.valores])
        self.tableWidget.setColumnCount(n_columnas)
        self.tableWidget.setHorizontalHeaderLabels([f"{h}" for h in range(0, n_columnas)])
        for i, valor in enumerate(self.valores):
            for j, temp in enumerate(valor["valores"]):
                item = QtWidgets.QTableWidgetItem()
                item.setData(QtCore.Qt.EditRole, temp)
                self.tableWidget.setItem(i, j, item)


    def generarReporte(self):
        # Función para generar un informe HTML y exportar el gráfico como imagen.
        try:
            df = pd.DataFrame([valor["valores"] for valor in self.valores],
                              index=[valor["nombre"] for valor in self.valores])
            env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=absPath('plantillas')))
            template = env.get_template('template.html')
            styler = df.style.applymap(lambda valor: 'color: red' if valor < 0 else 'color: black')
            html = template.render(tabla=styler.to_html())
            # Generamos el HTML
            with open(absPath('reporte.html'), 'w') as f:
                f.write(html)
            self.exportarGraficoComoImagen()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ups", f"Error generando reporte HTML:\n\n{e}")
        else:
            self.statusBar.showMessage("Reporte HTML generado")


    def exportarGraficoComoImagen(self):
        # Función para exportar el gráfico como una imagen PNG.
        try:
            exporter = pg.exporters.ImageExporter(self.widget.plotItem)
            exporter.export(absPath('plot.png'))
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ups", f"Error exportando gráfico como imagen:\n\n{e}")


    def exportarPDF(self):
        # Función para generar un informe PDF y abrirlo con el visor predeterminado.
        self.generarReporte()
        try:
            options = {'enable-local-file-access': None}
            pdfkit.from_file(absPath('reporte.html'), absPath('reporte.pdf'), options=options)
            self.abrirPDFConVisorPredeterminado()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ups", f"Error generando reporte PDF:\n\n{e}")
        else:
            self.statusBar.showMessage("Reporte PDF generado")


    def abrirPDFConVisorPredeterminado(self):
        # Función para abrir el informe PDF con el visor de PDF predeterminado del sistema.
        try:
            webbrowser.open(absPath('reporte.pdf'))
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ups", f"Error abriendo PDF:\n\n{e}")


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    window = MainWindow()
    window.show()
    app.exec()
