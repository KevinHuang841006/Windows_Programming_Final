from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

#Create by Po-Hao  button features~~~  for the button  
import button_feature


import sys
from os import path
import time
import cv2
import numpy as np

tooth_flag=0

class RecordVideo(QtCore.QObject):
    image_data = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, camera_port=0, parent=None):
        super().__init__(parent)
        self.camera = cv2.VideoCapture(camera_port)

        self.timer = QtCore.QBasicTimer()

    def start_recording(self):
        self.timer.start(0, self)

    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return

        read, data = self.camera.read()
        if read:
            self.image_data.emit(data)


class FaceDetectionWidget(QtWidgets.QWidget):
    def __init__(self, haar_cascade_filepath, parent=None):
        super().__init__(parent)
        self.classifier = cv2.CascadeClassifier(haar_cascade_filepath)
        self.image = QtGui.QImage()
        self._red = (0, 0, 255)
        self._width = 2
        self._min_size = (30, 30)

    def detect_faces(self, image: np.ndarray):
        # haarclassifiers work better in black and white
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.equalizeHist(gray_image)

        faces = self.classifier.detectMultiScale(gray_image,
                                                 scaleFactor=1.3,
                                                 minNeighbors=4,
                                                 flags=cv2.CASCADE_SCALE_IMAGE,
                                                 minSize=self._min_size)

        return faces

    def image_data_slot(self, image_data):
        faces = self.detect_faces(image_data)
        tests = np.array(image_data)
        #print(tests.shape)
        #time.sleep(2)
        #tests = RUN.img_reshape(tests)
        #RUN.teeth_detection(tests)
        """
          Edit here~~~~  image dim : 480 * 640 *3
          teeth detection block~
          image_data = reshape(image_data)         # to 224 * 224 * 3
          id = teeth_detection(image_data)         # do teeth detection
          print(id)                                # the id of teeth
        """
        tests = tests[40:460,160:520,:]
        cv2.imwrite('test1.jpg',tests)
        time.sleep(0.1)
        #print(tests.shape)
        #time.sleep(2)
        
        #draw rectangle
        """
        for (x, y, w, h) in faces:
            cv2.rectangle(image_data,
                          (x, y),
                          (x+w, y+h),
                          self._red,
                          self._width)
        cv2.imwrite('face_segment.jpg',tests)
        """
        self.image = self.get_qimage(image_data)
        if self.image.size() != self.size():
            self.setFixedSize(self.image.size())

        self.update()

    def get_qimage(self, image: np.ndarray):
        height, width, colors = image.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage
        #print(image.shape)
        image = QImage(image.data,
                       width,
                       height,
                       bytesPerLine,
                       QImage.Format_RGB888)

        image = image.rgbSwapped()
        return image

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()


