from PySide2 import QtGui, QtCore, QtWidgets

JSON_FILES = "JSON Files (*.json)"

def activeWindow():
    return QtWidgets.QApplication.activeWindow()


def showInfo(title, message):
    QtWidgets.QMessageBox.information(activeWindow(), title, message)


def userSelectedFile(title, filePattern, mustExist=True):
    if mustExist:
        fileName = QtWidgets.QFileDialog.getOpenFileName(
            activeWindow(), title, '', filePattern)[0]
    else:
        fileName = QtWidgets.QFileDialog.getSaveFileName(
            activeWindow(), caption=title, filter=filePattern)[0]

    if fileName == '':
        return None

    return fileName
