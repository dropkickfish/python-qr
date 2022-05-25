# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

import qrcode
from PIL import Image

from csv import reader

from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PySide6.QtCore import QFile, Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap


class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        self.load_ui()

        self.logoButton = self.findChild(QPushButton, 'logoButton')
        self.generateButton = self.findChild(QPushButton, 'generateButton')
        self.importButton = self.findChild(QPushButton, 'importButton')
        self.outputButton = self.findChild(QPushButton, 'outputButton')

        self.logoPreview = self.findChild(QLabel, 'logoPreview')
        self.qrPreview = self.findChild(QLabel, 'qrPreview')

        self.loadedItems = self.findChild(QTableWidget, 'loadedItems')

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

def logo_clicked(self):
    print("Logo clicked")
    fileName = QFileDialog.getOpenFileName(None, 'Import Image', '', 'Image Files (*.png)')
    if fileName:
        print(fileName[0])
    global logoFile
    logoFile=fileName[0]
    logo = QPixmap(fileName[0])
    widget.logoPreview.setPixmap(logo.scaled(widget.logoPreview.size(), Qt.KeepAspectRatio))
    generatePreview(fileName[0])
        
def generate_clicked(self):
    print("Generate clicked")
    generate(csvFile, logoFile)
        
def import_clicked(self):
    print("Import clicked")
    fileName = QFileDialog.getOpenFileName(None, 'Import CSV', '', 'CSV Files (*.csv)')
    if fileName:
        print(fileName[0])
    global csvFile
    csvFile=fileName[0]
    createTable(self, csvFile)
        
def output_clicked(self):
    print("Output clicked")
    directoryName = QFileDialog.getExistingDirectory(None, 'Select Directory', '', QFileDialog.ShowDirsOnly)
    if directoryName:
        print(directoryName)
    global outputDir
    outputDir = directoryName

def createTable(self, csv):
        
        table = widget.loadedItems
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(['Name', 'URL'])
        with open(csv, 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            table.setRowCount(len(list(csv_reader)))
        
        
        with open(csv, 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            # Iterate over each row in the csv using reader object
            i = 0
            for row in csv_reader:
                # row variable is a list that represents a row in csv    
                print(row)
                name = QTableWidgetItem()
                url = QTableWidgetItem()
                name.setData(Qt.DisplayRole, row[0])
                url.setData(Qt.DisplayRole, row[1])
                table.setItem(i, 0, name)
                table.setItem(i, 1, url)
                i += 1
        
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)



def generatePreview(logoLink, url = 'https://www.larking-gowen.co.uk/'):
    logo = Image.open(logoLink)

    # taking base width
    basewidth = 100

    # adjust image size
    wpercent = (basewidth/float(logo.size[0]))
    hsize = int((float(logo.size[1])*float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )   

    # adding URL or text to QRcode
    QRcode.add_data(url)

    # generating QR code
    QRcode.make()

    # taking color name from user
    QRcolor = (33, 106, 124)

    # adding color to QR code
    QRimg = QRcode.make_image(
        fill_color=QRcolor, back_color="white").convert('RGB')

    # set size of QR code
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
        (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)

    # save the QR code generated
    QRimg.save('temp.png')

    logo = QPixmap('temp.png')
    widget.qrPreview.setPixmap(logo.scaled(widget.logoPreview.size(), Qt.KeepAspectRatio))

    print('QR code generated!')

def generateQRCodes(logoLink, name, url, output):
    logo = Image.open(logoLink)

    # taking base width
    basewidth = 100

    # adjust image size
    wpercent = (basewidth/float(logo.size[0]))
    hsize = int((float(logo.size[1])*float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )   

    # adding URL or text to QRcode
    QRcode.add_data(url)

    # generating QR code
    QRcode.make()

    # taking color name from user
    QRcolor = (33, 106, 124)

    # adding color to QR code
    QRimg = QRcode.make_image(
        fill_color=QRcolor, back_color="white").convert('RGB')

    # set size of QR code
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
        (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)

    # save the QR code generated
    print(output+'/'+name+'.png')
    QRimg.save(output+'/'+name+'.png')
    
    print('QR code generated!')

def generate(csv, logoLink): 
    i = 0
    with open(csv, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            # row variable is a list that represents a row in csv
            generateQRCodes(logoLink, row[0], row[1], outputDir)
            i += 1
    i = str(i)
    msgBox = QMessageBox()
    print("Success! "+ i + " QR codes generated in "+ outputDir)
    msgBox.setText("Success! "+ i + "QR codes generated in "+ outputDir)
    msgBox.exec();    
        

if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()

    widget.logoButton.clicked.connect(logo_clicked)
    widget.generateButton.clicked.connect(generate_clicked)
    widget.importButton.clicked.connect(import_clicked)
    widget.outputButton.clicked.connect(output_clicked)

    widget.show()
    sys.exit(app.exec_())
