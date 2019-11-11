# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(400, 450)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setFocusPolicy(QtCore.Qt.NoFocus)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("bF.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.Russian, QtCore.QLocale.Russia))
        MainWindow.setWindowFilePath("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setEnabled(True)
        self.textBrowser.setToolTip("")
        self.textBrowser.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.textBrowser.setAutoFillBackground(False)
        self.textBrowser.setAcceptRichText(True)
        self.textBrowser.setOpenLinks(False)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(True)
        self.progressBar.setAutoFillBackground(False)
        self.progressBar.setProperty("value", 25)
        self.progressBar.setTextVisible(False)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.boxLanguage = QtWidgets.QComboBox(self.centralwidget)
        self.boxLanguage.setEditable(False)
        self.boxLanguage.setObjectName("boxLanguage")
        self.horizontalLayout_2.addWidget(self.boxLanguage)
        self.boxLogging = QtWidgets.QCheckBox(self.centralwidget)
        self.boxLogging.setTabletTracking(False)
        self.boxLogging.setChecked(True)
        self.boxLogging.setObjectName("boxLogging")
        self.horizontalLayout_2.addWidget(self.boxLogging)
        self.boxSilentMode = QtWidgets.QCheckBox(self.centralwidget)
        self.boxSilentMode.setChecked(True)
        self.boxSilentMode.setObjectName("boxSilentMode")
        self.horizontalLayout_2.addWidget(self.boxSilentMode)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 400, 21))
        self.menuBar.setDefaultUp(False)
        self.menuBar.setNativeMenuBar(True)
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menuBar)
        self.actionOpenFile = QtWidgets.QAction(MainWindow)
        self.actionOpenFile.setObjectName("actionOpenFile")
        self.actionOpenFolder = QtWidgets.QAction(MainWindow)
        self.actionOpenFolder.setObjectName("actionOpenFolder")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionClearWindow = QtWidgets.QAction(MainWindow)
        self.actionClearWindow.setObjectName("actionClearWindow")
        self.menuFile.addAction(self.actionOpenFile)
        self.menuFile.addAction(self.actionOpenFolder)
        self.menuFile.addAction(self.actionClearWindow)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.actionClearWindow.triggered.connect(self.textBrowser.clear)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "bFix"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Hello there</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">General Kenobi</p></body></html>"))
        self.progressBar.setToolTip(_translate("MainWindow", "<html><head/><body><p>FolderScan bar</p></body></html>"))
        self.progressBar.setFormat(_translate("MainWindow", "%v / %m"))
        self.boxLogging.setText(_translate("MainWindow", "Logging"))
        self.boxSilentMode.setText(_translate("MainWindow", "Silent mode"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpenFile.setText(_translate("MainWindow", "Open File"))
        self.actionOpenFolder.setText(_translate("MainWindow", "Open Folder"))
        self.actionExit.setText(_translate("MainWindow", "EXIT"))
        self.actionClearWindow.setText(_translate("MainWindow", "Clear Window"))
