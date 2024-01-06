import sys
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTextEdit,QSizePolicy
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image
from PyQt5.QtWidgets import QSlider
#import scipy.signal as signal
from scipy.signal import find_peaks
from matplotlib.figure import Figure
from PyQt5.QtGui import QFont
#from docx import Document
#from docx.shared import Inches



class MainWindow(QMainWindow):
    story = []
    story2 = []
    patient_story = []
    count = 0
    count1 = 0
    stiffness_improvement = 0
    lbl1 = ''
    lbl2 = ''
    lbl3 = ''
    chrtlbl1 = ''
    chrtlbl2 = ''
    chrtlbl3 = ''
    tvc = 0
    stfnss = []
    rom1 = 0
    rom2 = 0
    rom3 = 0
    mvctrialscounter = 0
    mvctrialscounter2=0
    mvctrialscounter3 =0
    voltrialscounter=0
    voltrialscounter2=0
    voltrialscounter3=0
    def __init__(self):
        super().__init__()
        self.i=0
        self.points = []
        self.patient_name = ""
        self.x_offset = 0
        self.y_offset = 0
        self.x_offset2 = 0
        self.y_offset2 = 0
        self.x_offset3 = 0
        self.y_offset3 = 0
        self.mvc_offset = 0
        self.mvc_offset2 = 0
        self.mvc_offset3 = 0
        
        self.lbl1 = 'pre'
        self.lbl2 = 'post'
        self.lbl3 = 'long'
        
        self.chrtlbl1 = 'Before'
        self.chrtlbl2 = 'After 1 session'
        self.chrtlbl3 = 'After 10 session'
        
        self.stfnss = []
        
        self.setWindowTitle("Data Analysis")
        self.setGeometry(100, 100, 1200, 800)

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)  
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        #chart_box = QWidget()
        #chart_layout = QVBoxLayout()
        #chart_layout.setContentsMargins(1, 1, 1, 1) 

        name_label = QLabel("Patient Name:")
        self.name_input = QLineEdit()
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.save_patient_name)
        self.switch_button = QPushButton("Change to long-term")
        self.switch_button.setCheckable(True)
        self.switch_button.clicked.connect(self.changetolongterm)
        name_layout = QHBoxLayout()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        name_layout.addWidget(self.confirm_button)
        name_layout.addWidget(self.switch_button)
        main_layout.addLayout(name_layout)
        

        data_title_layout = QHBoxLayout()
        data_input_layout = QHBoxLayout()
        self.data_label = QLabel("Enter the path of the dataset1 considered as pre:")
        self.dir_input = QLineEdit()
        self.data_label3 = QLabel("Enter the path of the dataset2 considered as post:")
        self.dir_input3 = QLineEdit()
        self.data_label2 = QLabel("Enter the path of the dataset3 considered as long:")
        self.dir_input2 = QLineEdit()
        plot_button2 = QPushButton("Set")
        plot_button2.clicked.connect(self.upload_data)
        data_title_layout.addWidget(self.data_label)
        data_input_layout.addWidget(self.dir_input)
        data_title_layout.addWidget(self.data_label3)
        data_input_layout.addWidget(self.dir_input3)
        data_title_layout.addWidget(self.data_label2)
        data_input_layout.addWidget(self.dir_input2)
        
        main_layout.addLayout(data_title_layout)
        main_layout.addLayout(data_input_layout)
        
        main_layout.addWidget(plot_button2)
        #chart_layout.addWidget(chart_box)
        #main_layout.addLayout(chart_layout, stretch=20)
        
        
        # Create a horizontal layout to hold the two columns
        main_layout2 = QHBoxLayout()
        # Create the first column (left column) with a QVBoxLayout
        left_column_layout = QVBoxLayout()
        
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas.setMaximumHeight(400)  # Set the maximum height you desire
        self.canvas.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        left_column_layout.addWidget(self.canvas)

        # Create the second column (right column) with a QVBoxLayout
        right_column_layout = QVBoxLayout()
        button_names = ["TV 5", "TV 50", "TV 100", "TV 120", "MVC", "Voluntary", "ROM" ,"ChangeCycle"]
        self.buttons = []
        
        for name in button_names:
            if name == "MVC" :
                font = QFont()
                font.setFamily('Calibri Light')
                font.setPointSize(9)
                button = QPushButton(name)
                button.clicked.connect(self.plot_chart)
                right_column_layout.addWidget(button)
                self.buttons.append(button)
                mvc_trials_changing_layout = QHBoxLayout()
                mvc_trials_changing_button_names = ['1▶️' , '2▶️' , '3▶️']
                for i in mvc_trials_changing_button_names:
                    bttn = QPushButton(i)
                    bttn.setFixedSize(30, 25)
                    bttn.setFont(font)
                    bttn.clicked.connect(self.plot_chart)
                    mvc_trials_changing_layout.addWidget(bttn)
                    self.buttons.append(bttn)
                right_column_layout.addLayout(mvc_trials_changing_layout)
                
                mvc_reversing_layout = QHBoxLayout()
                mvc_reversing_names = ['R1' , 'R2' , 'R3']
                for i in mvc_reversing_names:
                    bttn = QPushButton(i)
                    bttn.clicked.connect(self.plot_chart)
                    bttn.setCheckable(True)
                    #bttn.toggle()
                    bttn.setFixedSize(30, 25)
                    bttn.setFont(font)
                    mvc_reversing_layout.addWidget(bttn)
                    self.buttons.append(bttn)
                right_column_layout.addLayout(mvc_reversing_layout)
                
            elif name == "Voluntary" :
                button = QPushButton(name)
                button.clicked.connect(self.plot_chart)
                right_column_layout.addWidget(button)
                self.buttons.append(button)
                vol_trials_changing_layout = QHBoxLayout()
                vol_trials_changing_button_names = ['V1▶️' , 'V2▶️' , 'V3▶️']
                for i in vol_trials_changing_button_names:
                    bttnvl = QPushButton(i)
                    bttnvl.clicked.connect(self.plot_chart)
                    bttnvl.setFixedSize(30, 25)
                    bttnvl.setFont(font)
                    vol_trials_changing_layout.addWidget(bttnvl)
                    self.buttons.append(bttnvl)
                right_column_layout.addLayout(vol_trials_changing_layout) 
            else:
                button = QPushButton(name)
                button.clicked.connect(self.plot_chart)
                right_column_layout.addWidget(button)
                self.buttons.append(button)
            
        # self.buttons[7].setCheckable(True)
        # self.buttons[7].toggle()
        
        # self.buttons[8].setCheckable(True)
        # self.buttons[8].toggle()
        
        # self.buttons[9].setCheckable(True)
        # self.buttons[9].toggle()

          # Add the left and right columns to the main horizontal layout    
        main_layout2.addLayout(left_column_layout, 4)  # Set the left layout's stretch factor to 4
        main_layout2.addLayout(right_column_layout)  # The right layout's stretch factor defaults to 1

        # Set different space allocations for the columns
        left_column_layout.setContentsMargins(1, 1, 1, 1)
        right_column_layout.setContentsMargins(1, 1, 1, 1)
        main_layout.addLayout(main_layout2)


        # Create sliders
        self.x_slider = QSlider(Qt.Horizontal)
        self.y_slider = QSlider(Qt.Horizontal)
        self.x_slider2 = QSlider(Qt.Horizontal)
        self.y_slider2 = QSlider(Qt.Horizontal)
        self.x_slider3 = QSlider(Qt.Horizontal)
        self.y_slider3 = QSlider(Qt.Horizontal)
        self.mvc_slider = QSlider(Qt.Horizontal)
        self.mvc_slider2 = QSlider(Qt.Horizontal)
        self.mvc_slider3 = QSlider(Qt.Horizontal)
        
        # self.x_slider.setSingleStep(0.5)
        # self.x_slider3.setSingleStep(0.5)
        # self.x_slider3.setSingleStep(0.5)
        # self.y_slider.setSingleStep(0.5)
        # self.y_slider2.setSingleStep(0.5)
        # self.y_slider3.setSingleStep(0.5)
        
        self.x_slider.setMinimum(-60)
        self.x_slider.setMaximum(60)
        self.x_slider.setValue(0)  # Initial value

        self.y_slider.setMinimum(-60)
        self.y_slider.setMaximum(60)
        self.y_slider.setValue(0)  # Initial value
        
        self.x_slider2.setMinimum(-60)
        self.x_slider2.setMaximum(60)
        self.x_slider2.setValue(0)  # Initial value

        self.y_slider2.setMinimum(-60)
        self.y_slider2.setMaximum(60)
        self.y_slider2.setValue(0)  # Initial value
        
        self.x_slider3.setMinimum(-60)
        self.x_slider3.setMaximum(60)
        self.x_slider3.setValue(0)  # Initial value

        self.y_slider3.setMinimum(-60)
        self.y_slider3.setMaximum(60)
        self.y_slider3.setValue(0)  # Initial value
        
        self.mvc_slider3.setMinimum(-60)
        self.mvc_slider3.setMaximum(60)
        self.mvc_slider3.setValue(0)
        
        self.mvc_slider.setMinimum(-60)
        self.mvc_slider.setMaximum(60)
        self.mvc_slider.setValue(0)
        
        self.mvc_slider2.setMinimum(-60)
        self.mvc_slider2.setMaximum(60)
        self.mvc_slider2.setValue(0)
        
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.x_slider)
        slider_layout.addWidget(self.y_slider)
        slider_layout.addWidget(self.x_slider2)
        slider_layout.addWidget(self.y_slider2)
        slider_layout.addWidget(self.x_slider3)
        slider_layout.addWidget(self.y_slider3)
        slider_layout.addWidget(self.mvc_slider)
        slider_layout.addWidget(self.mvc_slider2)
        slider_layout.addWidget(self.mvc_slider3)
        
        slider_labelx = QLabel("X1")
        slider_labely = QLabel("Y1")
        slider_labelx2 = QLabel("X3")
        slider_labely2 = QLabel("Y3")
        slider_labelx3 = QLabel("X2")
        slider_labely3 = QLabel("Y2")
        slider_labelmvc = QLabel("mvc1")
        slider_labelmvc2 = QLabel("mvc2")
        slider_labelmvc3 = QLabel("mvc3")
        slider_label_layout = QHBoxLayout()
        slider_label_layout.addWidget(slider_labelx)
        slider_label_layout.addWidget(slider_labely)
        slider_label_layout.addWidget(slider_labelx3)
        slider_label_layout.addWidget(slider_labely3)
        slider_label_layout.addWidget(slider_labelx2)
        slider_label_layout.addWidget(slider_labely2)
        
        slider_label_layout.addWidget(slider_labelmvc)
        slider_label_layout.addWidget(slider_labelmvc2)
        slider_label_layout.addWidget(slider_labelmvc3)
        main_layout.addLayout(slider_label_layout)
        main_layout.addLayout(slider_layout)
        self.x_slider.valueChanged.connect(self.update_x_offset)
        self.y_slider.valueChanged.connect(self.update_y_offset)
        self.x_slider2.valueChanged.connect(self.update_x_offset2)
        self.y_slider2.valueChanged.connect(self.update_y_offset2)
        self.x_slider3.valueChanged.connect(self.update_x_offset3)
        self.y_slider3.valueChanged.connect(self.update_y_offset3)
        self.mvc_slider.valueChanged.connect(self.update_mvc_offset)
        self.mvc_slider2.valueChanged.connect(self.update_mvc_offset2)
        self.mvc_slider3.valueChanged.connect(self.update_mvc_offset3)
        
        self.x_slider.setTickPosition(QSlider.TicksBelow)
        self.x_slider.setTickInterval(5)
        self.y_slider.setTickPosition(QSlider.TicksBelow)
        self.y_slider.setTickInterval(5)
        self.x_slider2.setTickPosition(QSlider.TicksBelow)
        self.x_slider2.setTickInterval(5)
        self.y_slider2.setTickPosition(QSlider.TicksBelow)
        self.y_slider2.setTickInterval(5) 
        self.x_slider3.setTickPosition(QSlider.TicksBelow)
        self.x_slider3.setTickInterval(5)
        self.y_slider3.setTickPosition(QSlider.TicksBelow)
        self.y_slider3.setTickInterval(5)
        self.mvc_slider.setTickPosition(QSlider.TicksBelow)
        self.mvc_slider.setTickInterval(5)
        self.mvc_slider2.setTickPosition(QSlider.TicksBelow)
        self.mvc_slider2.setTickInterval(5)
        self.mvc_slider3.setTickPosition(QSlider.TicksBelow)
        self.mvc_slider3.setTickInterval(5)

        
        pdf_button_layout = QHBoxLayout()
        left_column_layout2 = QVBoxLayout()
        right_column_layout2 = QVBoxLayout()
        
        # Add a QPushButton for saving to PDF
        save_button = QPushButton("Save to PDF")
        save_button.clicked.connect(self.save_to_pdf)
        main_layout.addWidget(save_button)
              
        # Add QTextEdit for chart description
        comment_label = QLabel("Comment:")
        main_layout.addWidget(comment_label)
        self.chart_description_box = QLineEdit()
        self.chart_description_box.setReadOnly(True)  # Make it read-only
        main_layout.addWidget(self.chart_description_box)
        
        # Add QTextEdit for description
        description = QLabel("Description:")
        self.description_input = QTextEdit()
        self.description_input.setMaximumHeight(130)  # Set the maximum height you desire
        self.description_input.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        plot_button_description = QPushButton("Add Description")
        plot_button_description.clicked.connect(self.description)
        main_layout.addWidget(description)
        right_column_layout2.addWidget(self.description_input)
        left_column_layout2.addWidget(plot_button_description)
        
        # Create the "Generate Report" button
        generate_report_button = QPushButton("Manual Report")
        generate_report_button.clicked.connect(self.generate_report)
        left_column_layout2.addWidget(generate_report_button)
        generate_patient_report_button = QPushButton("Patient Report")
        generate_patient_report_button.clicked.connect(self.generate_patient_report)
        left_column_layout2.addWidget(generate_patient_report_button)
        generate_manual_patient_report_button = QPushButton("Manual Patient Report")
        generate_manual_patient_report_button.clicked.connect(self.open_patient_report_window)
        left_column_layout2.addWidget(generate_manual_patient_report_button)
        
        pdf_button_layout.addLayout(right_column_layout2,4)  # The right layout's stretch factor defaults to 1
        pdf_button_layout.addLayout(left_column_layout2)  # Set the left layout's stretch factor to 4
        
        left_column_layout2.setContentsMargins(1, 1, 1, 1)
        right_column_layout2.setContentsMargins(1, 1, 1, 1)
        main_layout.addLayout(pdf_button_layout)
    
    def open_patient_report_window(self):
        self.main_widget = QWidget()
        self.main_widget.setWindowTitle("Manual Report")
        pmain_layout = QVBoxLayout(self.main_widget)
        #self.setWindowTitle("Manual Patient Report")
        pmain_layout.setContentsMargins(15, 15, 15, 15)  

        patient_report_container = QWidget()
        main_patient_report_layout = QVBoxLayout(patient_report_container)
        
        format_label =  QLabel("Please enter your data in the format: [pre , post/long1 , After/long2]")
        format_label_piechart =  QLabel("Please enter your references in the format: [DF ROM , PF ROM , PROM , Stiffness, DF MVC ,PF MVC,  AROM , Speed ]")
        
        main_patient_report_layout.addWidget(format_label)
        
        dfrom_label = QLabel("Dorsiflexion:")
        self.dfrom_box = QLineEdit()
        main_patient_report_layout.addWidget(dfrom_label)
        main_patient_report_layout.addWidget(self.dfrom_box)
        
        
        pfrom_label = QLabel("Plantarflexion:")
        self.pfrom_box = QLineEdit()
        main_patient_report_layout.addWidget(pfrom_label)
        main_patient_report_layout.addWidget(self.pfrom_box)
        
        
        rom_label = QLabel("Passive ROM:")
        self.rom_box = QLineEdit()
        main_patient_report_layout.addWidget(rom_label)
        main_patient_report_layout.addWidget(self.rom_box)
       
        
        stiffness_label = QLabel("Stiffness:")
        self.stiffness_box = QLineEdit()
        main_patient_report_layout.addWidget(stiffness_label)
        main_patient_report_layout.addWidget(self.stiffness_box)
        
        
        mvcp_label = QLabel("MVC plantar:")
        self.mvcp_box = QLineEdit()
        main_patient_report_layout.addWidget(mvcp_label)
        main_patient_report_layout.addWidget(self.mvcp_box)
        
        
        mvcd_label = QLabel("MVC dorsi:")
        self.mvcd_box = QLineEdit()
        main_patient_report_layout.addWidget(mvcd_label)
        main_patient_report_layout.addWidget(self.mvcd_box)
        
        
        arom_label = QLabel("Active ROM:")
        self.arom_box = QLineEdit()
        main_patient_report_layout.addWidget(arom_label)
        main_patient_report_layout.addWidget(self.arom_box)
        
        
        speed_label = QLabel("Speed:")
        self.speed_box = QLineEdit()
        main_patient_report_layout.addWidget(speed_label)
        main_patient_report_layout.addWidget(self.speed_box)
        
        main_patient_report_layout.addWidget(format_label_piechart)
        
        references_label = QLabel("References:")
        self.references_box = QLineEdit()
        main_patient_report_layout.addWidget(references_label)
        main_patient_report_layout.addWidget(self.references_box)
        self.references_box.setText("[24.8,62.1,86.9,100,20,50,70.5,300]")
    
        gnrte_patient_report_button = QPushButton("Generate PDF")
        gnrte_patient_report_button.clicked.connect(self.plot_chart_patient_report_manual)
        main_patient_report_layout.addWidget(gnrte_patient_report_button)
        
        pmain_layout.addWidget(patient_report_container)
        
        self.main_widget.show()
        
    def plot_chart_patient_report_manual(self):
        pdf_filename = self.patient_name
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        styles = getSampleStyleSheet()
        if self.count1 == 0 :
            title = Paragraph(self.patient_name, styles['Title'])
            self.patient_story.append(title)
            
        pspeed_str = self.speed_box.text()
        self.pspeed = [float(x) for x in pspeed_str.strip('[]').split(',')]
        pAROM_str = self.arom_box.text()
        self.pAROM = [float(x) for x in pAROM_str.strip('[]').split(',')]
        pmvcd_str = self.mvcd_box.text()
        self.pmvcd = [float(x) for x in pmvcd_str.strip('[]').split(',')]
        pmvcp_str = self.mvcp_box.text()
        self.pmvcp = [float(x) for x in pmvcp_str.strip('[]').split(',')]
        pstiffness_str = self.stiffness_box.text()
        self.pstiffness = [float(x) for x in pstiffness_str.strip('[]').split(',')]
        rom_str = self.rom_box.text()
        self.rom = [float(x) for x in rom_str.strip('[]').split(',')]
        pPR_plantar_str = self.pfrom_box.text()
        self.pPR_plantar = [float(x) for x in pPR_plantar_str.strip('[]').split(',')]
        pPR_dorsi_str = self.dfrom_box.text()
        self.pPR_dorsi = [float(x) for x in pPR_dorsi_str.strip('[]').split(',')]
        references_str = self.references_box.text()
        self.references = [float(x) for x in references_str.strip('[]').split(',')]
        
        self.fig.clear()
        passive_parameters = ("DF (Deg)","PF (Deg)", "ROM" ,"Stiffness")
        passive_values = {
             self.chrtlbl1: (round(self.pPR_dorsi[0],1), round(self.pPR_plantar[0],1) , round(self.rom[0],1) , 50*round(self.pstiffness[0],1)),
             self.chrtlbl2: (round(self.pPR_dorsi[1],1), round(self.pPR_plantar[1],1), round(self.rom[1],1), 50*round(self.pstiffness[1],1)),
             self.chrtlbl3: (round(self.pPR_dorsi[2],1), round(self.pPR_plantar[2],1), round(self.rom[2],1) , 50*round(self.pstiffness[2],1)),
        }

        x = np.arange(len(passive_parameters))  # the label locations
        width = 0.15  # the width of the bars
        multiplier = 0

        #fig, ax = plt.subplots(subplot_kw={'constraint': 'tight'})
        ax = self.fig.add_subplot(111)

        for attribute, measurement in passive_values.items():
            offset = width * multiplier
            rects = ax.bar(x + offset, measurement, width, label=attribute)
            #ax.bar_label(rects, padding=3)
            multiplier += 1

         # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_title('Passive Parameters')
        ax.set_xticks(x + width, passive_parameters)
        ax.legend(loc='upper left', ncols=3)
        #ax.set_ylim(0, 250)
        
        
        self.canvas.draw()
        image_filename = f"chart_image1_{self.count1}.png"
        self.fig.savefig(image_filename)
        # Add the image to the PDF
        img = plt.imread(image_filename)
        img_width = 520  # Adjust the image width as needed
        img_height = img_width * img.shape[0] / img.shape[1]
        img_flowable = Image(image_filename, width=img_width, height=img_height)
        self.patient_story.append(img_flowable)
        self.patient_story.append(Spacer(1, 12))
        #self.patient_story.append(Spacer(1, 12))
        self.count1 = self.count1+1
        
        
        
        #ax.clear()
        self.fig.clf()
        self.fig.clear()
        ax1 = self.fig.add_subplot(111)
        active_parameters = ("DF MVC (Nm)","PF MVC (Nm)", "Active ROM (deg)", "Speed (deg/sec)")
        
        #self.mvcd = round(self.mvcd , 2)
        active_values = {
             self.chrtlbl1: (round(self.pmvcd[0], 1) , round(self.pmvcp[0], 1) , round(self.pAROM[0], 1) , round(self.pspeed[0], 1)),
             self.chrtlbl2: (round(self.pmvcd[1], 1) , round(self.pmvcp[1], 1) , round(self.pAROM[1], 1) , round(self.pspeed[1], 1)),
             self.chrtlbl3: (round(self.pmvcd[2], 1) , round(self.pmvcp[2], 1) , round(self.pAROM[2], 1) , round(self.pspeed[2], 1)),
        }

        x = np.arange(len(active_parameters))  # the label locations
        width = 0.15  # the width of the bars
        multiplier = 0

        #fig, ax1 = plt.subplots(layout='constrained')

        for attribute, measurement in active_values.items():
                offset = width * multiplier
                rects = ax1.bar(x + offset, measurement, width, label=attribute)
                #ax1.bar_label(rects, padding=3)
                multiplier += 1

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax1.set_title('Active Parameters')
        #plt.tight_layout() 
        ax1.set_xticks(x + width, active_parameters)
        ax1.legend(loc='upper left', ncols=3)
        #ax1.set_ylim(0, 250)

        #self.fig.clear()
        #self.fig.canvas.draw()
        self.canvas.draw()
        image_filename = f"chart_image1_{self.count1}.png"
        self.fig.savefig(image_filename)
        # Add the image to the PDF
        img = plt.imread(image_filename)
        img_width = 520  # Adjust the image width as needed
        img_height = img_width * img.shape[0] / img.shape[1]
        img_flowable = Image(image_filename, width=img_width, height=img_height)
        self.patient_story.append(img_flowable)
        #self.patient_story.append(Spacer(1, 12))
        self.patient_story.append(Spacer(1, 12))
        self.count1 = self.count1+1
        
        
        self.fig.clf()
        # data_pie for four pie charts
        DF_values_piechart = np.array([round((self.pPR_dorsi[0]/self.references[0])*100 ,2),
              round(((abs(self.pPR_dorsi[1]-self.pPR_dorsi[0]))/self.references[0])*100 ,2),
              round(((abs(self.pPR_dorsi[2]-self.pPR_dorsi[1]))/self.references[0])*100 ,2),
              round(((abs(self.references[0]-self.pPR_dorsi[2]))/self.references[0])*100 ,2)])

        PF_values_piechart = np.array([round((self.pPR_plantar[0]/self.references[1])*100 ,2),
              round(((abs(self.pPR_plantar[1]-self.pPR_plantar[0]))/self.references[1])*100 ,2),
              round(((abs(self.pPR_plantar[2]-self.pPR_plantar[1]))/self.references[1])*100 ,2),
              round(((abs(self.references[1]-self.pPR_plantar[2]))/self.references[1])*100 ,2)])

        ROM_values_piechart = np.array([round((self.rom[0]/self.references[2])*100 ,2),
              round(((abs(self.rom[1]-self.rom[0]))/self.references[2])*100 ,2),
              round(((abs(self.rom[2]-self.rom[1]))/self.references[2])*100 ,2),
              round(((abs(self.references[2]-self.rom[2]))/self.references[2])*100 ,2)])

        stiff_values_piechart = np.array([0,
              round(((abs(self.pstiffness[1]-self.pstiffness[0]))/self.pstiffness[0])*100,2),
              round(((abs(self.pstiffness[2]-self.pstiffness[0]))/self.pstiffness[0])*100,2),
              round(100-((abs(self.pstiffness[2]-self.pstiffness[0]))/self.pstiffness[0])*100 -((abs(self.pstiffness[1]-self.pstiffness[0])/self.pstiffness[0])*100),2)])

        data_pie_passive = [
            DF_values_piechart,
            PF_values_piechart,
            ROM_values_piechart,
            stiff_values_piechart
        ]
        
        print(data_pie_passive)

        #fig, ax = plt.subplots(subplot_kw={'constraint': 'tight'})
        #ax = self.fig.add_subplot(1, 4, figsize=(12, 3), subplot_kw=dict(projection="polar"))
        figpie = self.fig
        #figpie.set_size_inches(12, 3)
        axspie = figpie.subplots(1, 4, subplot_kw=dict(projection="polar"))

        pie_chart_titles_passive = ['DF Improvement' , 'PF Improvement' , 'ROM Improvement' , 'Stiffness Improvement']
        pie_labels = ['Pre' , 'Long1' , 'Long2' , 'Remained']
        size = 0.1  # Width of the pie pieces
        
        for i, ax in enumerate(axspie):
            vals = data_pie_passive[i]
    
            # Normalize vals to 2 pi
            valsnorm = vals / np.sum(vals) * 2 * np.pi
            # Obtain the ordinates of the bar edges
            valsleft = np.cumsum(np.append(0, valsnorm.flatten()[:-1])).reshape(vals.shape)
    
            # Use the tab20c colormap for outer and inner colors
            cmap = plt.colormaps["tab20c"]
            inner_colors = [cmap(i) for i in [3, 1, 9, 20]]
    
            # Set starting angle
            start_angle = 0  # Change this value to set the desired starting angle
    
            ax.bar(x=valsleft.flatten() + np.deg2rad(start_angle),
                   width=valsnorm.flatten(), bottom=0, height=1 - size,
                   color=inner_colors ,edgecolor='w', linewidth=1, align="edge")
    
            # Add labels
            for j, val in enumerate(vals.flatten()):
                print("Index j:", j)  # Add this line for debugging
                print("Current pie_labels:", pie_labels)  # Add this line for debugging
                print("Length of pie_labels:", len(pie_labels))  # Add this line for debugging
                angle = np.deg2rad((valsleft.flatten()[j] + valsnorm.flatten()[j] / 2) * 180 / np.pi + start_angle)
                ax.text(angle, 1.1, f'{pie_labels[j]}: {val}%', ha='center', va='center')
    
            # Set title and turn off axis
            ax.set(title=f"{pie_chart_titles_passive[i]}")
            ax.set_axis_off()

        # Adjust layout for better spacing
        self.fig.tight_layout()
        self.canvas.draw()
        image_filename = f"chart_image1_{self.count1}.png"
        self.fig.savefig(image_filename)
        # Add the image to the PDF
        img = plt.imread(image_filename)
        img_width = 520  # Adjust the image width as needed
        img_height = img_width * img.shape[0] / img.shape[1]
        img_flowable = Image(image_filename, width=img_width, height=img_height)
        self.patient_story.append(img_flowable)
        self.patient_story.append(Spacer(1, 12))
        #self.patient_story.append(Spacer(1, 12))
        self.count1 = self.count1+1
        
        
        self.fig.clf()
        # data_pie for four pie charts
        DF_MVC_values_piechart = np.array([round((self.pmvcd[0]/self.references[4])*100 ,2),
              round(((abs(self.pmvcd[1]-self.pmvcd[0]))/self.references[4])*100 ,2),
              round(((abs(self.pmvcd[2]-self.pmvcd[1]))/self.references[4])*100 ,2),
              round(((abs(self.references[4]-self.pmvcd[2]))/self.references[4])*100 ,2)])

        PF_MVC_values_piechart = np.array([round((self.pmvcp[0]/self.references[5])*100 ,2),
              round(((abs(self.pmvcp[1]-self.pmvcp[0]))/self.references[5])*100 ,2),
              round(((abs(self.pmvcp[2]-self.pmvcp[1]))/self.references[5])*100 ,2),
              round(((abs(self.references[5]-self.pmvcp[2]))/self.references[5])*100 ,2)])

        AROM_values_piechart = np.array([round((self.pAROM[0]/self.references[6])*100 ,2),
              round(((abs(self.pAROM[1]-self.pAROM[0]))/self.references[6])*100 ,2),
              round(((abs(self.pAROM[2]-self.pAROM[1]))/self.references[6])*100 ,2),
              round(((abs(self.references[6]-self.pAROM[2]))/self.references[6])*100 ,2)])

        speed_values_piechart = np.array([round((self.pspeed[0]/self.references[7])*100 ,2),
              round(((abs(self.pspeed[1]-self.pspeed[0]))/self.references[7])*100 ,2),
              round(((abs(self.pspeed[2]-self.pspeed[1]))/self.references[7])*100 ,2),
              round(((abs(self.references[7]-self.pspeed[2]))/self.references[7])*100 ,2)])
        
        data_pie_active = [
            DF_MVC_values_piechart,
            PF_MVC_values_piechart,
            AROM_values_piechart,
            speed_values_piechart
        ]
        
        figpie = self.fig
        #figpie.set_size_inches(12, 3)
        axspie = figpie.subplots(1, 4, subplot_kw=dict(projection="polar"))

        pie_chart_titles_active = ['DF MVC Improvement' , 'PF MVC Improvement' , 'AROM Improvement' , 'Speed Improvement']
        pie_labels = ['Pre' , 'Long1' , 'Long2' , 'Remained']
        size = 0.1  # Width of the pie pieces
        
        for i, ax in enumerate(axspie):
            vals = data_pie_active[i]
    
            # Normalize vals to 2 pi
            valsnorm = vals / np.sum(vals) * 2 * np.pi
            # Obtain the ordinates of the bar edges
            valsleft = np.cumsum(np.append(0, valsnorm.flatten()[:-1])).reshape(vals.shape)
    
            # Set starting angle
            start_angle = 0  # Change this value to set the desired starting angle
    
            ax.bar(x=valsleft.flatten() + np.deg2rad(start_angle),
                   width=valsnorm.flatten(), bottom=0, height=1 - size,
                   color=inner_colors ,edgecolor='w', linewidth=1, align="edge")
    
            # Add labels
            for j, val in enumerate(vals.flatten()):
                angle = np.deg2rad((valsleft.flatten()[j] + valsnorm.flatten()[j] / 2) * 180 / np.pi + start_angle)
                ax.text(angle, 1.1, f'{pie_labels[j]}: {val}%', ha='center', va='center')
    
            # Set title and turn off axis
            ax.set(title=f"{pie_chart_titles_active[i]}")
            ax.set_axis_off()

        # Adjust layout for better spacing
        self.fig.tight_layout()
        self.canvas.draw()
        image_filename = f"chart_image1_{self.count1}.png"
        self.fig.savefig(image_filename)
        # Add the image to the PDF
        img = plt.imread(image_filename)
        img_width = 520  # Adjust the image width as needed
        img_height = img_width * img.shape[0] / img.shape[1]
        img_flowable = Image(image_filename, width=img_width, height=img_height)
        self.patient_story.append(img_flowable)
        self.patient_story.append(Spacer(1, 12))
        #self.patient_story.append(Spacer(1, 12))
        self.count1 = self.count1+1
        
        
        pdf_filename = self.patient_name + "_manualPatientReport.pdf"
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        styles = getSampleStyleSheet()
        if self.count1 == 0 :
            title = Paragraph(self.patient_name, styles['Title'])
            self.patient_story.append(title)
            
        self.patient_story.append(Spacer(1, 12))
        
        #self.plot_chart_patient_report()
        patient_story = self.patient_story
        # Build the PDF
        doc.build(patient_story) 
        
        # Create a Document
        # doc1 = Document()
        # # Add content to the Document
        # for item in self.patient_story:
        #     if isinstance(item, str):
        #         doc1.add_paragraph(item)
        #     elif isinstance(item, str):  # Assuming the image path is stored as a string
        #         doc1.add_picture(item, width=Inches(5)) # Adjust the width as needed
        # # Save the Document
        # doc1.save(self.patient_name + 'patient_story.docx')

        # Inform the user that the PDF has been saved
        info_dialog = QMessageBox(self)
        info_dialog.setIcon(QMessageBox.Information)
        info_dialog.setWindowTitle("Info")
        info_dialog.setText("Patient Report was generated successfully.")
        info_dialog.setStandardButtons(QMessageBox.Ok)
        info_dialog.exec_()
    
    def on_click(self, event):
        
        if event.button == 1:  # Left mouse button
            x, y = event.xdata, event.ydata
            self.description_input.append(f'Clicked at x={x}, y={y}')
            print(f'Clicked at x={x}, y={y}')
            self.points.append((x, y))
            #self.axes.plot(x, y, 'ro')  # 'ro' stands for red dot
            #self.draw()

            # Calculate slope and difference in y-values if there are two points
            
            if len(self.points) >= 2 and len(self.points)%2 == 0:
                
                x1, y1 = self.points[self.i]
                x2, y2 = self.points[self.i+1]
                self.i = self.i + 2
                slope = (y2 - y1) / (x2 - x1)
                diff_y = y2 - y1
                self.description_input.append(f'Slope: {slope}, Difference in y-values: {diff_y}')
                print(f'Slope: {slope}, Difference in y-values: {diff_y}')
                
                
                
    def add_point(self, x, y):
        self.points.append((x, y))
        self.axes.plot(x, y, 'ro')  # 'ro' stands for red dot
        self.draw()
        
    def update_x_offset(self):
        value = self.x_slider.value()
        self.x_offset = value
        print(value)
        self.plot_chart()

    def update_y_offset(self):
        value = self.y_slider.value()
        self.y_offset = value
        self.plot_chart()
        print(value)
        
    def update_x_offset2(self):
        value = self.x_slider2.value()
        self.x_offset2 = value
        self.plot_chart()
        print(value)

    def update_y_offset2(self):
        value = self.y_slider2.value()
        self.y_offset2 = value
        self.plot_chart()
        print(value)

    def update_x_offset3(self):
        value = self.x_slider3.value()
        self.x_offset3 = value
        self.plot_chart()
        print(value)

    def update_y_offset3(self):
        value = self.y_slider3.value()
        self.y_offset3 = value
        self.plot_chart()
        print(value)
        
    def update_mvc_offset(self):
        value = self.mvc_slider.value()
        self.mvc_offset = value
        self.plot_chart()
        print(value)
    
    def update_mvc_offset2(self):
        value = self.mvc_slider2.value()
        self.mvc_offset2 = value
        self.plot_chart()
        print(value)
        
    def update_mvc_offset3(self):
        value = self.mvc_slider3.value()
        self.mvc_offset3 = value
        self.plot_chart()
        print(value)
        
    def changetolongterm(self):
        if self.switch_button.isChecked():
            self.data_label.setText("Enter the path of the dataset1 considered as pre:")
            self.data_label3.setText("Enter the path of the dataset2 considered as long1:")
            self.data_label2.setText("Enter the path of the dataset3 considered as long2:")
            
            self.lbl1 = 'pre'
            self.lbl2 = 'long1'
            self.lbl3 = 'long2'
            
            self.chrtlbl1 = 'Before'
            self.chrtlbl2 = 'After 10 session'
            self.chrtlbl3 = 'After 20 session'
        else:
            self.data_label.setText("Enter the path of the dataset1 considered as pre:")
            self.data_label3.setText("Enter the path of the dataset2 considered as post:")
            self.data_label2.setText("Enter the path of the dataset3 considered as long:")
            
            self.lbl1 = 'pre'
            self.lbl2 = 'post'
            self.lbl3 = 'long'
            
            self.chrtlbl1 = 'Before'
            self.chrtlbl2 = 'After 1 session'
            self.chrtlbl3 = 'After 10 session'
        
    def save_patient_name(self):
        self.patient_name = self.name_input.text()
        self.count = 0
        self.count1 = 0
        print("Patient Name:", self.patient_name)
    
    def description(self):
        if not hasattr(self, 'data1_tv_directory') or not hasattr(self, 'data2_tv_directory') or not hasattr(self, 'data3_tv_directory'):
            # Data is not set, show an error dialog
            error_dialog = QMessageBox(self)
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("Please set the data first.")
            error_dialog.setStandardButtons(QMessageBox.Ok)
            error_dialog.exec_()
            return
        
        if not self.patient_name:
            # Patient name is not confirmed, show an error dialog
            error_dialog = QMessageBox(self)
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("Please confirm the patient name first.")
            error_dialog.setStandardButtons(QMessageBox.Ok)
            error_dialog.exec_()
            return
        
        describ = self.description_input.toPlainText()
        # Replace newline characters with HTML line break tags
        describ_html = describ.replace('\n', '<br />')

        self.story.append(Spacer(1, 12))
        # Add the description as a paragraph
        styles = getSampleStyleSheet()
        comment_paragraph_d = Paragraph(describ_html, styles['Normal'])
        self.story.append(comment_paragraph_d)
        
        
    def save_to_pdf(self):
        if not hasattr(self, 'data1_tv_directory') or not hasattr(self, 'data2_tv_directory') or not hasattr(self, 'data3_tv_directory'):
            # Data is not set, show an error dialog
            error_dialog = QMessageBox(self)
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("Please set the data first.")
            error_dialog.setStandardButtons(QMessageBox.Ok)
            error_dialog.exec_()
            return

        if not self.patient_name:
            # Patient name is not confirmed, show an error dialog
            error_dialog = QMessageBox(self)
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("Please confirm the patient name first.")
            error_dialog.setStandardButtons(QMessageBox.Ok)
            error_dialog.exec_()
            return
        
        pdf_filename = self.patient_name
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        
        styles = getSampleStyleSheet()
        if self.count == 0 :
            title = Paragraph(self.patient_name, styles['Title'])
            self.story.append(title)
            
        self.story.append(Spacer(1, 12))
        # Add the chart description as a paragraph
        comment_paragraph = Paragraph(self.chart_description, styles['Normal'])
        self.story.append(comment_paragraph)
        # Save the current plot as an image
        #self.story.append(Spacer(1, 12))
        image_filename = f"chart_image_{self.count}.png"
        self.plot_chart()
        self.fig.savefig(image_filename)
        # Add the image to the PDF
        img = plt.imread(image_filename)
        img_width = 600  # Adjust the image width as needed
        img_height = img_width * img.shape[0] / img.shape[1]
        img_flowable = Image(image_filename, width=img_width, height=img_height)
        self.story.append(img_flowable)
        self.count = self.count+1
        self.fig.clear()
        return self.story
        
        
    def generate_patient_report(self):
        if not hasattr(self, 'data1_tv_directory') or not hasattr(self, 'data2_tv_directory') or not hasattr(self, 'data3_tv_directory'):
            # Data is not set, show an error dialog
            error_dialog = QMessageBox(self)
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("Please set the data first.")
            error_dialog.setStandardButtons(QMessageBox.Ok)
            error_dialog.exec_()
            return
        
        if not self.patient_name:
            # Patient name is not confirmed, show an error dialog
            error_dialog = QMessageBox(self)
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("Please confirm the patient name first.")
            error_dialog.setStandardButtons(QMessageBox.Ok)
            error_dialog.exec_()
            return
        
        pdf_filename = self.patient_name + "_patientReport.pdf"
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        styles = getSampleStyleSheet()
        if self.count1 == 0 :
            title = Paragraph(self.patient_name, styles['Title'])
            self.patient_story.append(title)
            
        self.patient_story.append(Spacer(1, 12))
        
        self.plot_chart_patient_report()
        patient_story = self.patient_story
        # Build the PDF
        doc.build(patient_story) 
        
        # Create a Document
        # doc1 = Document()
        # # Add content to the Document
        # for item in self.patient_story:
        #     if isinstance(item, str):
        #         doc1.add_paragraph(item)
        #     elif isinstance(item, str):  # Assuming the image path is stored as a string
        #         doc1.add_picture(item, width=Inches(5)) # Adjust the width as needed
        # # Save the Document
        # doc1.save(self.patient_name + 'patient_story.docx')

        # Inform the user that the PDF has been saved
        info_dialog = QMessageBox(self)
        info_dialog.setIcon(QMessageBox.Information)
        info_dialog.setWindowTitle("Info")
        info_dialog.setText("Patient Report was generated successfully.")
        info_dialog.setStandardButtons(QMessageBox.Ok)
        info_dialog.exec_()
    
    
    def plot_chart_patient_report(self):
        self.fig.clear()
        passive_parameters = ("DF (Deg)","PF (Deg)", "ROM (Deg)", "Stiffness")
        passive_values = {
             self.chrtlbl1: (round(self.PR_dorsi[0],1), round(self.PR_plantar[0],1) , round(self.rom1,1) , 50*round(self.stfnss[0],1) ),
             self.chrtlbl2: (round(self.PR_dorsi[2],1), round(self.PR_plantar[2],1), round(self.rom2,1) ,50*round(self.stfnss[1],1)),
             self.chrtlbl3: (round(self.PR_dorsi[1],1), round(self.PR_plantar[1],1), round(self.rom3,1) ,50*round(self.stfnss[2],1)),
        }

        x = np.arange(len(passive_parameters))  # the label locations
        width = 0.15  # the width of the bars
        multiplier = 0

        #fig, ax = plt.subplots(subplot_kw={'constraint': 'tight'})
        ax = self.fig.add_subplot(111)

        for attribute, measurement in passive_values.items():
            offset = width * multiplier
            rects = ax.bar(x + offset, measurement, width, label=attribute)
            #ax.bar_label(rects, padding=3)
            multiplier += 1

         # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_title('Passive Parameters')
        ax.set_xticks(x + width, passive_parameters)
        ax.legend(loc='upper left', ncols=3)
        #ax.set_ylim(0, 250)
        
        
        self.canvas.draw()
        image_filename = f"chart_image1_{self.count1}.png"
        self.fig.savefig(image_filename)
        # Add the image to the PDF
        img = plt.imread(image_filename)
        img_width = 520  # Adjust the image width as needed
        img_height = img_width * img.shape[0] / img.shape[1]
        img_flowable = Image(image_filename, width=img_width, height=img_height)
        self.patient_story.append(img_flowable)
        self.patient_story.append(Spacer(1, 12))
        #self.patient_story.append(Spacer(1, 12))
        self.count1 = self.count1+1
        
        
        
        ax.clear()
        self.fig.clear()
        ax1 = self.fig.add_subplot(111)
        active_parameters = ("DF MVC (Nm)","PF MVC (Nm)", "Active ROM (deg)", "Speed (deg/sec)")
        
        #self.mvcd = round(self.mvcd , 2)
        active_values = {
             self.chrtlbl1: (round(self.mvcd[0], 1) , round(self.mvcp[0], 1) , round(self.AROM[0], 1) , round(self.speed[0], 1)),
             self.chrtlbl2: (round(self.mvcd[2], 1) , round(self.mvcp[2], 1) , round(self.AROM[1], 1) , round(self.speed[1], 1) ),
             self.chrtlbl3: (round(self.mvcd[1], 1) , round(self.mvcp[1], 1) , round(self.AROM[2], 1) , round(self.speed[2], 1) ),
        }

        x = np.arange(len(active_parameters))  # the label locations
        width = 0.15  # the width of the bars
        multiplier = 0

        #fig, ax1 = plt.subplots(layout='constrained')

        for attribute, measurement in active_values.items():
                offset = width * multiplier
                rects = ax1.bar(x + offset, measurement, width, label=attribute)
                #ax1.bar_label(rects, padding=3)
                multiplier += 1

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax1.set_title('Active Parameters')
        #plt.tight_layout() 
        ax1.set_xticks(x + width, active_parameters)
        ax1.legend(loc='upper left', ncols=3)
        #ax1.set_ylim(0, 250)

        #self.fig.clear()
        #self.fig.canvas.draw()
        self.canvas.draw()
        image_filename = f"chart_image1_{self.count1}.png"
        self.fig.savefig(image_filename)
        # Add the image to the PDF
        img = plt.imread(image_filename)
        img_width = 520  # Adjust the image width as needed
        img_height = img_width * img.shape[0] / img.shape[1]
        img_flowable = Image(image_filename, width=img_width, height=img_height)
        self.patient_story.append(img_flowable)
        #self.patient_story.append(Spacer(1, 12))
        self.patient_story.append(Spacer(1, 12))
        self.count1 = self.count1+1
        
        
    def generate_report(self):
        if not hasattr(self, 'data1_tv_directory') or not hasattr(self, 'data2_tv_directory'):
            # Data is not set, show an error dialog
            error_dialog = QMessageBox(self)
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("Please set the data first.")
            error_dialog.setStandardButtons(QMessageBox.Ok)
            error_dialog.exec_()
            return
        
        if not self.patient_name:
            # Patient name is not confirmed, show an error dialog
            error_dialog = QMessageBox(self)
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("Please confirm the patient name first.")
            error_dialog.setStandardButtons(QMessageBox.Ok)
            error_dialog.exec_()
            return
        
        pdf_filename = self.patient_name + "_report.pdf"
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        
        story = self.story
        # Build the PDF
        doc.build(story) 
        
        # Inform the user that the PDF has been saved
        info_dialog = QMessageBox(self)
        info_dialog.setIcon(QMessageBox.Information)
        info_dialog.setWindowTitle("Info")
        info_dialog.setText("PDF saved successfully.")
        info_dialog.setStandardButtons(QMessageBox.Ok)
        info_dialog.exec_()
        
    def upload_data(self):
        self.DirectoryOfDataSet1 = self.dir_input.text()
        self.DirectoryOfDataSet2 = self.dir_input2.text()
        self.DirectoryOfDataSet3 = self.dir_input3.text()
        
        # DATA SET 1 CASE DIRECTORY
        directory_path_TV5 = self.DirectoryOfDataSet1 + '\TV_5_3'
        directory_path_TV50 = self.DirectoryOfDataSet1 + '\TV_50_3'
        directory_path_TV100 = self.DirectoryOfDataSet1 + '\TV_100_3'
        directory_path_TV120 = self.DirectoryOfDataSet1 + '\TV_120_3'
        directory_path_mvc = self.DirectoryOfDataSet1 + '\MVC'
        directory_path_voluntary = self.DirectoryOfDataSet1 + '\Voluntary'
        # DATA DIRECTORY
        Data_tv_5 = directory_path_TV5 + '\data.csv'
        Data_tv_50 = directory_path_TV50 + '\data.csv'
        Data_tv_100 = directory_path_TV100 + '\data.csv'
        Data_tv_120 = directory_path_TV120 + '\data.csv'
        Data_mvc = directory_path_mvc
        Data_voluntary = directory_path_voluntary

        # DATA SET 2 CASE DIRECTORY
        directory_path2_TV5 = self.DirectoryOfDataSet2 + '\TV_5_3'
        directory_path2_TV50 = self.DirectoryOfDataSet2 + '\TV_50_3'
        directory_path2_TV100 = self.DirectoryOfDataSet2 + '\TV_100_3'
        directory_path2_TV120 = self.DirectoryOfDataSet2 + '\TV_120_3'
        directory_path2_mvc = self.DirectoryOfDataSet2 + '\MVC'
        directory_path2_voluntary = self.DirectoryOfDataSet2 + '\Voluntary'
        # DATA DIRECTORY
        Data2_tv_5 = directory_path2_TV5 + '\data.csv'
        Data2_tv_50 = directory_path2_TV50 + '\data.csv'
        Data2_tv_100 = directory_path2_TV100 + '\data.csv'
        Data2_tv_120 = directory_path2_TV120 + '\data.csv'
        Data2_mvc = directory_path2_mvc
        Data2_voluntary = directory_path2_voluntary
        
        # DATA SET 3 CASE DIRECTORY
        directory_path3_TV5 = self.DirectoryOfDataSet3 + '\TV_5_3'
        directory_path3_TV50 = self.DirectoryOfDataSet3 + '\TV_50_3'
        directory_path3_TV100 = self.DirectoryOfDataSet3 + '\TV_100_3'
        directory_path3_TV120 = self.DirectoryOfDataSet3 + '\TV_120_3'
        directory_path3_mvc = self.DirectoryOfDataSet3 + '\MVC'
        directory_path3_voluntary = self.DirectoryOfDataSet3 + '\Voluntary'
        # DATA DIRECTORY
        Data3_tv_5 = directory_path3_TV5 + '\data.csv'
        Data3_tv_50 = directory_path3_TV50 + '\data.csv'
        Data3_tv_100 = directory_path3_TV100 + '\data.csv'
        Data3_tv_120 = directory_path3_TV120 + '\data.csv'
        Data3_mvc = directory_path3_mvc
        Data3_voluntary = directory_path3_voluntary
      
        self.data1_tv_directory = [Data_tv_5, Data_tv_50, Data_tv_100, Data_tv_120, Data_mvc, Data_voluntary]
        self.data2_tv_directory = [Data2_tv_5, Data2_tv_50, Data2_tv_100, Data2_tv_120, Data2_mvc, Data2_voluntary]
        self.data3_tv_directory = [Data3_tv_5, Data3_tv_50, Data3_tv_100, Data3_tv_120, Data3_mvc, Data3_voluntary]

        self.folders1_tv_directory = [directory_path_TV5, directory_path_TV50, directory_path_TV100, directory_path_TV120, directory_path_mvc, directory_path_voluntary]
        self.folders2_tv_directory = [directory_path2_TV5, directory_path2_TV50, directory_path2_TV100, directory_path2_TV120, directory_path2_mvc, directory_path2_voluntary]
        self.folders3_tv_directory = [directory_path3_TV5, directory_path3_TV50, directory_path3_TV100, directory_path3_TV120, directory_path3_mvc, directory_path3_voluntary]
    
        self.figure_name = ['5 deg/sec', '50 deg/sec', '100 deg/sec', '120 deg/sec']
        pass

        
        
    def plot_chart(self):
        button = self.sender()  # Get the button that triggered the function
        try:
            button_index = self.buttons.index(button)  # Find the index of the button in the list
        except ValueError:
            print("Button not found in list")
            return 
            
        self.figure_name = ['5 deg/sec', '50 deg/sec', '100 deg/sec', '120 deg/sec']
        if not hasattr(self, 'data1_tv_directory') or not hasattr(self, 'data2_tv_directory') or not hasattr(self, 'data3_tv_directory'):
            # Data is not set, show an error dialog
            error_dialog = QMessageBox(self)
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("Please set the data first.")
            error_dialog.setStandardButtons(QMessageBox.Ok)
            error_dialog.exec_()
            return
        
        button_index = self.buttons.index(self.sender())
        if button_index == 16:
            cyclenumber = ['Cycle 1' , 'Cycle 2' , 'Cycle 3']
            if self.tvc == 2: 
                self.tvc=0 
                self.description_input.append(f'TV Cycle was changed to {cyclenumber[self.tvc]}')
                print(cyclenumber[self.tvc])
            else:
                self.tvc = self.tvc + 1
                self.description_input.append(f'TV Cycle was changed to {cyclenumber[self.tvc]}')
                print(cyclenumber[self.tvc])
            
        if button_index == 0:
            
            data = pd.read_csv(self.data1_tv_directory[0])
            # Read the CSV file for X-axis data (position_tv)
            position_tv_w = data['Position(rad)']*180/np.pi
            TvCycles_position = [0 , (len(position_tv_w)//3) , 2*(len(position_tv_w)//3) , len(position_tv_w) ]
            position_tv = position_tv_w.iloc[TvCycles_position[self.tvc]:TvCycles_position[self.tvc+1]]
            
             # Read the CSV file for Y-axis data (torque_tv)
            torque_tv_w = data['Torque(Mz)']
            TvCycles_torque = [0 , (len(torque_tv_w)//3) , 2*(len(torque_tv_w)//3) , len(torque_tv_w) ]
            torque_tv = -1*torque_tv_w.iloc[TvCycles_torque[self.tvc]:TvCycles_torque[self.tvc+1]]
             # Apply moving average smoothing to X and Y data
            window_length = 600  
            position_smoothed_tv = position_tv.rolling(window_length, min_periods=1).mean()
            torque_smoothed_tv = torque_tv.rolling(window_length, min_periods=1).mean()
            position_smoothed_tv = position_smoothed_tv + self.x_offset
            torque_smoothed_tv = torque_smoothed_tv + self.y_offset
             # Calculate the spasticity by Sampling the data frame at the specified interval
            sampling_interval = 300
            position_sampled = position_smoothed_tv.iloc[:len(position_smoothed_tv)//2:sampling_interval].reset_index(drop=True)
            torque_sampled = torque_smoothed_tv.iloc[:len(torque_smoothed_tv)//2:sampling_interval].reset_index(drop=True)
            
            # position_sampleds = np.array(position_smoothed_tv.iloc[:len(position_smoothed_tv)//2:sampling_interval])
            # torque_sampleds = np.array(torque_smoothed_tv.iloc[:len(torque_smoothed_tv)//2:sampling_interval])

            
            dy1 = [0] * (min(len(position_sampled) , len(torque_sampled)));
            for i in range(len(dy1)-6):
               # print(f"i: {i}, i+1: {i+1}, len(position_sampleds): {len(position_sampleds)}")
                delta_position = position_sampled[i + 5] - position_sampled[i+4]
                dy1[i] = (torque_sampled[i + 5] - torque_sampled[i+4]) / delta_position
                
            dy1.remove(min(dy1))
            dy1.remove(min(dy1))
            dy1.remove(max(dy1))     
            #dy_torque_sampled = torque_sampled.diff().iloc[:].values
            
            data2 = pd.read_csv(self.data2_tv_directory[0])
            data3 = pd.read_csv(self.data3_tv_directory[0])
            
            
            # Read the first CSV file for X-axis data
            position_tv_w2 = data2['Position(rad)']
            TvCycles_position2 = [0 , (len(position_tv_w2)//3) , 2*(len(position_tv_w2)//3) , len(position_tv_w2) ]
            position_tv_2 = (data2['Position(rad)'].iloc[TvCycles_position2[self.tvc]:TvCycles_position2[self.tvc+1]])*180/np.pi
            
            # Read the second CSV file for Y-axis data
            torque_tv_w2 = -1*data2['Torque(Mz)']
            TvCycles_torque2 = [0 , (len(torque_tv_w2)//3) , 2*(len(torque_tv_w2)//3) , len(torque_tv_w2) ]
            torque_tv_2 = -1*data2['Torque(Mz)'].iloc[TvCycles_torque2[self.tvc]:TvCycles_torque2[self.tvc+1]]
            
            position_tv_w3 = data3['Position(rad)']
            TvCycles_position3 = [0 , (len(position_tv_w3)//3) , 2*(len(position_tv_w3)//3) , len(position_tv_w3) ]
            position_tv_3 = (data3['Position(rad)'].iloc[TvCycles_position3[self.tvc]:TvCycles_position3[self.tvc+1]])*180/np.pi
            # Read the second CSV file for Y-axis data
            torque_tv_w3 = -1*data3['Torque(Mz)']
            TvCycles_torque3 = [0 , (len(torque_tv_w3)//3) , 2*(len(torque_tv_w3)//3) , len(torque_tv_w3) ]
            torque_tv_3 = -1*data3['Torque(Mz)'].iloc[TvCycles_torque3[self.tvc]:TvCycles_torque3[self.tvc+1]]
            
            # Apply moving average smoothing to X and Y data
            window_length = 600  # Adjust the window length as desired
            position_smoothed_tv_2 = position_tv_2.rolling(window_length, min_periods=1).mean()
            torque_smoothed_tv_2 = torque_tv_2.rolling(window_length, min_periods=1).mean()
            position_smoothed_tv_2 = position_smoothed_tv_2 + self.x_offset2
            torque_smoothed_tv_2 = torque_smoothed_tv_2 + self.y_offset2
            
            position_smoothed_tv_3 = position_tv_3.rolling(window_length, min_periods=1).mean()
            torque_smoothed_tv_3 = torque_tv_3.rolling(window_length, min_periods=1).mean()
            position_smoothed_tv_3 = position_smoothed_tv_3 + self.x_offset3
            torque_smoothed_tv_3 = torque_smoothed_tv_3 + self.y_offset3
            
            position_sampled2 = position_smoothed_tv_2.iloc[:len(position_smoothed_tv_2)//2:sampling_interval].reset_index(drop=True)
            torque_sampled2 = torque_smoothed_tv_2.iloc[:len(torque_smoothed_tv_2)//2:sampling_interval].reset_index(drop=True)
            #dy_torque_sampled2 = torque_sampled2.diff().iloc[:].values 
            position_sampled3 = position_smoothed_tv_3.iloc[:len(position_smoothed_tv_3)//2:sampling_interval].reset_index(drop=True)
            torque_sampled3 = torque_smoothed_tv_3.iloc[:len(torque_smoothed_tv_3)//2:sampling_interval].reset_index(drop=True)
            #dy_torque_sampled3 = torque_sampled3.diff().iloc[:].values 
            
            dy3 = [0] * (min(len(position_sampled2) , len(torque_sampled2)));
            for i in range(len(dy3)-6):
               # print(f"i: {i}, i+1: {i+1}, len(position_sampleds): {len(position_sampleds)}")
                delta_position2 = position_sampled2[i + 5] - position_sampled2[i+4]
                dy3[i] = (torque_sampled2[i + 5] - torque_sampled2[i+4]) / delta_position2
            dy3.remove(min(dy3))
            dy3.remove(min(dy3))
            dy3.remove(max(dy3))    
                
            dy2 = [0] * (min(len(position_sampled3) , len(torque_sampled3)));
            for i in range(len(dy2)-6):
                # print(f"i: {i}, i+1: {i+1}, len(position_sampleds): {len(position_sampleds)}")
                 delta_position3 = position_sampled3[i + 5] - position_sampled3[i+4]
                 dy2[i] = (torque_sampled3[i + 5] - torque_sampled3[i+4]) / delta_position3
                 
            dy2.remove(min(dy2))
            dy2.remove(min(dy2))
            dy2.remove(max(dy2))     
                 
            
            
            # Patient report
            dorsi1 = abs(position_smoothed_tv.max())
            plantar1 = abs(position_smoothed_tv.min())
            dorsi2 = abs(position_smoothed_tv_2.max())
            plantar2 = abs(position_smoothed_tv_2.min())
            dorsi3 = abs(position_smoothed_tv_3.max())
            plantar3 = abs(position_smoothed_tv_3.min())
            dorsiImprovement = ((dorsi2 - dorsi1)/dorsi1)*100
            plantarImprovement = ((plantar2 - plantar1)/plantar1)*100
            
            self.PR_dorsi = [dorsi1 , dorsi2 , dorsi3]
            self.PR_plantar = [plantar1 , plantar2 , plantar3]
            #self.PR_dorsi = [1, 2 , 3]
            #self.PR_plantar = [1, 2 , 3]
            self.PROM_improvement = [dorsiImprovement , plantarImprovement]
            
            # Calculate the area under the curve
            area = np.trapz(torque_smoothed_tv.squeeze(), position_smoothed_tv.squeeze())
            area2 = np.trapz(torque_smoothed_tv_2.squeeze(), position_smoothed_tv_2.squeeze())
            area3 = np.trapz(torque_smoothed_tv_3.squeeze(), position_smoothed_tv_3.squeeze())
            #self.energyloss = ((area2 - area)/area)*100
            
            # Read the comment text file
            comment_file_path = self.folders1_tv_directory[0] + '\comment.txt'
            with open(comment_file_path, 'r') as file:
                self.chart_description = file.read()
                
            # Set the chart description in the QTextEdit box
            self.chart_description_box.setText(self.chart_description)

            # Read the neutral position_tv text file
            file_path_neutral_position_tv = self.DirectoryOfDataSet1 + '\\NeutralPosition.txt'
            with open(file_path_neutral_position_tv, 'r') as file2:
                Neutralposition_tv_before = file2.read()
            
           # Read the neutral position_tv text file
            file_path_neutral_position_tv_2 = self.DirectoryOfDataSet2 + '\\NeutralPosition.txt'
            with open(file_path_neutral_position_tv_2, 'r') as file2:
                Neutralposition_tv_after = file2.read()
                
            # Read the neutral position_tv text file
            file_path_neutral_position_tv_3 = self.DirectoryOfDataSet3 + '\\NeutralPosition.txt'
            with open(file_path_neutral_position_tv_3, 'r') as file3:
                Neutralposition_tv_after = file3.read()
        
            stffnss_length = round(min(len(dy1),len(dy2),len(dy3))/2)
            self.stfnss = [sum(dy1[round(len(dy1)/2):stffnss_length+round(len(dy1)/2)]) / stffnss_length , sum(dy2[round(len(dy2)/2):stffnss_length+round(len(dy2)/2)]) / stffnss_length , sum(dy3[round(len(dy3)/2):stffnss_length+round(len(dy3)/2)]) / stffnss_length]
            self.stiffness_improvement = [((self.stfnss[0]-self.stfnss[1])/self.stfnss[0])*100 , ((self.stfnss[0]-self.stfnss[2])/self.stfnss[0])*100]
            self.description_input.append(f'Stiffness Improvement pre/{self.lbl2}: {round(self.stiffness_improvement[0],2)}%')
            self.description_input.append(f'Stiffness Improvement pre/{self.lbl3}: {round(self.stiffness_improvement[1],2)}%')
            self.description_input.append(f'Stiffness {self.lbl1}: {round(self.stfnss[0],2)}')
            self.description_input.append(f'Stiffness {self.lbl2}: {round(self.stfnss[1],2)}')
            self.description_input.append(f'Stiffness {self.lbl3}: {round(self.stfnss[2],2)}')
            
            
            # Plot the Spasticity
            self.fig.clear()
            ax = self.fig.add_subplot(121)
            ax.bar(position_sampled.iloc[4:len(dy1)+4], dy1[:-1], alpha=0.3, label= self.lbl1)
            ax.bar(position_sampled3.iloc[4:len(dy2)+4], dy2[:-1] ,alpha=0.3, label= self.lbl2)
            ax.bar(position_sampled2.iloc[4:len(dy3)+4], dy3[:-1] ,alpha=0.3, label= self.lbl3)
            ax.set_xlabel('Position')
            ax.set_ylabel('Stiffness')
            ax.set_title('Stiffness at '+ self.figure_name[0])
            ax.legend()
            #ax.grid()
            self.canvas.draw()
            
            # Plot the position-torque
            ax1 = self.fig.add_subplot(122)
            ax1.plot(position_smoothed_tv , torque_smoothed_tv , label = self.lbl1 )
            ax1.plot(position_smoothed_tv_3 , torque_smoothed_tv_3 , label = self.lbl2)
            ax1.plot(position_smoothed_tv_2 , torque_smoothed_tv_2 , label = self.lbl3)
            
            ax1.legend() # Show legend with data set names
            ax1.set_xlabel('Position (deg)')
            ax1.set_ylabel('Torque (Nm)')
            ax1.set_title('Passive ROM at ' + self.figure_name[0])
            #ax1.grid(True)
            #self.fig.text(0.5, 0.99, chart_description, wrap=True, horizontalalignment='center', fontsize=8)
            #ax1.text(0.98, 0.09, f'Energy Loss Before: {format(round(area,2))}', ha='right', va='top', transform=ax1.transAxes)
            #ax1.text(0.98, 0.05, f'Energy Loss After: {format(round(area2,2))}', ha='right', va='top', transform=ax1.transAxes)
            self.canvas.draw()
            
            
        elif button_index == 1:
            data = pd.read_csv(self.data1_tv_directory[1])
            # Read the CSV file for X-axis data (position_tv)
            position_tv_w = data['Position(rad)']*180/np.pi
            
            position_tv = position_tv_w.iloc[(len(position_tv_w)//3):2*(len(position_tv_w)//3)]
             # Read the CSV file for Y-axis data (torque_tv)
            torque_tv_w = data['Torque(Mz)']
            torque_tv = -1*torque_tv_w.iloc[(len(torque_tv_w)//3):2*(len(torque_tv_w)//3)]
             # Apply moving average smoothing to X and Y data
            window_length = 600  
            position_smoothed_tv = position_tv.rolling(window_length, min_periods=1).mean()
            position_smoothed_tv = position_smoothed_tv + self.x_offset
            torque_smoothed_tv = torque_tv.rolling(window_length, min_periods=1).mean()
            torque_smoothed_tv = torque_smoothed_tv + self.y_offset
            
             # Calculate the spasticity by Sampling the data frame at the specified interval
            sampling_interval = 50
            position_sampled = position_smoothed_tv.iloc[:len(position_smoothed_tv)//2:sampling_interval]
            torque_sampled = torque_smoothed_tv.iloc[:len(torque_smoothed_tv)//2:sampling_interval]
            dy_torque_sampled = torque_sampled.diff().iloc[:].values
            
            
            data2 = pd.read_csv(self.data2_tv_directory[1])
            # Read the first CSV file for X-axis data
            position_tv_2 = (data2['Position(rad)'].iloc[(len(data2['Position(rad)'])//3):2*(len(data2['Position(rad)'])//3)])*180/np.pi
            # Read the second CSV file for Y-axis data
            torque_tv_2 = -1*data2['Torque(Mz)'].iloc[(len(data2['Torque(Mz)'])//3):2*(len(data2['Torque(Mz)'])//3)]
            # Apply moving average smoothing to X and Y data
            window_length = 600  # Adjust the window length as desired
            position_smoothed_tv_2 = position_tv_2.rolling(window_length, min_periods=1).mean()
            position_smoothed_tv_2 = position_smoothed_tv_2 + self.x_offset2
            torque_smoothed_tv_2 = torque_tv_2.rolling(window_length, min_periods=1).mean()
            torque_smoothed_tv_2 = torque_smoothed_tv_2 + self.y_offset2
            
            position_sampled2 = position_smoothed_tv_2.iloc[:len(position_smoothed_tv_2)//2:sampling_interval]
            torque_sampled2 = torque_smoothed_tv_2.iloc[:len(torque_smoothed_tv_2)//2:sampling_interval]
            dy_torque_sampled2 = torque_sampled2.diff().iloc[:].values  
            
            data3 = pd.read_csv(self.data3_tv_directory[1])
            # Read the first CSV file for X-axis data
            position_tv_3 = (data3['Position(rad)'].iloc[(len(data3['Position(rad)'])//3):2*(len(data3['Position(rad)'])//3)])*180/np.pi
            # Read the second CSV file for Y-axis data
            torque_tv_3 = -1*data3['Torque(Mz)'].iloc[(len(data3['Torque(Mz)'])//3):2*(len(data3['Torque(Mz)'])//3)]
            # Apply moving average smoothing to X and Y data
            window_length = 600  # Adjust the window length as desired
            position_smoothed_tv_3 = position_tv_3.rolling(window_length, min_periods=1).mean()
            position_smoothed_tv_3 = position_smoothed_tv_3 + self.x_offset3
            torque_smoothed_tv_3 = torque_tv_3.rolling(window_length, min_periods=1).mean()
            torque_smoothed_tv_3 = torque_smoothed_tv_3 + self.y_offset3
            
            position_sampled3 = position_smoothed_tv_3.iloc[:len(position_smoothed_tv_3)//2:sampling_interval]
            torque_sampled3 = torque_smoothed_tv_3.iloc[:len(torque_smoothed_tv_3)//2:sampling_interval]
            dy_torque_sampled3 = torque_sampled3.diff().iloc[:].values  
            
            # Calculate the area under the curve
            area = np.trapz(torque_smoothed_tv.squeeze(), position_smoothed_tv.squeeze())
            area2 = np.trapz(torque_smoothed_tv_2.squeeze(), position_smoothed_tv_2.squeeze())
            area3 = np.trapz(torque_smoothed_tv_3.squeeze(), position_smoothed_tv_3.squeeze())
            
            # Read the comment text file
            comment_file_path = self.folders1_tv_directory[1] + '\comment.txt'
            with open(comment_file_path, 'r') as file:
                self.chart_description = file.read()
                
            # Set the chart description in the QTextEdit box
            self.chart_description_box.setText(self.chart_description)

            # Read the neutral position_tv text file
            file_path_neutral_position_tv = self.DirectoryOfDataSet1 + '\\NeutralPosition.txt'
            with open(file_path_neutral_position_tv, 'r') as file2:
                Neutralposition_tv_before = file2.read()
            
           # Read the neutral position_tv text file
            file_path_neutral_position_tv_2 = self.DirectoryOfDataSet2 + '\\NeutralPosition.txt'
            with open(file_path_neutral_position_tv_2, 'r') as file2:
                Neutralposition_tv_after = file2.read() 
                
            # Read the neutral position_tv text file
            file_path_neutral_position_tv_3 = self.DirectoryOfDataSet3 + '\\NeutralPosition.txt'
            with open(file_path_neutral_position_tv_3, 'r') as file3:
                Neutralposition_tv_post = file3.read() 
        
            # Plot the Spasticity
            self.fig.clear()
            ax = self.fig.add_subplot(121)
            ax.bar(position_sampled, dy_torque_sampled, alpha=0.3, label= self.lbl1)
            ax.bar(position_sampled3, dy_torque_sampled3,alpha=0.3, label= self.lbl2)
            ax.bar(position_sampled2, dy_torque_sampled2,alpha=0.3, label= self.lbl3)
            
            ax.set_xlabel('Position')
            ax.set_ylabel('Stiffness')
            ax.set_title('Stiffness at '+ self.figure_name[1])
            ax.legend()
            ax.grid()
            self.canvas.draw()
            
            # Plot the position-torque
            ax1 = self.fig.add_subplot(122)
            ax1.plot(position_smoothed_tv  , torque_smoothed_tv  , label = self.lbl1 )
            ax1.plot(position_smoothed_tv_3  , torque_smoothed_tv_3  , label = self.lbl2)
            ax1.plot(position_smoothed_tv_2  , torque_smoothed_tv_2  , label = self.lbl3)
            
            ax1.legend() # Show legend with data set names
            ax1.set_xlabel('Position (deg)')
            ax1.set_ylabel('Torque (Nm)')
            ax1.set_title('Passive ROM at ' + self.figure_name[1])
            ax1.grid(True)
            #self.fig.text(0.5, 0.99, chart_description, wrap=True, horizontalalignment='center', fontsize=8)
            #ax1.text(0.98, 0.09, f'Energy Loss Before: {format(round(area,2))}', ha='right', va='top', transform=ax1.transAxes)
            #ax1.text(0.98, 0.05, f'Energy Loss After: {format(round(area2,2))}', ha='right', va='top', transform=ax1.transAxes)
            self.canvas.draw()
        elif button_index == 2:
            data = pd.read_csv(self.data1_tv_directory[2])
            # Read the CSV file for X-axis data (position_tv)
            position_tv_w = data['Position(rad)']*180/np.pi
            position_tv = position_tv_w.iloc[(len(position_tv_w)//3):2*(len(position_tv_w)//3)]
             # Read the CSV file for Y-axis data (torque_tv)
            torque_tv_w = data['Torque(Mz)']
            torque_tv = -1*torque_tv_w.iloc[(len(torque_tv_w)//3):2*(len(torque_tv_w)//3)]
             # Apply moving average smoothing to X and Y data
            window_length = 600  
            position_smoothed_tv = position_tv.rolling(window_length, min_periods=1).mean()
            torque_smoothed_tv = torque_tv.rolling(window_length, min_periods=1).mean()
            position_smoothed_tv = position_smoothed_tv + self.x_offset
            torque_smoothed_tv = torque_smoothed_tv + self.y_offset
             # Calculate the spasticity by Sampling the data frame at the specified interval
            sampling_interval = 30
            position_sampled = position_smoothed_tv.iloc[:len(position_smoothed_tv)//2:sampling_interval]
            torque_sampled = torque_smoothed_tv.iloc[:len(torque_smoothed_tv)//2:sampling_interval]
            dy_torque_sampled = torque_sampled.diff().iloc[:].values
            
            data2 = pd.read_csv(self.data2_tv_directory[2])
            # Read the first CSV file for X-axis data
            position_tv_2 = (data2['Position(rad)'].iloc[(len(data2['Position(rad)'])//3):2*(len(data2['Position(rad)'])//3)])*180/np.pi
            # Read the second CSV file for Y-axis data
            torque_tv_2 = -1*data2['Torque(Mz)'].iloc[(len(data2['Torque(Mz)'])//3):2*(len(data2['Torque(Mz)'])//3)]
            # Apply moving average smoothing to X and Y data
            window_length = 600  # Adjust the window length as desired
            position_smoothed_tv_2 = position_tv_2.rolling(window_length, min_periods=1).mean()
            torque_smoothed_tv_2 = torque_tv_2.rolling(window_length, min_periods=1).mean()
            position_smoothed_tv_2 = position_smoothed_tv_2 + self.x_offset2
            torque_smoothed_tv_2 = torque_smoothed_tv_2 + self.y_offset2
            position_sampled2 = position_smoothed_tv_2.iloc[:len(position_smoothed_tv_2)//2:sampling_interval]
            torque_sampled2 = torque_smoothed_tv_2.iloc[:len(torque_smoothed_tv_2)//2:sampling_interval]
            dy_torque_sampled2 = torque_sampled2.diff().iloc[:].values   
            
            data3 = pd.read_csv(self.data3_tv_directory[2])
            # Read the first CSV file for X-axis data
            position_tv_3 = (data3['Position(rad)'].iloc[(len(data3['Position(rad)'])//3):2*(len(data3['Position(rad)'])//3)])*180/np.pi
            # Read the second CSV file for Y-axis data
            torque_tv_3 = -1*data3['Torque(Mz)'].iloc[(len(data3['Torque(Mz)'])//3):2*(len(data3['Torque(Mz)'])//3)]
            # Apply moving average smoothing to X and Y data
            window_length = 600  # Adjust the window length as desired
            position_smoothed_tv_3 = position_tv_3.rolling(window_length, min_periods=1).mean()
            torque_smoothed_tv_3 = torque_tv_3.rolling(window_length, min_periods=1).mean()
            position_smoothed_tv_3 = position_smoothed_tv_3 + self.x_offset3
            torque_smoothed_tv_3 = torque_smoothed_tv_3 + self.y_offset3
            position_sampled3 = position_smoothed_tv_3.iloc[:len(position_smoothed_tv_3)//2:sampling_interval]
            torque_sampled3 = torque_smoothed_tv_3.iloc[:len(torque_smoothed_tv_3)//2:sampling_interval]
            dy_torque_sampled3 = torque_sampled3.diff().iloc[:].values   
            
            # Calculate the area under the curve
            area = np.trapz(torque_smoothed_tv.squeeze(), position_smoothed_tv.squeeze())
            area2 = np.trapz(torque_smoothed_tv_2.squeeze(), position_smoothed_tv_2.squeeze())
            area3 = np.trapz(torque_smoothed_tv_3.squeeze(), position_smoothed_tv_3.squeeze())
            
            # Read the comment text file
            comment_file_path = self.folders1_tv_directory[2] + '\comment.txt'
            with open(comment_file_path, 'r') as file:
                self.chart_description = file.read()
                
            # Set the chart description in the QTextEdit box
            self.chart_description_box.setText(self.chart_description)

            # Read the neutral position_tv text file
            file_path_neutral_position_tv = self.DirectoryOfDataSet1 + '\\NeutralPosition.txt'
            with open(file_path_neutral_position_tv, 'r') as file2:
                Neutralposition_tv_before = file2.read()
            
           # Read the neutral position_tv text file
            file_path_neutral_position_tv_2 = self.DirectoryOfDataSet2 + '\\NeutralPosition.txt'
            with open(file_path_neutral_position_tv_2, 'r') as file2:
                Neutralposition_tv_after = file2.read()
                
            # Read the neutral position_tv text file
            file_path_neutral_position_tv_3 = self.DirectoryOfDataSet3 + '\\NeutralPosition.txt'
            with open(file_path_neutral_position_tv_3, 'r') as file3:
                Neutralposition_tv_post = file3.read()
        
            # Plot the Spasticity
            self.fig.clear()
            ax = self.fig.add_subplot(121)
            ax.bar(position_sampled, dy_torque_sampled, alpha=0.3, label= self.lbl1)
            ax.bar(position_sampled3, dy_torque_sampled3,alpha=0.3, label= self.lbl2)
            ax.bar(position_sampled2, dy_torque_sampled2,alpha=0.3, label= self.lbl3)
            
            ax.set_xlabel('Position')
            ax.set_ylabel('Stiffness')
            ax.set_title('Stiffness at '+ self.figure_name[2])
            ax.legend()
            ax.grid()
            self.canvas.draw()
            
            # Plot the position-torque
            ax1 = self.fig.add_subplot(122)
            ax1.plot(position_smoothed_tv , torque_smoothed_tv , label = self.lbl1 )
            ax1.plot(position_smoothed_tv_3 , torque_smoothed_tv_3 , label = self.lbl2)
            ax1.plot(position_smoothed_tv_2 , torque_smoothed_tv_2 , label = self.lbl3)
            
            
            ax1.legend() # Show legend with data set names
            ax1.set_xlabel('Position (deg)')
            ax1.set_ylabel('Torque (Nm)')
            ax1.set_title('Passive ROM at ' + self.figure_name[2])
            ax1.grid(True)
            #self.fig.text(0.5, 0.99, chart_description, wrap=True, horizontalalignment='center', fontsize=8)
            #ax1.text(0.98, 0.09, f'Energy Loss Before: {format(round(area,2))}', ha='right', va='top', transform=ax1.transAxes)
            #ax1.text(0.98, 0.05, f'Energy Loss After: {format(round(area2,2))}', ha='right', va='top', transform=ax1.transAxes)
            self.canvas.draw()
        elif button_index == 3:
            data = pd.read_csv(self.data1_tv_directory[3])
            # Read the CSV file for X-axis data (position_tv)
            position_tv_w = data['Position(rad)']*180/np.pi
            position_tv = position_tv_w.iloc[(len(position_tv_w)//3):2*(len(position_tv_w)//3)]
             # Read the CSV file for Y-axis data (torque_tv)
            torque_tv_w = data['Torque(Mz)']
            torque_tv = -1*torque_tv_w.iloc[(len(torque_tv_w)//3):2*(len(torque_tv_w)//3)]
             # Apply moving average smoothing to X and Y data
            window_length = 600  
            position_smoothed_tv = position_tv.rolling(window_length, min_periods=1).mean()
            torque_smoothed_tv = torque_tv.rolling(window_length, min_periods=1).mean()
            position_smoothed_tv = position_smoothed_tv + self.x_offset
            torque_smoothed_tv = torque_smoothed_tv + self.y_offset
            
             # Calculate the spasticity by Sampling the data frame at the specified interval
            sampling_interval = 20
            position_sampled = position_smoothed_tv.iloc[:len(position_smoothed_tv)//2:sampling_interval]
            torque_sampled = torque_smoothed_tv.iloc[:len(torque_smoothed_tv)//2:sampling_interval]
            dy_torque_sampled = torque_sampled.diff().iloc[:].values
            
            data2 = pd.read_csv(self.data2_tv_directory[3])
            # Read the first CSV file for X-axis data
            position_tv_2 = (data2['Position(rad)'].iloc[(len(data2['Position(rad)'])//3):2*(len(data2['Position(rad)'])//3)])*180/np.pi
            # Read the second CSV file for Y-axis data
            torque_tv_2 = -1*data2['Torque(Mz)'].iloc[(len(data2['Torque(Mz)'])//3):2*(len(data2['Torque(Mz)'])//3)]
            # Apply moving average smoothing to X and Y data
            window_length = 600  # Adjust the window length as desired
            position_smoothed_tv_2 = position_tv_2.rolling(window_length, min_periods=1).mean()
            torque_smoothed_tv_2 = torque_tv_2.rolling(window_length, min_periods=1).mean()
            position_smoothed_tv_2 = position_smoothed_tv_2 + self.x_offset2
            torque_smoothed_tv_2 = torque_smoothed_tv_2 + self.y_offset2
            position_sampled2 = position_smoothed_tv_2.iloc[:len(position_smoothed_tv_2)//2:sampling_interval]
            torque_sampled2 = torque_smoothed_tv_2.iloc[:len(torque_smoothed_tv_2)//2:sampling_interval]
            dy_torque_sampled2 = torque_sampled2.diff().iloc[:].values 
            
            data3 = pd.read_csv(self.data3_tv_directory[3])
            # Read the first CSV file for X-axis data
            position_tv_3 = (data3['Position(rad)'].iloc[(len(data3['Position(rad)'])//3):2*(len(data3['Position(rad)'])//3)])*180/np.pi
            # Read the second CSV file for Y-axis data
            torque_tv_3 = -1*data3['Torque(Mz)'].iloc[(len(data3['Torque(Mz)'])//3):2*(len(data3['Torque(Mz)'])//3)]
            # Apply moving average smoothing to X and Y data
            window_length = 600  # Adjust the window length as desired
            position_smoothed_tv_3 = position_tv_3.rolling(window_length, min_periods=1).mean()
            torque_smoothed_tv_3 = torque_tv_3.rolling(window_length, min_periods=1).mean()
            position_smoothed_tv_3 = position_smoothed_tv_3 + self.x_offset3
            torque_smoothed_tv_3 = torque_smoothed_tv_3 + self.y_offset3
            position_sampled3 = position_smoothed_tv_3.iloc[:len(position_smoothed_tv_3)//2:sampling_interval]
            torque_sampled3 = torque_smoothed_tv_3.iloc[:len(torque_smoothed_tv_3)//2:sampling_interval]
            dy_torque_sampled3 = torque_sampled3.diff().iloc[:].values 
            
            # Calculate the area under the curve
            area = np.trapz(torque_smoothed_tv.squeeze(), position_smoothed_tv.squeeze())
            area2 = np.trapz(torque_smoothed_tv_2.squeeze(), position_smoothed_tv_2.squeeze())
            area3 = np.trapz(torque_smoothed_tv_3.squeeze(), position_smoothed_tv_3.squeeze())
            
            # Read the comment text file
            comment_file_path = self.folders1_tv_directory[3] + '\comment.txt'
            with open(comment_file_path, 'r') as file:
                self.chart_description = file.read()
                
            # Set the chart description in the QTextEdit box
            self.chart_description_box.setText(self.chart_description)

            # Read the neutral position_tv text file
            file_path_neutral_position_tv = self.DirectoryOfDataSet1 + '\\NeutralPosition.txt'
            with open(file_path_neutral_position_tv, 'r') as file2:
                Neutralposition_tv_before = file2.read()
            
           # Read the neutral position_tv text file
            file_path_neutral_position_tv_2 = self.DirectoryOfDataSet2 + '\\NeutralPosition.txt'
            with open(file_path_neutral_position_tv_2, 'r') as file2:
                Neutralposition_tv_after = file2.read() 
                
            # Read the neutral position_tv text file
            file_path_neutral_position_tv_3 = self.DirectoryOfDataSet3 + '\\NeutralPosition.txt'
            with open(file_path_neutral_position_tv_3, 'r') as file3:
                Neutralposition_tv_post = file3.read() 
        
            # Plot the Spasticity
            self.fig.clear()
            ax = self.fig.add_subplot(121)
            ax.bar(position_sampled, dy_torque_sampled, alpha=0.3, label= self.lbl1)
            ax.bar(position_sampled3, dy_torque_sampled3,alpha=0.3, label= self.lbl2)
            ax.bar(position_sampled2, dy_torque_sampled2,alpha=0.3, label= self.lbl3)
            
            ax.set_xlabel('Position')
            ax.set_ylabel('Stiffness')
            ax.set_title('Stiffness at '+ self.figure_name[3])
            ax.legend()
            ax.grid()
            self.canvas.draw()
            
            # Plot the position-torque
            ax1 = self.fig.add_subplot(122)
            ax1.plot(position_smoothed_tv , torque_smoothed_tv , label = self.lbl1 )
            ax1.plot(position_smoothed_tv_3 , torque_smoothed_tv_3 , label = self.lbl2)
            ax1.plot(position_smoothed_tv_2 , torque_smoothed_tv_2 , label = self.lbl3)
            
            ax1.legend() # Show legend with data set names
            ax1.set_xlabel('Position (deg)')
            ax1.set_ylabel('Torque (Nm)')
            ax1.set_title('Passive ROM at ' + self.figure_name[3])
            ax1.grid(True)
            #self.fig.text(0.5, 0.99, chart_description, wrap=True, horizontalalignment='center', fontsize=8)
            #ax1.text(0.98, 0.09, f'Energy Loss Before: {format(round(area,2))}', ha='right', va='top', transform=ax1.transAxes)
            #ax1.text(0.98, 0.05, f'Energy Loss After: {format(round(area2,2))}', ha='right', va='top', transform=ax1.transAxes)
            self.canvas.draw()
            
        elif button_index == 4 or button.text() == '3▶️' or button.text() == '2▶️' or button.text() == '1▶️' or button.text() == 'R3' or button.text() == 'R2' or button.text() == 'R1':
            file_path = self.folders1_tv_directory[4] + '\comment.txt'
            with open(file_path, 'r') as file:
                self.chart_description = file.read()
                
            # Set the chart description in the QTextEdit box
            self.chart_description_box.setText(self.chart_description)
    
            # Read the neutral position text file
            file_path_neutral_position = self.DirectoryOfDataSet1 + '\\NeutralPosition.txt'
            with open(file_path_neutral_position, 'r') as file2:
                NeutralPosition_before = file2.read()
    
            # Read the neutral position text file
            file_path_neutral_position2 = self.DirectoryOfDataSet2 + '\\NeutralPosition.txt'
            with open(file_path_neutral_position2, 'r') as file3:
                NeutralPosition_after = file3.read()
                
            # Read the neutral position text file
            file_path_neutral_position3 = self.DirectoryOfDataSet3 + '\\NeutralPosition.txt'
            with open(file_path_neutral_position3, 'r') as file4:
                NeutralPosition_post = file4.read()
    
            # Set the path to the directory containing the CSV files
            mvc_csv_files = [file for file in os.listdir(self.data1_tv_directory[4]) if file.endswith('.csv')]
            mvc_csv_files2 = [file for file in os.listdir(self.data2_tv_directory[4]) if file.endswith('.csv')]
            mvc_csv_files3 = [file for file in os.listdir(self.data3_tv_directory[4]) if file.endswith('.csv')]
            
            DataMvc = pd.read_csv(self.data1_tv_directory[4] + '\\'+ mvc_csv_files[self.mvctrialscounter])
            if button.text() == '1▶️' and len(mvc_csv_files)>1:
                if len(mvc_csv_files)-1 == self.mvctrialscounter:
                    self.mvctrialscounter = 0
                    DataMvc = pd.read_csv(self.data1_tv_directory[4] + '\\'+ mvc_csv_files[self.mvctrialscounter])
                else:
                    #print(self.mvctrialscounter)
                    self.mvctrialscounter +=1
                    DataMvc = pd.read_csv(self.data1_tv_directory[4] + '\\'+ mvc_csv_files[self.mvctrialscounter])
                    
            DataMvc3 = pd.read_csv(self.data3_tv_directory[4] + '\\'+ mvc_csv_files3[self.mvctrialscounter2])
            if button.text() == '2▶️' and len(mvc_csv_files3)>1:
                if len(mvc_csv_files3)-1 == self.mvctrialscounter2:
                    self.mvctrialscounter2 = 0
                    DataMvc3 = pd.read_csv(self.data3_tv_directory[4] + '\\'+ mvc_csv_files3[self.mvctrialscounter2])
                else:
                    self.mvctrialscounter2 +=1
                    DataMvc3 = pd.read_csv(self.data3_tv_directory[4] + '\\'+ mvc_csv_files3[self.mvctrialscounter2])
                    
            DataMvc2 = pd.read_csv(self.data2_tv_directory[4] + '\\'+ mvc_csv_files2[self.mvctrialscounter3])
            if button.text() == '3▶️' and len(mvc_csv_files2)>1:
                if len(mvc_csv_files2)-1 == self.mvctrialscounter3:
                    self.mvctrialscounter3 = 0
                    DataMvc2 = pd.read_csv(self.data2_tv_directory[4] + '\\'+ mvc_csv_files2[self.mvctrialscounter3])
                else:
                    self.mvctrialscounter3 +=1
                    DataMvc2 = pd.read_csv(self.data2_tv_directory[4] + '\\'+ mvc_csv_files2[self.mvctrialscounter3])
                    
            # DataMvc = pd.read_csv(self.data1_tv_directory[4])
            # DataMvc2 = pd.read_csv(self.data2_tv_directory[4])
            # DataMvc3 = pd.read_csv(self.data3_tv_directory[4])

            # Read the CSV file for Y-axis data (Torque)
            torque_mvc = DataMvc['Torque(Mz)']
            torque_mvc2 = DataMvc2['Torque(Mz)']
            torque_mvc3 = DataMvc3['Torque(Mz)']

            # Apply moving average smoothing to X and Y data
            window_length = 200  
            time = np.linspace(0, 30, num=len(torque_mvc))
            torque = torque_mvc.rolling(window_length, min_periods=1).mean() 
            time2 = np.linspace(0, 30, num=len(torque_mvc2))
            torque2 = torque_mvc2.rolling(window_length, min_periods=1).mean() 
            time3 = np.linspace(0, 30, num=len(torque_mvc3))
            torque3 = torque_mvc3.rolling(window_length, min_periods=1).mean() 
            
                
            # Calculate the rolling mean and standard deviation with a window of 2 seconds
            window_size = 2000
            rolling_mean_first_third = torque.iloc[:len(torque)//3].rolling(window_size).mean()
            rolling_std_first_third = torque.iloc[:len(torque)//3].rolling(window_size).std()

            rolling_mean_last_third = torque.iloc[(len(torque)//3)*2:].rolling(window_size).mean()
            rolling_std_last_third = torque.iloc[(len(torque)//3)*2:].rolling(window_size).std()

            rolling_mean_first_third2 = torque2.iloc[:len(torque2)//3].rolling(window_size).mean()
            rolling_std_first_third2 = torque2.iloc[:len(torque2)//3].rolling(window_size).std()

            rolling_mean_last_third2 = torque2.iloc[(len(torque2)//3)*2:].rolling(window_size).mean()
            rolling_std_last_third2 = torque2.iloc[(len(torque2)//3)*2:].rolling(window_size).std()
            
            rolling_mean_first_third3 = torque3.iloc[:len(torque3)//3].rolling(window_size).mean()
            rolling_std_first_third3 = torque3.iloc[:len(torque3)//3].rolling(window_size).std()

            rolling_mean_last_third3 = torque3.iloc[(len(torque3)//3)*2:].rolling(window_size).mean()
            rolling_std_last_third3 = torque3.iloc[(len(torque3)//3)*2:].rolling(window_size).std()

            # Find the index where the standard deviation is minimum
            min_std_index_f = rolling_std_first_third.idxmin()
            min_std_index_l = rolling_std_last_third.idxmin()

            min_std_index_f2 = rolling_std_first_third2.idxmin()
            min_std_index_l2 = rolling_std_last_third2.idxmin()
            
            min_std_index_f3 = rolling_std_first_third3.idxmin()
            min_std_index_l3 = rolling_std_last_third3.idxmin()

            # Get the mean value of the 2-second window with minimum standard deviation
            mean_of_min_std_window_f = rolling_mean_first_third.loc[min_std_index_f]
            mean_of_min_std_window_l = rolling_mean_last_third.loc[min_std_index_l]

            mean_of_min_std_window_f2 = rolling_mean_first_third2.loc[min_std_index_f2]
            mean_of_min_std_window_l2 = rolling_mean_last_third2.loc[min_std_index_l2]
            
            mean_of_min_std_window_f3 = rolling_mean_first_third3.loc[min_std_index_f3]
            mean_of_min_std_window_l3 = rolling_mean_last_third3.loc[min_std_index_l3]

            # Plot the data
            self.fig.clear()
            
            if self.buttons[10].isChecked() :
                torque2 = np.flipud(torque2.values)
                buffer2 = mean_of_min_std_window_f2
                mean_of_min_std_window_f2 = mean_of_min_std_window_l2
                mean_of_min_std_window_l2 = buffer2
                
            if self.buttons[9].isChecked() :
                torque3 = np.flipud(torque3.values)
                buffer3 = mean_of_min_std_window_f3
                mean_of_min_std_window_f3 = mean_of_min_std_window_l3
                mean_of_min_std_window_l3 = buffer3
    
            if self.buttons[8].isChecked():
                torque = np.flipud(torque.values)
                buffer = mean_of_min_std_window_f
                mean_of_min_std_window_f = mean_of_min_std_window_l
                mean_of_min_std_window_l = buffer
            
            self.mvcd = [mean_of_min_std_window_f+self.mvc_offset , mean_of_min_std_window_f2+self.mvc_offset3, mean_of_min_std_window_f3+self.mvc_offset2]
            self.mvcp = [abs(mean_of_min_std_window_l+self.mvc_offset) , abs(mean_of_min_std_window_l2+self.mvc_offset3) , abs(mean_of_min_std_window_l3+self.mvc_offset2) ]
            #self.mvcd = [1 , 2, 3]
            #self.mvcp = [1 , 2, 3]
            
            #self.mvcimprovement = [((mean_of_min_std_window_f2 - mean_of_min_std_window_f)/mean_of_min_std_window_f)*100 , ((abs(mean_of_min_std_window_l2) - abs(mean_of_min_std_window_l))/abs(mean_of_min_std_window_l))*100]
            line1 = f'Dorsi {self.lbl1}: {round(mean_of_min_std_window_f+self.mvc_offset,2)}'
            line2 = f'Plantar {self.lbl1}: {round(mean_of_min_std_window_l+self.mvc_offset,2)}'
            line3 = f'Dorsi {self.lbl2}: {round(mean_of_min_std_window_f3+self.mvc_offset2,2)}'
            line4 = f'Plantar {self.lbl2}: {round(mean_of_min_std_window_l3+self.mvc_offset2,2)}'
            line5 = f'Dorsi {self.lbl3}: {round(mean_of_min_std_window_f2+self.mvc_offset3,2)}'
            line6 = f'Plantar {self.lbl3}: {round(mean_of_min_std_window_l2+self.mvc_offset3,2)}'
            line7 = f'Dorsi improvement Pre/{self.lbl2}: {(round(mean_of_min_std_window_f3+self.mvc_offset2,2)-round(mean_of_min_std_window_f+self.mvc_offset,2))/round(mean_of_min_std_window_f+self.mvc_offset,2)*100:.2f}'
            line8 = f'Plantar improvement Pre/{self.lbl2}: {(round(mean_of_min_std_window_l3+self.mvc_offset2,2)-round(mean_of_min_std_window_l+self.mvc_offset,2))/round(mean_of_min_std_window_l+self.mvc_offset,2)*100:.2f}'
            line9 = f'Dorsi improvement Pre/{self.lbl3}: {(round(mean_of_min_std_window_f2+self.mvc_offset3,2)-round(mean_of_min_std_window_f+self.mvc_offset,2))/round(mean_of_min_std_window_f+self.mvc_offset,2)*100:.2f}'
            line10 = f'Plantar improvement Pre/{self.lbl3}: {(round(mean_of_min_std_window_l2+self.mvc_offset3,2)-round(mean_of_min_std_window_l+self.mvc_offset,2))/round(mean_of_min_std_window_l+self.mvc_offset,2)*100:.2f}'
            
            mvc_content = [line1,line3,line5,line2,line4,line6,line7,line8,line9,line10]
            # Convert the list to a string
            mvc_content_str = '\n'.join(mvc_content)
            # Set the text
            self.description_input.setPlainText(mvc_content_str)
            
            ax3 = self.fig.add_subplot(111)
            ax3.plot(time,torque + self.mvc_offset  , label = self.lbl1)
            ax3.plot(time3,torque3 + self.mvc_offset2 , label = self.lbl2)
            ax3.plot(time2,torque2 + self.mvc_offset3 , label = self.lbl3)
            
            ax3.set_xlabel('Time')
            ax3.set_ylabel('Torque (Nm)')
            ax3.set_title('MVC')
            ax3.grid(True)
            # Add the mean values as text on the chart
            #ax3.text(0.3, 0.35, f'Dorsi Before: {round(mean_of_min_std_window_f,2)}', ha='right', va='top', transform=plt.gca().transAxes)
            #ax3.text(0.3, 0.25, f'Plantar Before: {round(mean_of_min_std_window_l,2)}', ha='right', va='top', transform=plt.gca().transAxes)
            ax3.legend()
            #ax3.text(0.3, 0.15, f'Dorsi After: {round(mean_of_min_std_window_f2,2)}', ha='right', va='top', transform=plt.gca().transAxes)
            #ax3.text(0.3, 0.05, f'Plantar After: {round(mean_of_min_std_window_l2,2)}', ha='right', va='top', transform=plt.gca().transAxes)
            #ax3.text(0.3, 0.55, f'Dorsi Post: {round(mean_of_min_std_window_f3,2)}', ha='right', va='top', transform=plt.gca().transAxes)
            #ax3.text(0.3, 0.45, f'Plantar Post: {round(mean_of_min_std_window_l3,2)}', ha='right', va='top', transform=plt.gca().transAxes)
            self.canvas.draw()


        elif button_index == 11 or button.text() == 'V3▶️' or button.text() == 'V2▶️' or button.text() == 'V1▶️':

            ################################## first data ################################

            # Read the text file
            file_path = self.folders1_tv_directory[5] + '\comment.txt'
            with open(file_path, 'r') as file:
                self.chart_description = file.read()
                
            # Set the chart description in the QTextEdit box
            self.chart_description_box.setText(self.chart_description)
            
            
            vol_csv_files = [file for file in os.listdir(self.data1_tv_directory[5]) if file.endswith('.csv')]
            vol_csv_files2 = [file for file in os.listdir(self.data2_tv_directory[5]) if file.endswith('.csv')]
            vol_csv_files3 = [file for file in os.listdir(self.data3_tv_directory[5]) if file.endswith('.csv')]
            
            data_voluntary_w = pd.read_csv(self.data1_tv_directory[5] + '\\'+ vol_csv_files[self.voltrialscounter])
            if button.text() == 'V1▶️' and len(vol_csv_files)>1:
                if len(vol_csv_files)-1 == self.voltrialscounter:
                    self.voltrialscounter = 0
                    data_voluntary_w = pd.read_csv(self.data1_tv_directory[5] + '\\'+vol_csv_files[self.voltrialscounter])
                else:
                    self.voltrialscounter +=1
                    data_voluntary_w = pd.read_csv(self.data1_tv_directory[5] + '\\'+vol_csv_files[self.voltrialscounter])
                    
            data_voluntary_w3 = pd.read_csv(self.data3_tv_directory[5] + '\\'+vol_csv_files3[self.voltrialscounter2])
            if button.text() == 'V2▶️' and len(vol_csv_files3)>1:
                if len(vol_csv_files3)-1 == self.voltrialscounter2:
                    self.voltrialscounter2 = 0
                    data_voluntary_w3 = pd.read_csv(self.data3_tv_directory[5] + '\\'+vol_csv_files3[self.voltrialscounter2])
                else:
                    self.voltrialscounter2 +=1
                    data_voluntary_w3 = pd.read_csv(self.data3_tv_directory[5] + '\\'+vol_csv_files3[self.voltrialscounter2])
                    
            data_voluntary_w2 = pd.read_csv(self.data2_tv_directory[5] + '\\'+vol_csv_files2[self.voltrialscounter3])
            if button.text() == 'V3▶️' and len(vol_csv_files2)>1:
                if len(vol_csv_files2)-1 == self.voltrialscounter3:
                    self.voltrialscounter3 = 0
                    data_voluntary_w2 = pd.read_csv(self.data2_tv_directory[5] + '\\'+vol_csv_files2[self.voltrialscounter3])
                else:
                    self.voltrialscounter3 +=1
                    data_voluntary_w2 = pd.read_csv(self.data2_tv_directory[5] + '\\'+vol_csv_files2[self.voltrialscounter3])
                
            
            #data_voluntary_w = pd.read_csv(self.data1_tv_directory[5])
            data_voluntary = data_voluntary_w['Position(rad)']
            
            # Apply moving average smoothing to X and Y data
            window_length = 200  
            data_voluntary_smoothed = data_voluntary.rolling(window_length, min_periods=1).mean() * (180 / np.pi)
            t = np.linspace(0,30,num= len(data_voluntary_smoothed))
            
            # Find extrema and minima in the signal
            maxima_indices, _ = find_peaks(data_voluntary_smoothed)
            minima_indices, _ = find_peaks(-data_voluntary_smoothed)
                
            maximas = [0] * len(maxima_indices)
            minimas = [0] * len(minima_indices)
            Tmaximas = [0] * len(maxima_indices)
            Tminimas = [0] * len(minima_indices)

            #Calculate the differences between the consecutive extrema and minima
            max_diff = -float('inf')
            maxspeed = -float('inf')
            diff_maxspeed = 0
            extrema_with_max_speed = None
            extrema_with_max_diff = None
            for i in range(1, min(len(maxima_indices), len(minima_indices))):
                maximas[i] = round(data_voluntary_smoothed[maxima_indices[i]],1)
                Tmaximas[i] = t[maxima_indices[i]]
                Tminimas[i] = t[minima_indices[i]]
                minimas[i] = round(data_voluntary_smoothed[minima_indices[i]],1)
                diff = abs(data_voluntary_smoothed[maxima_indices[i]] - data_voluntary_smoothed[minima_indices[i]])
                if diff > 1 and (abs(Tmaximas[i] - Tminimas[i])> 0.2):
                   diff_maxspeed = diff/abs(Tmaximas[i] - Tminimas[i])  
                if diff > max_diff:
                    max_diff = diff
                    extrema_with_max_diff = (maxima_indices[i], minima_indices[i])
                if diff_maxspeed > maxspeed and diff > 1:
                    maxspeed = diff_maxspeed
                    extrema_with_max_speed = (maxima_indices[i], minima_indices[i])

            #print(extrema_with_max_speed)
            min_value = data_voluntary_smoothed[extrema_with_max_diff[0]]
            max_value = data_voluntary_smoothed[extrema_with_max_diff[1]]
            min_value_str = f'{min_value:.2f}'
            max_value_str = f'{max_value:.2f}'
            


            ################################## second data ################################

            #data_voluntary_w2 = pd.read_csv(self.data2_tv_directory[5])
            data_voluntary2 = data_voluntary_w2['Position(rad)']

            # Apply moving average smoothing to X and Y data
            window_length = 200  # Adjust the window length as desired
            data_voluntary_smoothed2 = data_voluntary2.rolling(window_length, min_periods=1).mean()* (180 / np.pi)
            t2 = np.linspace(0,30,num= len(data_voluntary_smoothed2))
            # Find extrema and minima in the signal
            
            # Find extrema and minima in the signal
            maxima_indices2, _ = find_peaks(data_voluntary_smoothed2)
            minima_indices2, _ = find_peaks(-data_voluntary_smoothed2)
            maximas2 = [0] * len(maxima_indices2)
            minimas2 = [0] * len(minima_indices2)
            Tmaximas2 = [0] * len(maxima_indices2)
            Tminimas2 = [0] * len(minima_indices2)

            # Calculate the differences between the consecutive extrema and minima
            max_diff2 = -float('inf')
            extrema_with_max_diff2 = None
            maxspeed2 = -float('inf')
            extrema_with_max_speed2 = None
            diff_maxspeed2 = 0
            
            
            for i2 in range(1, min(len(maxima_indices2), len(minima_indices2))):
                maximas2[i2] = round(data_voluntary_smoothed2[maxima_indices2[i2]],1)
                Tmaximas2[i2] = t2[maxima_indices2[i2]]
                Tminimas2[i2] = t2[minima_indices2[i2]]
                minimas2[i2] = round(data_voluntary_smoothed2[minima_indices2[i2]],1)
                diff2 = abs(data_voluntary_smoothed2[maxima_indices2[i2]] - data_voluntary_smoothed2[minima_indices2[i2]])
                if diff2 > 1 and (abs(Tmaximas2[i2] - Tminimas2[i2])> 0.2):
                    diff_maxspeed2 = diff2/abs(Tmaximas2[i2] - Tminimas2[i2]) 
                if diff2 > max_diff2:
                    max_diff2 = diff2
                    extrema_with_max_diff2 = (maxima_indices2[i2], minima_indices2[i2])
                if diff_maxspeed2 > maxspeed2 and diff2 > 1:
                    maxspeed2 = diff_maxspeed2
                    extrema_with_max_speed2 = (maxima_indices2[i2], minima_indices2[i2])
        
            #print(len(Tminimas2))
            #print(len(minimas2))
            #print(extrema_with_max_speed2)
            
            min_value2 = data_voluntary_smoothed2[extrema_with_max_diff2[0]]
            max_value2 = data_voluntary_smoothed2[extrema_with_max_diff2[1]]
            min_value_str2 = f'{min_value2:.2f}'
            max_value_str2 = f'{max_value2:.2f}'
            
            ################################## third data ################################

            #data_voluntary_w3 = pd.read_csv(self.data3_tv_directory[5])
            data_voluntary3 = data_voluntary_w3['Position(rad)']

            # Apply moving average smoothing to X and Y data
            window_length = 200  # Adjust the window length as desired
            data_voluntary_smoothed3 = data_voluntary3.rolling(window_length, min_periods=1).mean()* (180 / np.pi)
            t3 = np.linspace(0,30,num= len(data_voluntary_smoothed3))
            
            # Find extrema and minima in the signal
            maxima_indices3, _ = find_peaks(data_voluntary_smoothed3)
            minima_indices3, _ = find_peaks(-data_voluntary_smoothed3)
            maximas3 = [0] * len(maxima_indices3)
            minimas3 = [0] * len(minima_indices3)
            Tmaximas3 = [0] * len(maxima_indices3)
            Tminimas3 = [0] * len(minima_indices3)

            # Calculate the differences between the consecutive extrema and minima
            max_diff3 = -float('inf')
            extrema_with_max_diff3 = None
            maxspeed3 = -float('inf')
            extrema_with_max_speed3 = None
            diff_maxspeed3 = 0
            for i3 in range(1, min(len(maxima_indices3), len(minima_indices3))):
                diff3 = abs(data_voluntary_smoothed3[maxima_indices3[i3]] - data_voluntary_smoothed3[minima_indices3[i3]])
                maximas3[i3] = round(data_voluntary_smoothed3[maxima_indices3[i3]],1)
                Tmaximas3[i3] = t3[maxima_indices3[i3]]
                Tminimas3[i3] = t3[minima_indices3[i3]]
                minimas3[i3] = round(data_voluntary_smoothed3[minima_indices3[i3]],1)
                
                if diff3 > 1 and (abs(Tmaximas3[i3] - Tminimas3[i3])> 0.2):
                    diff_maxspeed3 = diff3/abs(Tmaximas3[i3] - Tminimas3[i3]) 
                if diff3 > max_diff3:
                    max_diff3 = diff3
                    extrema_with_max_diff3 = (maxima_indices3[i3], minima_indices3[i3])
                if diff_maxspeed3 > maxspeed3 and diff3 > 1:
                    maxspeed3 = diff_maxspeed3
                    extrema_with_max_speed3 = (maxima_indices3[i3], minima_indices3[i3])

            #print(extrema_with_max_speed3)
            min_value3 = data_voluntary_smoothed3[extrema_with_max_diff3[0]]
            max_value3 = data_voluntary_smoothed3[extrema_with_max_diff3[1]]
            min_value_str3 = f'{min_value3:.2f}'
            max_value_str3 = f'{max_value3:.2f}'
            
            # Patient report
            self.AROM = [abs(max_value-min_value) , abs(max_value3-min_value3) , abs(max_value2-min_value2)]
            self.speed = [maxspeed ,maxspeed3 ,maxspeed2]
            #print(self.speed)
            #print(abs(t[extrema_with_max_diff[0]] - t[extrema_with_max_diff[1]]))
            #print(abs(max_value - min_value))
            
            self.speedimprovement = [ ((self.speed[1]-self.speed[0])/self.speed[0])*100 , ((self.speed[2]-self.speed[0])/self.speed[0])*100 ]
            self.AROMimprovement = [ ((self.AROM[1]-self.AROM[0])/self.AROM[0])*100 , ((self.AROM[2]-self.AROM[0])/self.AROM[0])*100 ]
            
            line00 = f"Max Speeds: Pre:{maxspeed:.2f} , {self.lbl2}:{maxspeed3:.2f} , {self.lbl3}:{maxspeed2:.2f} "
            line01 = f"Max AROMs: Pre:{self.AROM[0]:.2f} , {self.lbl2}:{self.AROM[1]:.2f} , {self.lbl3}:{self.AROM[2]:.2f} "
            line1 = f"Speed improvement pre/{self.lbl2}: {self.speedimprovement[0]:.2f} %"
            line2 = f"Speed improvement pre/{self.lbl3}: {self.speedimprovement[1]:.2f} %"
            line3 = f"AROM improvement pre/{self.lbl2}: {self.AROMimprovement[0]:.2f} %"
            line4 = f"AROM improvement pre/{self.lbl3}: {self.AROMimprovement[1]:.2f} %"
            voluntary_content = [line00,line01,line1,line2,line3,line4]
            # Convert the list to a string
            voluntary_content_str = '\n'.join(voluntary_content)
            # Set the text
            self.description_input.setPlainText(voluntary_content_str)

            self.fig.clear()
            ax4 = self.fig.add_subplot(311)
            ax4.plot(t , data_voluntary_smoothed,label= self.lbl1)
            ax4.set_ylabel('Position (deg)')
            # ax4.scatter(Tmaximas, maximas , c='g')
            # ax4.scatter(Tminimas, minimas , c='g')
            # for i, txt in enumerate(maximas):
            #     ax4.text(Tmaximas[i], maximas[i], str(txt), ha='right', va='bottom')
            # for i, txt in enumerate(minimas):
            #     ax4.text(Tminimas[i], minimas[i], str(txt), ha='right', va='top')
                
            ax4.scatter(t[extrema_with_max_diff[1]], data_voluntary_smoothed[extrema_with_max_diff[1]] , c='r')
            ax4.scatter(t[extrema_with_max_diff[0]], data_voluntary_smoothed[extrema_with_max_diff[0]] , c='r')
            ax4.legend()
            #plt.ylabel('Feedback Torque (Nm)')
            ax4.set_title('Voluntary')
            ax4.grid(True)
            ax4.text(t[extrema_with_max_diff[1]], data_voluntary_smoothed[extrema_with_max_diff[1]] , f'Max : {max_value_str}', ha='right', va='bottom', color='red')
            ax4.text(t[extrema_with_max_diff[0]], data_voluntary_smoothed[extrema_with_max_diff[0]] , f'Min : {min_value_str}', ha='right', va='top', color='red')
            
            ax5 = self.fig.add_subplot(313)
            ax5.plot(t2 ,data_voluntary_smoothed2, label= self.lbl3)
            ax5.set_ylabel('Position (deg)')
            # ax5.scatter(Tmaximas2, maximas2 , c='g')
            # ax5.scatter(Tminimas2, minimas2 , c='g')
            # for i2, txt2 in enumerate(maximas2):
            #     ax5.text(Tmaximas2[i2], maximas2[i2], str(txt2), ha='right', va='bottom')
            # for i2, txt2 in enumerate(minimas2):
            #     ax5.text(Tminimas2[i2], minimas2[i2], str(txt2), ha='right', va='top')
                
            ax5.scatter(t2[extrema_with_max_diff2[1]], data_voluntary_smoothed2[extrema_with_max_diff2[1]], c='r')
            ax5.scatter(t2[extrema_with_max_diff2[0]], data_voluntary_smoothed2[extrema_with_max_diff2[0]] , c='r')
            ax5.legend()
            ax5.text(t2[extrema_with_max_diff2[1]], data_voluntary_smoothed2[extrema_with_max_diff2[1]], f'Max : {max_value_str2}', ha='right', va='bottom', color='red')
            ax5.text(t2[extrema_with_max_diff2[0]], data_voluntary_smoothed2[extrema_with_max_diff2[0]] , f'Min : {min_value_str2}', ha='right', va='top', color='red')
            ax5.grid(True)
            
            ax5 = self.fig.add_subplot(312)
            ax5.plot(t3,data_voluntary_smoothed3, label= self.lbl2)
            ax5.set_ylabel('Position (deg)')
            # ax5.scatter(Tmaximas3, maximas3 , c='g')
            # ax5.scatter(Tminimas3, minimas3 , c='g')
            # for i3, txt3 in enumerate(maximas3):
            #     ax5.text(Tmaximas3[i3], maximas3[i3], str(txt3), ha='right', va='bottom')
            # for i3, txt3 in enumerate(minimas3):
            #     ax5.text(Tminimas3[i3], minimas3[i3], str(txt3), ha='right', va='top')
                
            ax5.scatter(t3[extrema_with_max_diff3[1]], data_voluntary_smoothed3[extrema_with_max_diff3[1]] , c='r')
            ax5.scatter(t3[extrema_with_max_diff3[1]], data_voluntary_smoothed3[extrema_with_max_diff3[1]] , c='r')
            ax5.legend()
            ax5.text(t3[extrema_with_max_diff3[1]], data_voluntary_smoothed3[extrema_with_max_diff3[1]] , f'Max : {max_value_str3}', ha='right', va='bottom', color='red')
            ax5.text(t3[extrema_with_max_diff3[0]], data_voluntary_smoothed3[extrema_with_max_diff3[0]] , f'Min : {min_value_str3}', ha='right', va='top', color='red')
            ax5.grid(True)
            #ax5.tight_layout()  # Adjust the layout to prevent overlapping
            self.canvas.draw()

        elif button_index == 15:
            data_w = pd.read_csv(self.data1_tv_directory[0])
            data = (data_w['Position(rad)']*180/np.pi) + self.x_offset
            data2_w = pd.read_csv(self.data2_tv_directory[0])
            data2 = (data2_w['Position(rad)']*180/np.pi) + self.x_offset2
            data3_w = pd.read_csv(self.data3_tv_directory[0])
            data3 = (data3_w['Position(rad)']*180/np.pi) + self.x_offset3
            
            # Read the neutral position_tv text file
            file_path_neutral_position_tv = self.DirectoryOfDataSet1 + '\\NeutralPosition.txt'
            with open(file_path_neutral_position_tv, 'r') as file2:
                Neutralposition_tv_before = file2.read()
            
           # Read the neutral position_tv text file
            file_path_neutral_position_tv_2 = self.DirectoryOfDataSet2 + '\\NeutralPosition.txt'
            with open(file_path_neutral_position_tv_2, 'r') as file2:
                Neutralposition_tv_after = file2.read() 
                
            # Read the neutral position_tv text file
            file_path_neutral_position_tv_3 = self.DirectoryOfDataSet3 + '\\NeutralPosition.txt'
            with open(file_path_neutral_position_tv_3, 'r') as file3:
                Neutralposition_tv_post = file3.read() 
            
            self.chart_description = ' '
            # Set the chart description in the QTextEdit box
            self.chart_description_box.setText(self.chart_description)
            
            # bar chart
            
            dorsi1 = abs(data.max())
            plantar1 = abs(data.min())
            dorsi2 = abs(data2.max())
            plantar2 = abs(data2.min())
            dorsi3 = abs(data3.max())
            plantar3 = abs(data3.min())
            self.rom1 = dorsi1 + plantar1
            self.rom2 = dorsi3 + plantar3
            self.rom3 = dorsi2 + plantar2
            dorsiImprovement = ((dorsi2 - dorsi1)/dorsi1)*100
            plantarImprovement = ((plantar2 - plantar1)/plantar1)*100
            dorsiImprovementpost = ((dorsi3 - dorsi1)/dorsi1)*100
            plantarImprovementpost = ((plantar3 - plantar1)/plantar1)*100
            x = ['DF {self.lbl1}','DF {self.lbl2}', 'DF {self.lbl3}' ]
            #y = [dorsi1, dorsi3, dorsi2]
            #x2 = ['PF Before','PF Post', 'PF After']
            #y2 = [plantar1 , plantar3, plantar2]
            
            line1 = f"NP {self.lbl1}: {abs(round(float(Neutralposition_tv_before),0))}"
            line2 = f"NP {self.lbl2}: {abs(round(float(Neutralposition_tv_post),0))}"
            line3 = f"NP {self.lbl3}: {abs(round(float(Neutralposition_tv_after),0))}"
            line4 = f"ROM {self.lbl1}: {round(float(dorsi1 + plantar1),0)} "
            line5 = f"ROM {self.lbl2}: {round(float(dorsi3 + plantar3),0)} "
            line6 = f"ROM {self.lbl3}: {round(float(dorsi2 + plantar2),0)} "
            #line7 = f"PI before/post: {round(float(plantarImprovementpost),0)} %"
            ROM_content = [line1,line2,line3,line4,line5,line6]
            # Convert the list to a string
            ROM_content_str = '\n'.join(ROM_content)
            # Set the text
            self.description_input.setPlainText(ROM_content_str)
            
            
            self.fig.clear()
            rom_parameters = ("Dorsiflextion ROM (Deg)","Plantarflexion ROM (Deg)")
            passive_values = {
                 self.chrtlbl1: (round(dorsi1 ,2), round(plantar1 ,2)),
                 self.chrtlbl2: (round(dorsi3 ,2), round(plantar3 ,2)),
                 self.chrtlbl3: (round(dorsi2 ,2), round(plantar2 ,2)),
            }

            x = np.arange(len(rom_parameters))  # the label locations
            width = 0.15  # the width of the bars
            multiplier = 0

            #fig, ax = plt.subplots(subplot_kw={'constraint': 'tight'})
            ax = self.fig.add_subplot(111)

            for attribute, measurement in passive_values.items():
                offset = width * multiplier
                rects = ax.bar(x + offset, measurement, width, label=attribute)
                ax.bar_label(rects, padding=3)
                multiplier += 1

             # Add some text for labels, title and custom x-axis tick labels, etc.
            ax.set_title('ROM')
            ax.set_xticks(x + width, rom_parameters)
            ax.set_ylabel('Position (deg)')
            ax.legend(loc='lower left', ncols=3)
            #ax.set_ylim(0, 250)
            self.canvas.draw()
            
            #ax6 = self.fig.add_subplot(121)
            #ax6.bar(x,y,width=0.4)
            #ax6.set_title('Passive ROM')
            #ax6.set_ylabel('Position (deg)')
            #ax6.text(0.3, 0.98, f'NP before: {abs(round(float(Neutralposition_tv_before),0))}', ha='right', va='top', transform=plt.gca().transAxes)
            #ax6.text(0.3, 0.88, f'NP post: {abs(round(float(Neutralposition_tv_post),0))}', ha='right', va='top', transform=plt.gca().transAxes)
            #ax6.text(0.3, 0.78, f'NP after: {abs(round(float(Neutralposition_tv_after),0))}', ha='right', va='top', transform=plt.gca().transAxes)
            #ax7 = self.fig.add_subplot(122)
            #ax7.bar(x2,y2, color = 'orange',width=0.3)
            # ax7.set_title('Passive ROM')
            # ax7.set_ylabel('Position (deg)')
            # ax7.text(0.3, 0.98, f'DI after: {round(float(dorsiImprovement),0)} %', ha='right', va='top', transform=plt.gca().transAxes) 
            # ax7.text(0.3, 0.88, f'PI after: {round(float(plantarImprovement),0)} %', ha='right', va='top', transform=plt.gca().transAxes) 
            # ax7.text(0.3, 0.78, f'DI before/post: {round(float(dorsiImprovementpost),0)} %', ha='right', va='top', transform=plt.gca().transAxes) 
            # ax7.text(0.3, 0.68, f'PI before/post: {round(float(plantarImprovementpost),0)} %', ha='right', va='top', transform=plt.gca().transAxes) 
        pass
    # self.canvas.draw()

            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
