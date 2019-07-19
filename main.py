import sys
from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout,QDial,QMainWindow, QFileDialog,QListWidgetItem)
from PySide2 import QtCore, QtUiTools
from video import Ui_MainWindow
from PySide2.QtCore import QUrl,QTime,QFileInfo
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent,QMediaPlaylist

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Create widgets
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.mediaPlayer = QMediaPlayer()
        self.playlist = QMediaPlaylist()




        #mediaContent1 = QMediaContent(QUrl.fromLocalFile("big_buck_bunny.avi"))
        #mediaContent2=QMediaContent(QUrl.fromLocalFile("Doom.Patrol1.mp4"))
        #self.playlist.addMedia(mediaContent1)
        #self.playlist.addMedia(mediaContent2)
        #self.playlist.setCurrentIndex(1)


        #self.mediaPlayer.setMedia(self.playlist)
        self.mediaPlayer.setVideoOutput(self.ui.wvideo)

        self.ui.ltemps.setText("")
        self.ui.lduree.setText("")
        self.ui.dialVolume.setValue(0)
        self.ui.lvolume_2.setText(str(self.ui.dialVolume.value()))

        self.ui.pblecture.clicked.connect(self.lectureClicked)
        self.ui.pbpause.clicked.connect(self.pauseClicked)
        self.ui.pbstop.clicked.connect(self.stopClicked)
        self.ui.pbsuivant.clicked.connect(self.suivantClicked)
        self.ui.pbprecedent.clicked.connect(self.precedentClicked)
        self.ui.pbajouter.clicked.connect(self.ajouter2)
        self.ui.pbsupprimer.clicked.connect(self.supprimer)
        self.ui.listWidget.itemDoubleClicked.connect(self.mediaSelected2)

        self.ui.dialVolume.valueChanged.connect(self.volumeChanged)
        #self.mediaPlayer.positionChanged.connect(self.tempsChanged)

        self.mediaPlayer.positionChanged.connect(self.lectureEnCours)
        #self.mediaPlayer.positionChanged.connect(self.progressionChanged)
        self.ui.stpscourant.sliderMoved.connect(self.sliderMove)


    def sliderMove(self):
        self.mediaPlayer.setPosition(self.ui.stpscourant.value())

    def lectureEnCours(self):
        mediaPosition = self.mediaPlayer.position()
        currentTimeMedia =QTime(0,0,0)

        currentTimeMedia = currentTimeMedia.addMSecs(mediaPosition)
        mediaDuration = self.mediaPlayer.duration()
        totalTimeMedia = QTime(0,0,0)
        totalTimeMedia = totalTimeMedia.addMSecs(mediaDuration)
        self.ui.ltemps.setText(currentTimeMedia.toString("HH:mm:ss"))
        self.ui.lduree.setText(totalTimeMedia.toString("HH:mm:ss"))
        self.ui.stpscourant.setRange(0, self.mediaPlayer.duration())
        self.ui.stpscourant.setValue(self.mediaPlayer.position())

    def lectureClicked(self):
        print("Lecture!!")
        self.mediaPlayer.play()

    def pauseClicked(self):
        print("pause!!")
        if self.mediaPlayer.state()==QMediaPlayer.PausedState:
            self.mediaPlayer.play()
        else:
            self.mediaPlayer.pause()

    def stopClicked(self):
        print("stop!!")
        self.mediaPlayer.stop()

    def suivantClicked(self):
        print("suivant!!")
        currentItemRow = self.ui.listWidget.currentRow()
        if currentItemRow == -1:
            return
        totalItems = self.ui.listWidget.count()
        self.ui.listWidget.setCurrentRow((currentItemRow+1)%totalItems)
        self.mediaSelected2()


    def precedentClicked(self):
        print("precedent!!")
        currentItemRow = self.ui.listWidget.currentRow()
        if currentItemRow == -1:
            return
        totalItems = self.ui.listWidget.count()
        self.ui.listWidget.setCurrentRow((currentItemRow -1) % totalItems)
        self.mediaSelected2()

    def volumeChanged(self):
        self.ui.dialVolume.setMaximum(100)
        self.mediaPlayer.setVolume(self.ui.dialVolume.value())
        self.ui.lvolume_2.setText(str(self.ui.dialVolume.value()))

    def ajouter(self):
        nomMedia = QFileDialog.getOpenFileName(self,"Choix Film", "C:/Users/AELION/PycharmProjects/videoLHector", "Movie Files (*.avi *.mp4)")
        item = QListWidgetItem(nomMedia[0])
        self.ui.listWidget.addItem(item)

    def ajouter2(self):
        nomMedia = QFileDialog.getOpenFileName(self, "Choix Film", "C:/Users/AELION/PycharmProjects/videoLHector", "Movie Files (*.avi *.mp4)")
        fInfo = QFileInfo(nomMedia[0])
        fShortName = fInfo.baseName()
        print(fShortName)
        item = QListWidgetItem(fShortName)
        item.setToolTip(nomMedia[0])
        self.ui.listWidget.addItem(item)

    def supprimer(self):
        rowItem = self.ui.listWidget.currentRow()
        if rowItem != -1:
            self.ui.listWidget.takeItem(rowItem)

    def mediaSelected1(self):
        currentItem = self.ui.listWidget.currentItem()
        mediaContent = QMediaContent(QUrl.fromLocalFile(currentItem.text()))
        self.mediaPlayer.setMedia(mediaContent)
        self.lectureClicked()

    def mediaSelected2(self):
        currentItem = self.ui.listWidget.currentItem()
        mediaContent = QMediaContent(QUrl.fromLocalFile(currentItem.toolTip()))
        self.mediaPlayer.setMedia(mediaContent)
        self.lectureClicked()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())