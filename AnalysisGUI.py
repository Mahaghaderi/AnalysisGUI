import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTextEdit
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image
from PyQt5.QtWidgets import QSlider


class MainWindow(QMainWindow):
    story = []
    count = 0
    def __init__(self):
        super().__init__()

        self.patient_name = ""
        self.x_offset = 0
        self.y_offset = 0
        self.x_offset2 = 0
        self.y_offset2 = 0
        
        self.setWindowTitle("Data Analysis")
        self.setGeometry(150, 100, 1000, 900)

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)  
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        chart_box = QWidget()
        chart_layout = QVBoxLayout()
        chart_layout.setContentsMargins(10, 10, 10, 10) 

        name_label = QLabel("Patient Name:")
        self.name_input = QLineEdit()
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.save_patient_name)
        name_layout = QHBoxLayout()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        name_layout.addWidget(self.confirm_button)
        main_layout.addLayout(name_layout)

        data_label = QLabel("Enter the path of the dataset 1 considered as before:")
        self.dir_input = QLineEdit()
        data_label2 = QLabel("Enter the path of the dataset 2 considered as after:")
        self.dir_input2 = QLineEdit()
        plot_button2 = QPushButton("Set")
        plot_button2.clicked.connect(self.upload_data)
        chart_layout.addWidget(data_label)
        chart_layout.addWidget(self.dir_input)
        #chart_layout.addWidget(plot_button)
        chart_layout.addWidget(data_label2)
        chart_layout.addWidget(self.dir_input2)
        chart_layout.addWidget(plot_button2)
         
        chart_layout.addWidget(chart_box)
        main_layout.addLayout(chart_layout, stretch=20)

        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        main_layout.addWidget(self.canvas)
        
        # Create sliders
        self.x_slider = QSlider(Qt.Horizontal)
        self.y_slider = QSlider(Qt.Horizontal)
        self.x_slider2 = QSlider(Qt.Horizontal)
        self.y_slider2 = QSlider(Qt.Horizontal)
        
        self.x_slider.setMinimum(-30)
        self.x_slider.setMaximum(30)
        self.x_slider.setValue(0)  # Initial value

        self.y_slider.setMinimum(-30)
        self.y_slider.setMaximum(30)
        self.y_slider.setValue(0)  # Initial value
        
        self.x_slider2.setMinimum(-30)
        self.x_slider2.setMaximum(30)
        self.x_slider2.setValue(0)  # Initial value

        self.y_slider2.setMinimum(-30)
        self.y_slider2.setMaximum(30)
        self.y_slider2.setValue(0)  # Initial value
        
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.x_slider2)
        slider_layout.addWidget(self.y_slider2)
        slider_layout.addWidget(self.x_slider)
        slider_layout.addWidget(self.y_slider)
        slider_labelx = QLabel("X Before")
        slider_labely = QLabel("Y Before")
        slider_labelx2 = QLabel("X After")
        slider_labely2 = QLabel("Y After")
        slider_label_layout = QHBoxLayout()
        slider_label_layout.addWidget(slider_labelx)
        slider_label_layout.addWidget(slider_labely)
        slider_label_layout.addWidget(slider_labelx2)
        slider_label_layout.addWidget(slider_labely2)
        main_layout.addLayout(slider_label_layout)
        main_layout.addLayout(slider_layout)
        self.x_slider.valueChanged.connect(self.update_x_offset)
        self.y_slider.valueChanged.connect(self.update_y_offset)
        self.x_slider2.valueChanged.connect(self.update_x_offset2)
        self.y_slider2.valueChanged.connect(self.update_y_offset2)


        
        button_names = ["TV 5", "TV 50", "TV 100", "TV 120", "MVC", "VOLUNTARY", "ROM", "RMVC_A", "RMVC_B"]
        self.buttons = []
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        for name in button_names:
            button = QPushButton(name)
            button.clicked.connect(self.plot_chart)
            button_layout.addWidget(button)
            self.buttons.append(button)
            
        self.buttons[7].setCheckable(True)
        self.buttons[7].toggle()
        
        self.buttons[8].setCheckable(True)
        self.buttons[8].toggle()
        
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
        plot_button_description = QPushButton("Add Description")
        plot_button_description.clicked.connect(self.description)
        main_layout.addWidget(description)
        main_layout.addWidget(self.description_input)
        main_layout.addWidget(plot_button_description)
        
        # Create the "Generate Report" button
        generate_report_button = QPushButton("Generate Report")
        generate_report_button.clicked.connect(self.generate_report)
        main_layout.addWidget(generate_report_button)  
        
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
    
    def save_patient_name(self):
            self.patient_name = self.name_input.text()
            self.count = 0
            print("Patient Name:", self.patient_name)
    
    def description(self):
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
        
        describ = self.description_input.toPlainText()
        self.story.append(Spacer(1, 12))
        # Add the description as a paragraph
        styles = getSampleStyleSheet()
        comment_paragraph_d = Paragraph(describ, styles['Normal'])
        self.story.append(comment_paragraph_d)
        #self.story.append(Spacer(1, 12))
        
        
    def save_to_pdf(self):
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
        Data_mvc = directory_path_mvc + '\data.csv'
        Data_voluntary = directory_path_voluntary + '\data.csv'

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
        Data2_mvc = directory_path2_mvc + '\data.csv'
        Data2_voluntary = directory_path2_voluntary + '\data.csv'
      
        self.data1_tv_directory = [Data_tv_5, Data_tv_50, Data_tv_100, Data_tv_120, Data_mvc, Data_voluntary]
        self.data2_tv_directory = [Data2_tv_5, Data2_tv_50, Data2_tv_100, Data2_tv_120, Data2_mvc, Data2_voluntary]

        self.folders1_tv_directory = [directory_path_TV5, directory_path_TV50, directory_path_TV100, directory_path_TV120, directory_path_mvc, directory_path_voluntary]
        self.folders2_tv_directory = [directory_path2_TV5, directory_path2_TV50, directory_path2_TV100, directory_path2_TV120, directory_path2_mvc, directory_path2_voluntary]
    
        self.figure_name = ['5 deg/sec', '50 deg/sec', '100 deg/sec', '120 deg/sec']

        
        
    def plot_chart(self):
        button = self.sender()  # Get the button that triggered the function
        try:
            button_index = self.buttons.index(button)  # Find the index of the button in the list
        except ValueError:
            print("Button not found in list")
            return 
            
        self.figure_name = ['5 deg/sec', '50 deg/sec', '100 deg/sec', '120 deg/sec']
        if not hasattr(self, 'data1_tv_directory') or not hasattr(self, 'data2_tv_directory'):
            # Data is not set, show an error dialog
            error_dialog = QMessageBox(self)
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("Please set the data first.")
            error_dialog.setStandardButtons(QMessageBox.Ok)
            error_dialog.exec_()
            return
        
        button_index = self.buttons.index(self.sender())
        if button_index == 0:
            data = pd.read_csv(self.data1_tv_directory[0])
            # Read the CSV file for X-axis data (position_tv)
            position_tv_w = data['Enc. Position(deg)']
            position_tv = position_tv_w.iloc[(len(position_tv_w)//3):2*(len(position_tv_w)//3)]
             # Read the CSV file for Y-axis data (torque_tv)
            torque_tv_w = data['Torque(Mz)']
            torque_tv = torque_tv_w.iloc[(len(torque_tv_w)//3):2*(len(torque_tv_w)//3)]
             # Apply moving average smoothing to X and Y data
            window_length = 600  
            position_smoothed_tv = position_tv.rolling(window_length, min_periods=1).mean()
            torque_smoothed_tv = torque_tv.rolling(window_length, min_periods=1).mean()
            position_smoothed_tv = position_smoothed_tv + self.x_offset
            torque_smoothed_tv = torque_smoothed_tv + self.y_offset
             # Calculate the spasticity by Sampling the data frame at the specified interval
            sampling_interval = 150
            position_sampled = position_smoothed_tv.iloc[:len(position_smoothed_tv)//2:sampling_interval]
            torque_sampled = torque_smoothed_tv.iloc[:len(torque_smoothed_tv)//2:sampling_interval]
            dy_torque_sampled = torque_sampled.diff().iloc[:].values
            
            data2 = pd.read_csv(self.data2_tv_directory[0])
            # Read the first CSV file for X-axis data
            position_tv_2 = data2['Enc. Position(deg)'].iloc[(len(data2['Enc. Position(deg)'])//3):2*(len(data2['Enc. Position(deg)'])//3)]
            # Read the second CSV file for Y-axis data
            torque_tv_2 = data2['Torque(Mz)'].iloc[(len(data2['Torque(Mz)'])//3):2*(len(data2['Torque(Mz)'])//3)]
            # Apply moving average smoothing to X and Y data
            window_length = 600  # Adjust the window length as desired
            position_smoothed_tv_2 = position_tv_2.rolling(window_length, min_periods=1).mean()
            torque_smoothed_tv_2 = torque_tv_2.rolling(window_length, min_periods=1).mean()
            position_smoothed_tv_2 = position_smoothed_tv_2 + self.x_offset2
            torque_smoothed_tv_2 = torque_smoothed_tv_2 + self.y_offset2
            
            position_sampled2 = position_smoothed_tv_2.iloc[:len(position_smoothed_tv_2)//2:sampling_interval]
            torque_sampled2 = torque_smoothed_tv_2.iloc[:len(torque_smoothed_tv_2)//2:sampling_interval]
            dy_torque_sampled2 = torque_sampled2.diff().iloc[:].values   
            
            # Calculate the area under the curve
            area = np.trapz(torque_smoothed_tv.squeeze(), position_smoothed_tv.squeeze())
            area2 = np.trapz(torque_smoothed_tv_2.squeeze(), position_smoothed_tv_2.squeeze())
            
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
        
            # Plot the Spasticity
            self.fig.clear()
            ax = self.fig.add_subplot(121)
            ax.bar(position_sampled, dy_torque_sampled, alpha=0.3, label='Before')
            ax.bar(position_sampled2, dy_torque_sampled2,alpha=0.3, label='After')
            ax.set_xlabel('Position')
            ax.set_ylabel('Stiffness')
            ax.set_title('Stiffness at '+ self.figure_name[0])
            ax.legend()
            ax.grid()
            self.canvas.draw()
            
            # Plot the position-torque
            ax1 = self.fig.add_subplot(122)
            ax1.plot(position_smoothed_tv , torque_smoothed_tv , label = 'Before' )
            ax1.plot(position_smoothed_tv_2 , torque_smoothed_tv_2 , label = 'After')
            ax1.legend() # Show legend with data set names
            ax1.set_xlabel('Position (deg)')
            ax1.set_ylabel('Torque (Nm)')
            ax1.set_title('Passive ROM at ' + self.figure_name[0])
            ax1.grid(True)
            #self.fig.text(0.5, 0.99, chart_description, wrap=True, horizontalalignment='center', fontsize=8)
            ax1.text(0.98, 0.09, f'Energy Loss Before: {format(round(area,2))}', ha='right', va='top', transform=ax1.transAxes)
            ax1.text(0.98, 0.05, f'Energy Loss After: {format(round(area2,2))}', ha='right', va='top', transform=ax1.transAxes)
            self.canvas.draw()
            
            
        elif button_index == 1:
            data = pd.read_csv(self.data1_tv_directory[1])
            # Read the CSV file for X-axis data (position_tv)
            position_tv_w = data['Enc. Position(deg)']
            position_tv = position_tv_w.iloc[(len(position_tv_w)//3):2*(len(position_tv_w)//3)]
             # Read the CSV file for Y-axis data (torque_tv)
            torque_tv_w = data['Torque(Mz)']
            torque_tv = torque_tv_w.iloc[(len(torque_tv_w)//3):2*(len(torque_tv_w)//3)]
             # Apply moving average smoothing to X and Y data
            window_length = 600  
            position_smoothed_tv = position_tv.rolling(window_length, min_periods=1).mean()
            position_smoothed_tv = position_smoothed_tv + self.x_offset
            torque_smoothed_tv = torque_tv.rolling(window_length, min_periods=1).mean()
            torque_smoothed_tv = torque_smoothed_tv + self.y_offset
            
             # Calculate the spasticity by Sampling the data frame at the specified interval
            sampling_interval = 150
            position_sampled = position_smoothed_tv.iloc[:len(position_smoothed_tv)//2:sampling_interval]
            torque_sampled = torque_smoothed_tv.iloc[:len(torque_smoothed_tv)//2:sampling_interval]
            dy_torque_sampled = torque_sampled.diff().iloc[:].values
            
            
            data2 = pd.read_csv(self.data2_tv_directory[1])
            # Read the first CSV file for X-axis data
            position_tv_2 = data2['Enc. Position(deg)'].iloc[(len(data2['Enc. Position(deg)'])//3):2*(len(data2['Enc. Position(deg)'])//3)]
            # Read the second CSV file for Y-axis data
            torque_tv_2 = data2['Torque(Mz)'].iloc[(len(data2['Torque(Mz)'])//3):2*(len(data2['Torque(Mz)'])//3)]
            # Apply moving average smoothing to X and Y data
            window_length = 600  # Adjust the window length as desired
            position_smoothed_tv_2 = position_tv_2.rolling(window_length, min_periods=1).mean()
            position_smoothed_tv_2 = position_smoothed_tv_2 + self.x_offset2
            torque_smoothed_tv_2 = torque_tv_2.rolling(window_length, min_periods=1).mean()
            torque_smoothed_tv_2 = torque_smoothed_tv_2 + self.y_offset2
            
            position_sampled2 = position_smoothed_tv_2.iloc[:len(position_smoothed_tv_2)//2:sampling_interval]
            torque_sampled2 = torque_smoothed_tv_2.iloc[:len(torque_smoothed_tv_2)//2:sampling_interval]
            dy_torque_sampled2 = torque_sampled2.diff().iloc[:].values   
            
            # Calculate the area under the curve
            area = np.trapz(torque_smoothed_tv.squeeze(), position_smoothed_tv.squeeze())
            area2 = np.trapz(torque_smoothed_tv_2.squeeze(), position_smoothed_tv_2.squeeze())
            
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
        
            # Plot the Spasticity
            self.fig.clear()
            ax = self.fig.add_subplot(121)
            ax.bar(position_sampled, dy_torque_sampled, alpha=0.3, label='Before')
            ax.bar(position_sampled2, dy_torque_sampled2,alpha=0.3, label='After')
            ax.set_xlabel('Position')
            ax.set_ylabel('Stiffness')
            ax.set_title('Stiffness at '+ self.figure_name[1])
            ax.legend()
            ax.grid()
            self.canvas.draw()
            
            # Plot the position-torque
            ax1 = self.fig.add_subplot(122)
            ax1.plot(position_smoothed_tv  , torque_smoothed_tv  , label = 'Before' )
            ax1.plot(position_smoothed_tv_2  , torque_smoothed_tv_2  , label = 'After')
            ax1.legend() # Show legend with data set names
            ax1.set_xlabel('Position (deg)')
            ax1.set_ylabel('Torque (Nm)')
            ax1.set_title('Passive ROM at ' + self.figure_name[1])
            ax1.grid(True)
            #self.fig.text(0.5, 0.99, chart_description, wrap=True, horizontalalignment='center', fontsize=8)
            ax1.text(0.98, 0.09, f'Energy Loss Before: {format(round(area,2))}', ha='right', va='top', transform=ax1.transAxes)
            ax1.text(0.98, 0.05, f'Energy Loss After: {format(round(area2,2))}', ha='right', va='top', transform=ax1.transAxes)
            self.canvas.draw()
        elif button_index == 2:
            data = pd.read_csv(self.data1_tv_directory[2])
            # Read the CSV file for X-axis data (position_tv)
            position_tv_w = data['Enc. Position(deg)']
            position_tv = position_tv_w.iloc[(len(position_tv_w)//3):2*(len(position_tv_w)//3)]
             # Read the CSV file for Y-axis data (torque_tv)
            torque_tv_w = data['Torque(Mz)']
            torque_tv = torque_tv_w.iloc[(len(torque_tv_w)//3):2*(len(torque_tv_w)//3)]
             # Apply moving average smoothing to X and Y data
            window_length = 600  
            position_smoothed_tv = position_tv.rolling(window_length, min_periods=1).mean()
            torque_smoothed_tv = torque_tv.rolling(window_length, min_periods=1).mean()
            position_smoothed_tv = position_smoothed_tv + self.x_offset
            torque_smoothed_tv = torque_smoothed_tv + self.y_offset
             # Calculate the spasticity by Sampling the data frame at the specified interval
            sampling_interval = 150
            position_sampled = position_smoothed_tv.iloc[:len(position_smoothed_tv)//2:sampling_interval]
            torque_sampled = torque_smoothed_tv.iloc[:len(torque_smoothed_tv)//2:sampling_interval]
            dy_torque_sampled = torque_sampled.diff().iloc[:].values
            
            data2 = pd.read_csv(self.data2_tv_directory[2])
            # Read the first CSV file for X-axis data
            position_tv_2 = data2['Enc. Position(deg)'].iloc[(len(data2['Enc. Position(deg)'])//3):2*(len(data2['Enc. Position(deg)'])//3)]
            # Read the second CSV file for Y-axis data
            torque_tv_2 = data2['Torque(Mz)'].iloc[(len(data2['Torque(Mz)'])//3):2*(len(data2['Torque(Mz)'])//3)]
            # Apply moving average smoothing to X and Y data
            window_length = 600  # Adjust the window length as desired
            position_smoothed_tv_2 = position_tv_2.rolling(window_length, min_periods=1).mean()
            torque_smoothed_tv_2 = torque_tv_2.rolling(window_length, min_periods=1).mean()
            position_smoothed_tv_2 = position_smoothed_tv_2 + self.x_offset2
            torque_smoothed_tv_2 = torque_smoothed_tv_2 + self.y_offset2
            
            position_sampled2 = position_smoothed_tv_2.iloc[:len(position_smoothed_tv_2)//2:sampling_interval]
            torque_sampled2 = torque_smoothed_tv_2.iloc[:len(torque_smoothed_tv_2)//2:sampling_interval]
            dy_torque_sampled2 = torque_sampled2.diff().iloc[:].values   
            
            # Calculate the area under the curve
            area = np.trapz(torque_smoothed_tv.squeeze(), position_smoothed_tv.squeeze())
            area2 = np.trapz(torque_smoothed_tv_2.squeeze(), position_smoothed_tv_2.squeeze())
            
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
        
            # Plot the Spasticity
            self.fig.clear()
            ax = self.fig.add_subplot(121)
            ax.bar(position_sampled, dy_torque_sampled, alpha=0.3, label='Before')
            ax.bar(position_sampled2, dy_torque_sampled2,alpha=0.3, label='After')
            ax.set_xlabel('Position')
            ax.set_ylabel('Stiffness')
            ax.set_title('Stiffness at '+ self.figure_name[2])
            ax.legend()
            ax.grid()
            self.canvas.draw()
            
            # Plot the position-torque
            ax1 = self.fig.add_subplot(122)
            ax1.plot(position_smoothed_tv , torque_smoothed_tv , label = 'Before' )
            ax1.plot(position_smoothed_tv_2 , torque_smoothed_tv_2 , label = 'After')
            ax1.legend() # Show legend with data set names
            ax1.set_xlabel('Position (deg)')
            ax1.set_ylabel('Torque (Nm)')
            ax1.set_title('Passive ROM at ' + self.figure_name[2])
            ax1.grid(True)
            #self.fig.text(0.5, 0.99, chart_description, wrap=True, horizontalalignment='center', fontsize=8)
            ax1.text(0.98, 0.09, f'Energy Loss Before: {format(round(area,2))}', ha='right', va='top', transform=ax1.transAxes)
            ax1.text(0.98, 0.05, f'Energy Loss After: {format(round(area2,2))}', ha='right', va='top', transform=ax1.transAxes)
            self.canvas.draw()
        elif button_index == 3:
            data = pd.read_csv(self.data1_tv_directory[3])
            # Read the CSV file for X-axis data (position_tv)
            position_tv_w = data['Enc. Position(deg)']
            position_tv = position_tv_w.iloc[(len(position_tv_w)//3):2*(len(position_tv_w)//3)]
             # Read the CSV file for Y-axis data (torque_tv)
            torque_tv_w = data['Torque(Mz)']
            torque_tv = torque_tv_w.iloc[(len(torque_tv_w)//3):2*(len(torque_tv_w)//3)]
             # Apply moving average smoothing to X and Y data
            window_length = 600  
            position_smoothed_tv = position_tv.rolling(window_length, min_periods=1).mean()
            torque_smoothed_tv = torque_tv.rolling(window_length, min_periods=1).mean()
            position_smoothed_tv = position_smoothed_tv + self.x_offset
            torque_smoothed_tv = torque_smoothed_tv + self.y_offset
            
             # Calculate the spasticity by Sampling the data frame at the specified interval
            sampling_interval = 150
            position_sampled = position_smoothed_tv.iloc[:len(position_smoothed_tv)//2:sampling_interval]
            torque_sampled = torque_smoothed_tv.iloc[:len(torque_smoothed_tv)//2:sampling_interval]
            dy_torque_sampled = torque_sampled.diff().iloc[:].values
            
            data2 = pd.read_csv(self.data2_tv_directory[3])
            # Read the first CSV file for X-axis data
            position_tv_2 = data2['Enc. Position(deg)'].iloc[(len(data2['Enc. Position(deg)'])//3):2*(len(data2['Enc. Position(deg)'])//3)]
            # Read the second CSV file for Y-axis data
            torque_tv_2 = data2['Torque(Mz)'].iloc[(len(data2['Torque(Mz)'])//3):2*(len(data2['Torque(Mz)'])//3)]
            # Apply moving average smoothing to X and Y data
            window_length = 600  # Adjust the window length as desired
            position_smoothed_tv_2 = position_tv_2.rolling(window_length, min_periods=1).mean()
            torque_smoothed_tv_2 = torque_tv_2.rolling(window_length, min_periods=1).mean()
            position_smoothed_tv_2 = position_smoothed_tv_2 + self.x_offset2
            torque_smoothed_tv_2 = torque_smoothed_tv_2 + self.y_offset2
            position_sampled2 = position_smoothed_tv_2.iloc[:len(position_smoothed_tv_2)//2:sampling_interval]
            torque_sampled2 = torque_smoothed_tv_2.iloc[:len(torque_smoothed_tv_2)//2:sampling_interval]
            dy_torque_sampled2 = torque_sampled2.diff().iloc[:].values   
            
            # Calculate the area under the curve
            area = np.trapz(torque_smoothed_tv.squeeze(), position_smoothed_tv.squeeze())
            area2 = np.trapz(torque_smoothed_tv_2.squeeze(), position_smoothed_tv_2.squeeze())
            
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
        
            # Plot the Spasticity
            self.fig.clear()
            ax = self.fig.add_subplot(121)
            ax.bar(position_sampled, dy_torque_sampled, alpha=0.3, label='Before')
            ax.bar(position_sampled2, dy_torque_sampled2,alpha=0.3, label='After')
            ax.set_xlabel('Position')
            ax.set_ylabel('Stiffness')
            ax.set_title('Stiffness at '+ self.figure_name[3])
            ax.legend()
            ax.grid()
            self.canvas.draw()
            
            # Plot the position-torque
            ax1 = self.fig.add_subplot(122)
            ax1.plot(position_smoothed_tv , torque_smoothed_tv , label = 'Before' )
            ax1.plot(position_smoothed_tv_2 , torque_smoothed_tv_2 , label = 'After')
            ax1.legend() # Show legend with data set names
            ax1.set_xlabel('Position (deg)')
            ax1.set_ylabel('Torque (Nm)')
            ax1.set_title('Passive ROM at ' + self.figure_name[3])
            ax1.grid(True)
            #self.fig.text(0.5, 0.99, chart_description, wrap=True, horizontalalignment='center', fontsize=8)
            ax1.text(0.98, 0.09, f'Energy Loss Before: {format(round(area,2))}', ha='right', va='top', transform=ax1.transAxes)
            ax1.text(0.98, 0.05, f'Energy Loss After: {format(round(area2,2))}', ha='right', va='top', transform=ax1.transAxes)
            self.canvas.draw()
            
        elif button_index == 4:
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
    
            # Set the path to the directory containing the CSV files
            DataMvc = pd.read_csv(self.data1_tv_directory[4])
            DataMvc2 = pd.read_csv(self.data2_tv_directory[4])

            # Read the CSV file for Y-axis data (Torque)
            torque_mvc = DataMvc['Torque(Mz)']
            torque_mvc2 = DataMvc2['Torque(Mz)']

            # Apply moving average smoothing to X and Y data
            window_length = 200  
            time = np.linspace(0, 30, num=len(torque_mvc))
            torque = torque_mvc.rolling(window_length, min_periods=1).mean()
            time2 = np.linspace(0, 30, num=len(torque_mvc2))
            torque2 = torque_mvc2.rolling(window_length, min_periods=1).mean()
            
                
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

            # Find the index where the standard deviation is minimum
            min_std_index_f = rolling_std_first_third.idxmin()
            min_std_index_l = rolling_std_last_third.idxmin()

            min_std_index_f2 = rolling_std_first_third2.idxmin()
            min_std_index_l2 = rolling_std_last_third2.idxmin()

            # Get the mean value of the 2-second window with minimum standard deviation
            mean_of_min_std_window_f = rolling_mean_first_third.loc[min_std_index_f]
            mean_of_min_std_window_l = rolling_mean_last_third.loc[min_std_index_l]

            mean_of_min_std_window_f2 = rolling_mean_first_third2.loc[min_std_index_f2]
            mean_of_min_std_window_l2 = rolling_mean_last_third2.loc[min_std_index_l2]

            # Plot the data
            self.fig.clear()
            
            if self.buttons[7].isChecked() :
                torque2 = np.flipud(torque2.values)
                buffer2 = mean_of_min_std_window_f2
                mean_of_min_std_window_f2 = mean_of_min_std_window_l2
                mean_of_min_std_window_l2 = buffer2
    
            if self.buttons[8].isChecked():
                torque = np.flipud(torque.values)
                buffer = mean_of_min_std_window_f
                mean_of_min_std_window_f = mean_of_min_std_window_l
                mean_of_min_std_window_l = buffer
                
            ax3 = self.fig.add_subplot(111)
            ax3.plot(time,torque , label = 'Before')
            ax3.plot(time2,torque2 , label = 'After')
            ax3.set_xlabel('Time')
            ax3.set_ylabel('Torque (Nm)')
            ax3.set_title('MVC')
            ax3.grid(True)
            # Add the mean values as text on the chart
            ax3.text(0.3, 0.35, f'Dorsi Before: {round(mean_of_min_std_window_f,2)}', ha='right', va='top', transform=plt.gca().transAxes)
            ax3.text(0.3, 0.25, f'Plantar Before: {round(mean_of_min_std_window_l,2)}', ha='right', va='top', transform=plt.gca().transAxes)
            ax3.legend()
            ax3.text(0.3, 0.15, f'Dorsi After: {round(mean_of_min_std_window_f2,2)}', ha='right', va='top', transform=plt.gca().transAxes)
            ax3.text(0.3, 0.05, f'Plantar After: {round(mean_of_min_std_window_l2,2)}', ha='right', va='top', transform=plt.gca().transAxes)
            self.canvas.draw()


        elif button_index == 5:

            ################################## first data ################################

            # Read the text file
            file_path = self.folders1_tv_directory[5] + '\comment.txt'
            with open(file_path, 'r') as file:
                self.chart_description = file.read()
                
            # Set the chart description in the QTextEdit box
            self.chart_description_box.setText(self.chart_description)
            
            data_voluntary_w = pd.read_csv(self.data1_tv_directory[5])
            data_voluntary = data_voluntary_w['Position(rad)']

            # Apply moving average smoothing to X and Y data
            window_length = 200  # Adjust the window length as desired
            data_voluntary_smoothed = data_voluntary.rolling(window_length, min_periods=1).mean() * (180 / np.pi)
            #time = np.linspace(0,30,num= len(data_voluntary_smoothed))

            min_value = data_voluntary_smoothed.min()
            max_value = data_voluntary_smoothed.max()
            min_value_str = f'{min_value:.2f}'
            max_value_str = f'{max_value:.2f}'

            ################################## second data ################################
            # Set the path to the directory containing the CSV files
            # Read the text file
            #file_path2 = self.folders2_tv_directory[5] + '\comment.txt'
            #with open(file_path2, 'r') as file:
                #chart_description2 = file.read()

            data_voluntary_w2 = pd.read_csv(self.data2_tv_directory[5])
            data_voluntary2 = data_voluntary_w2['Position(rad)']

            # Apply moving average smoothing to X and Y data
            window_length = 100  # Adjust the window length as desired
            data_voluntary_smoothed2 = data_voluntary2.rolling(window_length, min_periods=1).mean()* (180 / np.pi)
            #time2 = np.linspace(0,30,num= len(data_voluntary_smoothed2))
            min_value2 = data_voluntary_smoothed2.min()
            max_value2 = data_voluntary_smoothed2.max()
            min_value_str2 = f'{min_value2:.2f}'
            max_value_str2 = f'{max_value2:.2f}'

            self.fig.clear()
            ax4 = self.fig.add_subplot(211)
            ax4.plot(data_voluntary_smoothed,label='Before')
            ax4.set_ylabel('Position (deg)')
            ax4.scatter(data_voluntary_smoothed.idxmax(), max_value, c='red', label='Max')
            ax4.scatter(data_voluntary_smoothed.idxmin(), min_value, c='green', label='Min')
            ax4.legend()
            #plt.ylabel('Feedback Torque (Nm)')
            ax4.set_title('Voluntary')
            ax4.grid(True)
            ax4.text(data_voluntary_smoothed.idxmax(), max_value, f'Max Before: {max_value_str}', ha='right', va='bottom', color='red')
            ax4.text(data_voluntary_smoothed.idxmin(), min_value, f'Min Before: {min_value_str}', ha='right', va='top', color='green')

            ax5 = self.fig.add_subplot(212)
            ax5.plot(data_voluntary_smoothed2, label='After')
            ax5.set_ylabel('Position (deg)')
            ax5.scatter(data_voluntary_smoothed2.idxmax(), max_value2, c='blue', label='Max')
            ax5.scatter(data_voluntary_smoothed2.idxmin(), min_value2, c='orange', label='Min')
            ax5.legend()
            ax5.text(data_voluntary_smoothed2.idxmax(), max_value2, f'Max After: {max_value_str2}', ha='right', va='bottom', color='blue')
            ax5.text(data_voluntary_smoothed2.idxmin(), min_value2, f'Min After: {min_value_str2}', ha='right', va='top', color='orange')
            ax5.grid(True)
            #ax5.tight_layout()  # Adjust the layout to prevent overlapping
            self.canvas.draw()

        elif button_index == 6:
            data_w = pd.read_csv(self.data1_tv_directory[0])
            data = data_w['Enc. Position(deg)'] + self.x_offset
            data2_w = pd.read_csv(self.data2_tv_directory[0])
            data2 = data2_w['Enc. Position(deg)'] + self.x_offset2
            # Read the neutral position_tv text file
            file_path_neutral_position_tv = self.DirectoryOfDataSet1 + '\\NeutralPosition.txt'
            with open(file_path_neutral_position_tv, 'r') as file2:
                Neutralposition_tv_before = file2.read()
            
           # Read the neutral position_tv text file
            file_path_neutral_position_tv_2 = self.DirectoryOfDataSet2 + '\\NeutralPosition.txt'
            with open(file_path_neutral_position_tv_2, 'r') as file2:
                Neutralposition_tv_after = file2.read() 
            
            self.chart_description = ' '
            # Set the chart description in the QTextEdit box
            self.chart_description_box.setText(self.chart_description)
            
            # bar chart
            
            dorsi1 = abs(data.max())
            plantar1 = abs(data.min())
            dorsi2 = abs(data2.max())
            plantar2 = abs(data2.min())
            dorsiImprovement = ((dorsi2 - dorsi1)/dorsi1)*100
            plantarImprovement = ((plantar2 - plantar1)/plantar1)*100
            x = ['dorsi_before','plantar_before']
            y = [dorsi1,plantar1]
            x2 = ['dorsi_after','plantar_after']
            y2 = [dorsi2,plantar2]
            self.fig.clear()
            ax6 = self.fig.add_subplot(121)
            ax6.bar(x,y)
            ax6.set_title('Passive ROM')
            ax6.set_ylabel('Position (deg)')
            ax6.text(0.3, 0.98, f'NP: {abs(round(float(Neutralposition_tv_before),0))}', ha='right', va='top', transform=plt.gca().transAxes)
            ax7 = self.fig.add_subplot(122)
            ax7.bar(x2,y2, color = 'orange')
            ax7.set_title('Passive ROM')
            ax7.set_ylabel('Position (deg)')
            ax7.text(0.3, 0.98, f'NP: {abs(round(float(Neutralposition_tv_after),0))}', ha='right', va='top', transform=plt.gca().transAxes)
            ax7.text(0.3, 0.88, f'DI: {round(float(dorsiImprovement),0)} %', ha='right', va='top', transform=plt.gca().transAxes) 
            ax7.text(0.3, 0.78, f'PI: {round(float(plantarImprovement),0)} %', ha='right', va='top', transform=plt.gca().transAxes) 
            self.canvas.draw()

            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
