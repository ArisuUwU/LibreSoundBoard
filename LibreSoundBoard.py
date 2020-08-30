#!/usr/bin/env python3
"""
LibreSoundBoard
Copyright (C) 2020  ArisuTheWired

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import sys
import subprocess
from os import listdir
from os.path import isfile, join
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, 
    QDesktopWidget, QLabel, QGridLayout, QPushButton, QDialog, QLabel)
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon

VERSION = "1.0.0"

#  This can be found here:
#  $ pactl list short sinks
AUDIOSERVICE = "pulse"
AUDIODEVICE = 'alsa_output.pci-0000_00_1b.0.analog-stereo'
class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        self.center()
        self.setWindowTitle('LibreSoundBoard')
        self.setWindowIcon(QIcon('icon.png'))
        self.mainwidget = LibreSoundBoard()
        self.setCentralWidget(self.mainwidget)
        self.show()
        
    def center(self):
        geo = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        geo.moveCenter(centerPoint)
        self.move(geo.topLeft())

    #Makes sure that any background process is stopped when the program exits
    def closeEvent(self, event):
        self.mainwidget.playingSound.terminate()
        event.accept()

class LibreSoundBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.playingSound = subprocess.Popen(["echo"], stdout=subprocess.PIPE)#dummy
        self.sounds = [soundFile for soundFile in listdir('sounds') if isfile(join('sounds', soundFile))]
        self.sounds.sort()
        column = 0
        row = 0
        grid = QGridLayout()
        grid.setSpacing(10)
        buttons = []
        for i in range(len(self.sounds)):
            buttons.append(QPushButton(self.sounds[i], self))
            #we need state after lambda because the button returns the button state and messes with the function
            #we also cant pass i alone because i gets overwritten with lambda for some reason (ie will always be what i was last on loop exit)
            #because of this, we assign i to a and pass a to the function. this sticks.
            buttons[i].clicked.connect(lambda state, a=i : self.playSound(a))
            grid.addWidget(buttons[i], row, column)
            if(column > 3):
                row += 1
                column = 0
            else:
                column += 1
        stop = QPushButton("Stop Sound", self)
        stop.clicked.connect(lambda : self.playingSound.terminate())
        grid.addWidget(stop, row+1, 0, 1, -1)
        self.setLayout(grid)
    #stops the ffmpeg process and puts a new one into the background.
    def playSound(self, index):
        self.playingSound.terminate()
        self.playingSound=subprocess.Popen(["ffmpeg", "-i", "sounds/" + self.sounds[index], "-f", AUDIOSERVICE, "-device", AUDIODEVICE, "'LibreSoundBoard'"], stdout=subprocess.PIPE)

if __name__ == '__main__':
    print("LibreSoundBoard version " + VERSION)
    app = QApplication(sys.argv)
    libreSoundBoard = Application()
    sys.exit(app.exec_())
