#!/usr/bin/env python3


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType


import sys
from os import path
import os
import shutil
import sqlite3
from functools import partial
import webbrowser

MAIN, _ = loadUiType(path.join(path.dirname(__file__), "unt2.ui"))




class MainApp(QMainWindow , MAIN):
    def __init__(self,parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.show_data()
        self.handel_tools()
        self.handel_buttons()
        self.handel_UI()
        
        

    def handel_UI(self):
        self.setWindowIcon(QIcon("icons programe/ToolsGUI.png"))
        self.setWindowTitle("ToolsGUI")
        self.setFixedSize(730, 465)
        self.setGeometry(300, 200, 730, 520)
        self.statusBar().showMessage("ToolsGUI Creat By Saladi Ayoubi Version 0.001")




    def handel_buttons(self):
        self.Button_refrech.clicked.connect(self.handel_refresh_widget)
        self.Button_add.clicked.connect(self.handel_import)
        self.Button_close.clicked.connect(self.close)
        self.Button_seting.clicked.connect(self.handel_siteng_show)
 
        # Buttons Connct Widget Suteng 
        self.back_siteng.clicked.connect(self.handel_refresh_widget)
        self.reset.clicked.connect(self.handel_reset_programme)
        
        # Buttons Connect style Sheet
        self.S_Origenal.clicked.connect(self.style_origenal)
        self.S_Adaptic.clicked.connect(self.style_adaptic)
        self.S_Amoled.clicked.connect(self.style_amoled)
        self.S_Dark.clicked.connect(self.style_dark)
        self.S_Light.clicked.connect(self.style_light)

        # Buttons open Link adriss porogrammer
        self.tool_fb.clicked.connect(self.My_Facbook)
        self.tool_git.clicked.connect(self.My_Github)



    # Buttons window  tooles
    def handel_refresh_widget(self):
        self.show_data()
        self.handel_tools()
        self.stackedWidget.setCurrentIndex(0)



    def handel_commands(self , id):
        path = db_paths[id]
        path = f'cd "{path}" &&'
        command = db_commands[id]
        os.system("gnome-terminal -e 'bash -c \""+path+command+";bash\"'")
        print(path)
        

    # funcion get data from file db/toolsGUI.db
    def show_data(self):
        global db_id , db_names , db_icons , db_paths , db_commands
        db = sqlite3.connect("db/toolsGUI.db")
        cr = db.cursor()
        cr.execute("create table if not exists tools (id integer, name text, icon image, path texe, commande text)")
        show = cr.execute("select * from tools")

        db_id = []
        db_names = []
        db_icons = []
        db_paths =[]
        db_commands = []
        for raw in show:
            db_id.append(raw[0])
            db_names.append(raw[1])
            db_icons.append(raw[2])
            db_paths.append(raw[3])
            db_commands.append(raw[4])
        db.commit()
        db.close()
        print("data base close ")



    # functoin created Buttons from tools 
    def handel_tools(self):
        global button

        self.widget = QWidget()             
        self.grid = QGridLayout()

        # get list icons to tools  
        if not os.path.exists("IMG"):
            os.mkdir("IMG")

        icons = os.listdir("IMG")
        icons.sort(key=lambda x: x.zfill(9))

        #list Buttons Tools
        button = icons.copy()

        positions = [(i , j) for i in range(int(len(db_id)/5+1)) for j in range(5)]
        print(" positions :"+str(positions ))
        for id , posit , value , icon in zip(db_id , positions , db_names , icons):
                if value == '':
                        continue

            
                button[id] = QToolButton()
                    
                button[id].setIcon(QIcon("IMG/"+icon))
                button[id].setIconSize(QSize(75,75))
                button[id].setToolTip(str(value))  

                button[id].clicked.connect(partial(self.handel_commands , id))
                self.grid.addWidget(button[id] , *posit)
        
        
        self.widget.setLayout(self.grid)
        self.scrollArea.setWidget(self.widget)
        


    # function show widget sitenge 
    def handel_siteng_show(self):
        self.stackedWidget.setCurrentIndex(1)

    # function reset program and delet data 
    def handel_reset_programme(self):
        ret = QMessageBox.question(self, 'Warning', " Are you sure to delete the data ?", QMessageBox.Yes | QMessageBox.Cancel)
        if ret == QMessageBox.Yes:
            shutil.rmtree("IMG")
            os.remove("db/toolsGUI.db")






    # add style sheet in data base 
    def style_origenal(self):
        style = "Style/origenal.qss"
        handel_save_stylesheet(0 , style )
        QMessageBox.information(None , "Save Style Dheet", "save succeeded reboot programme")

    
    # add style sheet in data base 
    def style_adaptic(self):
        style = "Style/adaptic.qss"
        handel_save_stylesheet(0 , style)
        QMessageBox.information(None , "Save Style Dheet", "save succeeded reboot programme")


    # add style sheet in data base 
    def style_amoled(self):
        style = "Style/amoled.qss"
        handel_save_stylesheet(0 , style)
        QMessageBox.information(None , "Save Style Dheet", "save succeeded reboot programme")
    

    # add style sheet in data base 
    def style_dark(self):
        style = "Style/dark.qss"
        handel_save_stylesheet(0 , style)
        QMessageBox.information(None , "Save Style Dheet", "save succeeded reboot programme")



    
    # add style sheet in data base 
    def style_light(self):
        style = "Style/light.qss"
        handel_save_stylesheet(0 , style)
        QMessageBox.information(None , "Save Style Dheet", "save succeeded reboot programme")
 





    # Function open my facebook 
    def My_Facbook(self):
        webbrowser.open_new("https://www.facebook.com/sami.rabih.925/")



    # Function open My_Github
    def My_Github(self):
        webbrowser.open_new("https://github.com/SalahdinAyoubi")


        
    # this is window with import tool  
    def handel_import(self):
        global win , icon , lpath , name_tool , lcmd
        win = QWidget()
        fbox = QFormLayout()
        win.setStyleSheet("background-color: rgb(85, 87, 83);")

        # Buttond Window import files
        icon = QToolButton()
        icon.setIcon(QIcon("icons programe/add.png"))
        icon.setIconSize(QSize(75,75))
        icon.setFixedSize(75, 75)
        name_tool = QLineEdit()
        name_tool.setPlaceholderText("  Craet Name Tool")


        get_file = QPushButton("Path Folder Tool")
        lpath = QLineEdit()
        lpath.setPlaceholderText("   Enter path Tool")

        lcmd  = QLineEdit()
        lcmd.setPlaceholderText("  Enter Command Terminal ")

        label_cmd = QLabel("Command")
        save , cancel = QPushButton("Save"),QPushButton("Cancel")
        
        # layout window import files
        fbox.addRow(icon , name_tool)
        fbox.addRow(get_file , lpath)
        fbox.addRow(label_cmd , lcmd)
        fbox.addRow(save , cancel)

        win.setLayout(fbox)
        win.setWindowTitle("Add Tool")
        win.setFixedSize(500, 250)
        win.move(500 , 250)
        win.setStyleSheet("QToolTip { color: #ffffff; background-color: #000000; border: 0px; }")
        win.show()

        # command window import file and save  
        cancel.clicked.connect(win.close)
        icon.clicked.connect(get_image_file)
        get_file.clicked.connect(save_path_tool)
        save.clicked.connect(save_data_tool)


# get image for tool with window add tools
def get_image_file(self):
    global path_icon
    path_icon = QFileDialog.getOpenFileName()
    icon.setIcon(QIcon(path_icon[0])) 
   


def save_path_tool(self):
    save = QFileDialog.getExistingDirectory(None, "select Download Diroctory")
    lpath.setText(save)


def save_data_tool(self):
    if not os.path.exists("IMG"):
        os.mkdir("IMG")


    name = name_tool.text()
    IMG = os.listdir("IMG")
    cp_icon = len(IMG)
    

    path_tool = lpath.text()
    cmd = lcmd.text()

    if name == "" or path_tool == "" or cmd == "":
        win.close()
        QMessageBox.information(None, "Save  Error", "Save failed !!, please enter correct data")
        

    else:
        shutil.copyfile(str(path_icon[0]) , f"IMG/{cp_icon}.png")
        hanfel_save_database(cp_icon , name , f"IMG/{cp_icon}.png" , path_tool , cmd)
        win.close()
        QMessageBox.information(None , "Data Save Complete", "Data save succeeded")
    
        
        
           


# funcion save tool data bade and regestre 
def hanfel_save_database(id, name, image, path, commande):
    db = sqlite3.connect("db/toolsGUI.db")
    cr = db.cursor()
    cr.execute("create table if not exists tools (id integer, name text, icon image, path texe, commande text)")
    cr.execute("insert into tools (id, name, icon, path, commande) values(?,?,?,?,?)",(id, name, image, path, commande))
    db.commit()
    db.close()



def handel_save_stylesheet(id , style):
    db = sqlite3.connect("db/StyleSheet.db")
    cr = db.cursor()
    cr.execute("create table if not exists stylesheet (id int, style text)")
    cr.execute("delete from stylesheet where id=0")
    cr.execute("insert into stylesheet (id , style ) values(?,?)" , (id , style))   
    db.commit()
    db.close()


def main():
    app = QApplication(sys.argv)
    window = MainApp()

    db = sqlite3.connect("db/StyleSheet.db")
    cr = db.cursor()
    show = cr.execute("select * from stylesheet")
    for raw in show:
        style = raw[1]
    db.commit()
    db.close()

    # set stylesheet
    file = QFile(str(style))
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

    window.show()
    app.exec_()


if __name__== "__main__":
    main()