# GUI Design here~~~~~~~~~~
class MainWidget(QtWidgets.QWidget):
    def __init__(self, haarcascade_filepath, parent=None):
        super().__init__(parent)
        fp = haarcascade_filepath
        self.face_detection_widget = FaceDetectionWidget(fp)

        
        self.record_video = RecordVideo()
        
        
        image_data_slot = self.face_detection_widget.image_data_slot
        self.record_video.image_data.connect(image_data_slot)

        layout = QtWidgets.QVBoxLayout()
        
        #First Item
        layout.addWidget(self.face_detection_widget)
        
        #Second
        self.textbox = QtWidgets.QLineEdit(self)
        layout.addWidget(self.textbox)
        
        #Third
        self.run_button = QtWidgets.QPushButton('Start')
        layout.addWidget(self.run_button)
        
        
        #Forth add Re_label text
        relabel_layout = QtWidgets.QHBoxLayout()
        self.label1 = QtWidgets.QLabel()
        self.label1.setText("\n")
        self.label1.setText("Relabel~~~")
        self.label1.setFixedWidth(70)
        self.label_textbox = QtWidgets.QLineEdit("non")
        self.label_textbox.setFixedWidth(40)
        relabel_layout.addWidget(self.label1, QtCore.Qt.AlignLeft)
        relabel_layout.addWidget(self.label_textbox, QtCore.Qt.AlignLeft)
        layout.addLayout(relabel_layout, QtCore.Qt.AlignLeft)
        
        #Fifth
        self.reset_button = QtWidgets.QPushButton('reset_button')
        layout.addWidget(self.reset_button)
        
        #Sixth
        layout2 = QtWidgets.QHBoxLayout()
        self.button1 = QtWidgets.QPushButton('1')
        self.button2 = QtWidgets.QPushButton('2')
        self.button3 = QtWidgets.QPushButton('3')
        self.button4 = QtWidgets.QPushButton('4')
        layout2.addWidget(self.button1)
        layout2.addWidget(self.button2)
        layout2.addWidget(self.button3)
        layout2.addWidget(self.button4)
        layout.addLayout(layout2)
        
        layout3 = QtWidgets.QHBoxLayout()
        self.button5 = QtWidgets.QPushButton('5')
        self.button6 = QtWidgets.QPushButton('6')
        self.button7 = QtWidgets.QPushButton('7')
        self.button8 = QtWidgets.QPushButton('8')
        layout3.addWidget(self.button5)
        layout3.addWidget(self.button6)
        layout3.addWidget(self.button7)
        layout3.addWidget(self.button8)
        layout.addLayout(layout3)


        # Edit here~~~~~ graphic, line chart
        self.empty_label = QtWidgets.QLabel()
        layout.addWidget(self.empty_label)
        self.total_result_button = QtWidgets.QPushButton('total_result')
        layout.addWidget(self.total_result_button)
        
        current_layout = QtWidgets.QHBoxLayout()
        self.current_result_ComboBox = QtWidgets.QComboBox()
        self.current_result_ComboBox.addItem('Action_1')
        self.current_result_ComboBox.addItem('Action_2')
        self.current_result_ComboBox.addItem('Action_3')
        self.current_result_ComboBox.addItem('Action_4')
        self.current_result_ComboBox.addItem('Action_5')
        self.current_result_ComboBox.addItem('Action_6')
        self.current_result_ComboBox.addItem('Action_7')
        self.current_result_ComboBox.addItem('Action_8')
        self.current_label = QtWidgets.QLabel('Current Result:')
        current_layout.addWidget(self.current_label)
        current_layout.addWidget(self.current_result_ComboBox)
        layout.addLayout(current_layout)
        
        #ADD annotation
        self.current_list = QtWidgets.QListWidget()
        self.current_list.addItem('Some Tips~~~')
        self.current_list.addItem('test1')
        self.current_list.addItem('test2')
        self.current_list.addItem('test3')
        layout.addWidget(self.current_list)
        
        
        self.run_button.clicked.connect(self.record_video.start_recording)
        self.reset_button.clicked.connect(self.reset_button1)
        self.button1.clicked.connect(self.push_button1)
        self.button2.clicked.connect(self.push_button2)
        
        
        
        self.current_result_ComboBox.activated[str].connect(self.onActivated) 
        
        
        self.setLayout(layout)
    
    def onActivated(self,text):
        print(text)
    
    def reset_button1(self):
        tooth_flag=0
        self.label_textbox.setText("non")
        button_feature.set_flag(tooth_flag)
    def push_button1(self):
        tooth_flag=1
        self.label_textbox.setText("1")
        button_feature.set_flag(tooth_flag)
    def push_button2(self):
        tooth_flag=2
        self.label_textbox.setText("2")
        button_feature.set_flag(tooth_flag)

def main(haar_cascade_filepath):
    app = QtWidgets.QApplication(sys.argv)

    main_window = QtWidgets.QMainWindow()
    main_widget = MainWidget(haar_cascade_filepath)
    main_window.setCentralWidget(main_widget)
    main_window.show()
    sys.exit(app.exec_())

#Start from heere~~~~
if __name__ == '__main__':
    #RUN.printf()
    cascade_filepath = path.abspath('haarcascade_frontalface_default.xml')
    #print(path.abspath(find()))
    main(cascade_filepath)
