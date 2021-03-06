import sys
import os
import time
import datetime
import glob
import chardet
import configparser
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QThread
from shutil import move
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import PatternMatchingEventHandler

import design

defCfgVal = {
    "logging" : "True",
    "silentmode" : "True",
    "silenttray" : "False",
    "starttray" : "False",
    "showsettings" : "True",
    "workfolder" : "C:/WNC/user/iso",
    "externallanguage" : "None",
    "externalbadwords" : "None"
    }

defLngVal = {
    "head" : "Program launch",
    "emptywordfile" : "The dictionary of broken words is empty !!!",
    "trackedfolder" : "Tracked Folder: ",
    "hookedfile" : "Hooked file: ",
    "menu" : "Menu",
    "openfilebutton" : "Open file",
    "openfiledescription" : "Fix file",
    "openfolderbutton" : "Open folder",
    "openfolderdescription" : "Fix files in folder",
    "clearbutton" : "Clear window",
    "cleardescription" : "Clear text window",
    "exitbutton" : "Exit",
    "exitdescription" : "Exit the program",
    "file" : "File: ",
    "time" : "Time: ",
    "decode" : "Change encoding: ",
    "corruptedword1" : "Corrupted word: ",
    "corruptedword2" : "Fixed on: ",
    "corruptedword3" : "Number of fixes: ",
    "folder" : "Folder: ",
    "founded" : "Files found: ",
    "fixed" : "Fixed files: ",
    "logbutton" : "Logging",
    "silent" : "Silent mode",
    "done" : "Done",
    "showwindow" : "Show",
    "closewindow" : "Close",
    "yes" : "Yes",
    "no" : "No",
    "exitmsg" : "Are you sure you want to quit?",
    "about" : "About"
    }

def resource_path(relative):

    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    else:
        return os.path.join(os.path.abspath("."), relative)

class myIntarface(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.textBrowser.clear()
        self.progressBar.hide()
        self.textAbout.hide()
        self.pushButtonOk.hide()
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.config.optionxform = str
        self.brokenWordCount = 0
        self.preUI()
        self.initConfig()
        self.guiLanguage()
        self.postUI()
        self.initConnect()
        self.observer = Observer()
        self.myobserver = myObserver(self)
        self.observer.schedule(self.myobserver, path=self.config.get("CONFIG",'workfolder'), recursive=True)
        self.observer.start()

    #Initialize programm
        
    def initConfig(self):
        if not os.path.exists('config.cfg'):
            with open('config.cfg', 'w+', encoding="utf-8") as defaultCfg:
                defaultCfg.close()
        
        self.config.read('config.cfg',encoding="utf-8")
        
        if not self.config.has_section("CONFIG"):
            self.config.add_section("CONFIG")
        for key, val in defCfgVal.items():
            if (not self.config.has_option("CONFIG", key)) or (self.config.get("CONFIG", key) == None):
                self.config.set("CONFIG", key, val)

        if not self.config.has_section("LANGUAGE"):
            self.config.add_section("LANGUAGE")
        for key, val in defLngVal.items():
            if (not self.config.has_option("LANGUAGE", key)) or (self.config.get("LANGUAGE", key) == None):
                self.config.set("LANGUAGE", key, val)

        if not self.config.has_section("BROKEN WORDS"):
            self.config.add_section("BROKEN WORDS")
            self.config.set("BROKEN WORDS", ";Dictionary of corrupted words")
        self.updateCfg()

        if self.config.get("CONFIG", "externallanguage") != None and self.config.get("CONFIG", "externallanguage") != "None":
            customLang = configparser.ConfigParser(allow_no_value=True)
            customLang.optionxform = str
            try:
                customLang.read(self.config.get("CONFIG", "externallanguage"),encoding="utf-8")
                if customLang.has_section("LANGUAGE"):
                    for key in customLang.options("LANGUAGE"):
                        if customLang.get("LANGUAGE",key) == None:
                            continue
                        self.config.set("LANGUAGE",key, customLang.get("LANGUAGE",key))
            except:
                pass

        if self.config.get("CONFIG", "externalbadwords") != None and self.config.get("CONFIG", "externalbadwords") != "None":
            customWords = configparser.ConfigParser(allow_no_value=True)
            customWords.optionxform = str
            try:
                customWords.read(self.config.get("CONFIG", "externalbadwords"),encoding="utf-8")
                if customWords.has_section("BROKEN WORDS"):
                    for key in customWords.options("BROKEN WORDS"):
                        if customWords.get("BROKEN WORDS",key) == None:
                            continue
                        self.config.set("BROKEN WORDS",key, customWords.get("BROKEN WORDS",key))
                        self.brokenWordCount += 1
            except:
                pass

        
        for sector in self.config.sections():
            for key in self.config.options(sector):
                if self.config[sector][key] == None:
                    self.config.remove_option(sector, key)
        
                    
    def updateCfg(self):
        with open("config.cfg", "w", encoding="utf-8") as config_file:
            self.config.write(config_file)
            config_file.close()

    def preUI(self):
        self.bFixIco = QtGui.QIcon(resource_path('bF.png'))
        icon = QtGui.QIcon()
        self.setWindowIcon(self.bFixIco)
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.bFixIco)
        #self.tray_icon.show()
        self.actionShow = QtWidgets.QAction("Show", self)
        #self.actionHide = QtWidgets.QAction("Hide", self)
        self.actionClose = QtWidgets.QAction("Close", self)
        self.actionShow.triggered.connect(self.show)
        #self.actionHide.triggered.connect(self.hide)
        self.actionClose.triggered.connect(self.close)
        self.tray_menu = QtWidgets.QMenu()
        self.tray_menu.addAction(self.actionShow)
        #self.tray_menu.addAction(self.actionHide)
        self.tray_menu.addAction(self.actionClose)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.useTray = False

    def showEvent(self, event):
        self.useTray = False
        self.showNormal()
        self.tray_icon.hide()
    def hideEvent(self, event):
        self.useTray = True
        self.hide()
        self.tray_icon.show()
    def closeEvent(self, event):
        self.tray_icon.hide()
        self.tray_icon.destroy()

    #GUI stuff

    def guiLanguage(self):
        #self.config.get("LANGUAGE",msg)
        #self.config["LANGUAGE"][msg]
        
        self.menuFile.setTitle(self.config["LANGUAGE"]['menu'])
        self.actionOpenFile.setText(self.config["LANGUAGE"]['openfilebutton'])
        #self.actionOpenFile.setToolTip(self.config["LANGUAGE"]['openfiledescription'])
        self.actionOpenFolder.setText(self.config["LANGUAGE"]['openfolderbutton'])
        #self.actionOpenFolder.setToolTip(self.config["LANGUAGE"]['openfolderdescription'])
        self.actionClearWindow.setText(self.config["LANGUAGE"]['clearbutton'])
        #self.actionClearWindow.setToolTip(self.config["LANGUAGE"]['cleardescription'])
        self.actionAbout.setText(self.config["LANGUAGE"]['about'])
        self.actionExit.setText(self.config["LANGUAGE"]['exitbutton'])
        #self.actionExit.setToolTip(str(self.LNG['exitdescription'])
        self.boxLogging.setText(self.config["LANGUAGE"]['logbutton'])
        self.boxSilentMode.setText(self.config["LANGUAGE"]['silent'])
        self.actionShow.setText(self.config["LANGUAGE"]['showwindow'])
        self.actionClose.setText(self.config["LANGUAGE"]['closewindow'])

        self.textBrowser.append(self.config["LANGUAGE"]['head']+'\n'+
                                self.config["LANGUAGE"]['trackedfolder']+" "+
                                self.config["CONFIG"]['workfolder']+'\n')
        self.logging(self.config["LANGUAGE"]['head'])
        self.logging(self.config["LANGUAGE"]['trackedfolder']+self.config["CONFIG"]['workfolder'])

        for key in self.config.options("BROKEN WORDS"):
            self.brokenWordCount += 1
        if self.brokenWordCount == 0:
            self.textBrowser.append(self.config["LANGUAGE"]["emptywordfile"])
        
    def postUI(self):
        if not self.config.getboolean("CONFIG",'showsettings'):
            self.boxLogging.hide()
            self.boxSilentMode.hide()
            self.boxLanguage.hide()
        if self.config.getboolean("CONFIG",'starttray'):
            self.useTray = True
            self.hide()
            self.tray_icon.show()
        else:
            self.show()

    def initConnect(self):
        self.boxLogging.toggle()
        if self.config.getboolean("CONFIG",'logging'):
            self.boxLogging.setCheckState(Qt.Checked)
        self.boxLogging.stateChanged.connect(self.updateLogButton)

        self.boxSilentMode.toggle()
        if self.config.getboolean("CONFIG",'silentmode') == 'True':
            self.boxSilentMode.setCheckState(Qt.Checked)
        self.boxSilentMode.stateChanged.connect(self.updateSilentButton)

        self.actionOpenFile.triggered.connect(self.openFile)
        self.actionOpenFolder.triggered.connect(self.openFolder)
        self.actionExit.triggered.connect(QtWidgets.qApp.quit)

    def updateLogButton(self, state):
        if state == Qt.Checked:
            self.config.set("CONFIG",'logging','True')
        else:
            self.config.set("CONFIG",'logging','False')
        self.updateCfg()

    def updateSilentButton(self, state):
        if state == Qt.Checked:
            self.config.set("CONFIG",'silentmode','True')
        else:
            self.config.set("CONFIG",'silentmode','False')
        self.updateCfg()

    def openFile(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, '', '', 'CNI (*.cni)')[0]
        if len(fname) > 0:
            self.myobserver.openExternalFile(fname)

    def openFolder(self):
        filename = QtWidgets.QFileDialog.getExistingDirectory(self, '')
        if len(filename) > 0:
            self.myobserver.openExternalFolder(filename)

    def logging(self, msg):
        if not self.config.getboolean("CONFIG",'logging'): return

        if not os.path.exists('program.log'):
            with open('program.log', 'w+', encoding="utf-8") as newLog: newLog.close()

        with open('program.log', 'a+', encoding="utf-8") as log:
            if type(msg) == str or type(msg) == int or type(msg) == float or type(msg) == bool:
                log.write(str(datetime.datetime.now())+' '+str(msg)+'\n')
            elif type(msg) == list:
                bFirst = False
                for line in msg:
                    if not bFirst:
                        log.write(str(datetime.datetime.now())+' '+str(line).replace('\\','/')+'\n')
                        bFirst = True
                    else:
                        log.write('\t'+str(line).replace('\\','/')+'\n')
            elif type(msg) == dict:
                bFirst = False
                for k, *v in msg:
                    if not bFirst:
                        log.write(str(datetime.datetime.now())+'\n')
                        bFirst = True
                    else:
                        log.write('\t'+str(k)+'  '+str(v)+'\n')
            else:
                log.write('[ERROR] Unknown msg type\n')
            log.close()

    def addTextToWindow(self, lst):
        for line in lst:
            self.textBrowser.append(str(line).replace('\\','/'))
            
        if self.useTray and not self.config.getboolean("CONFIG",'silenttray'):
            msgHead = str()
            msgBody = str()
            for line in lst:
                if len(msgHead) == 0:
                    msgHead = line.replace(self.config.get("LANGUAGE","hookedfile"),'').replace(self.config.get("CONFIG","workfolder"),'').replace('\\','').replace('/','')
                else:
                    if len(msgBody) == 0:
                        msgBody = line.replace('\t','')
                    else:
                        msgBody = msgBody + '\n' + line
                    
            self.tray_icon.showMessage(msgHead,msgBody,self.bFixIco)
        self.logging(lst)
        horScrollBar = self.textBrowser.horizontalScrollBar()
        verScrollBar = self.textBrowser.verticalScrollBar()
        scrollIsAtEnd = verScrollBar.maximum() - verScrollBar.value() >= 10

        if scrollIsAtEnd:
            verScrollBar.setValue(verScrollBar.maximum()) # Scrolls to the bottom
            horScrollBar.setValue(0) # scroll to the left

    def activateBar(self, maxCount):
        self.progressBar.setMaximum(maxCount)
        self.progressBar.setValue(0)
        self.progressBar.show()

    def updateBar(self, value):
        self.progressBar.setValue(value)

    def deactivateBar(self):
        self.progressBar.hide()
        self.progressBar.setMaximum(0)
        self.progressBar.setValue(0)

class copyFolderThread(QThread):
    def __init__(self, observ):
        super().__init__()
        self.observ = observ
        self.folderList = list()
        self.MSG = []

    def addFolder(self, fname):
        self.folderList.append(fname)
        self.start()

    def run(self):
        if not len(self.folderList):
            return
        self.observ.ui.actionOpenFolder.setEnabled(False)
        for folderpath in self.folderList:
            print(folderpath)
            fileList = glob.glob(folderpath+'\\*.cni')
            #print(fileList)
            fileCount = len(fileList)
            self.observ.ui.activateBar(fileCount)
            counter = 0
            fixedCounter = 0
            self.MSG.append(self.observ.ui.config.get("LANGUAGE",'folder')+folderpath)
            self.MSG.append(self.observ.ui.config.get("LANGUAGE",'founded')+str(fileCount))
            self.MSG.append('\n')
            self.observ.ui.addTextToWindow(self.MSG)
            self.MSG.clear()
            for line in fileList:
                counter += 1
                QThread.msleep(10)
                if self.observ.fixfile(line)>0:
                    fixedCounter += 1
                self.observ.ui.updateBar(counter)
                if not self.observ.ui.config.getboolean("CONFIG",'silentmode'):
                    self.MSG.insert(0,self.observ.ui.config.get("LANGUAGE",'file')+line)
                    self.MSG.append('\n')
                    self.observ.ui.addTextToWindow(self.MSG)
                self.MSG.clear()
            self.observ.ui.deactivateBar()
            self.MSG.append(self.observ.ui.config.get("LANGUAGE",'fixed')+str(fixedCounter))
            self.MSG.append(self.observ.ui.config.get("LANGUAGE",'done'))
            self.observ.ui.addTextToWindow(self.MSG)
            self.MSG.clear()
        self.folderList.clear()
        self.observ.ui.actionOpenFolder.setEnabled(True)
        

class myObserver(PatternMatchingEventHandler):
    patterns = ["*.cni", "*.CNI"]
    def __init__(self, interface):
        super().__init__()
        self.ui = interface
        self.MSG = []
        self.TmpTime = datetime.datetime.now()
        self.TmpTimeOld = self.TmpTime
        self.TmpName = []
        self.TmpNameOld = []
        self.copyThread = copyFolderThread(self)

    def on_modified(self, event):
        self.filetrack(event)

    def on_moved(self, event):
        self.filetrack(event)

    def on_created(self, event):
        self.filetrack(event)

    def filetrack(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        
        self.TmpTime = datetime.datetime.now()
        self.TmpName = event.src_path

        if (self.TmpTime-self.TmpTimeOld).seconds < 2 and self.TmpName == self.TmpNameOld:
            return

        self.fixfile(event.src_path)
        if len(self.MSG) >0:
            self.MSG.insert(0, self.ui.config.get("LANGUAGE",'hookedfile')+event.src_path)
            self.ui.addTextToWindow(self.MSG)
        self.MSG.clear()
        self.TmpTimeOld = self.TmpTime
        self.TmpNameOld = self.TmpName

    def fixfile(self, filepath):
        #filepath = filepath.replace('\u005C','/')
        fixed = 0
        fixed += self.isDecode(filepath)
        if self.ui.brokenWordCount > 0:
            for key in self.ui.config.options("BROKEN WORDS"):
                fixed += self.isReplaceWord(filepath, key, self.ui.config.get("BROKEN WORDS",key))
        return fixed

    def isDecode(self, filepath):
        with open(filepath, "rb") as F:
            text = F.read()
            F.close()
            enc = chardet.detect(text).get("encoding")
            if enc and enc.lower() != "utf-8":
                self.MSG.append('        ' +enc+ ' --> UTF-8')
                text = text.decode(enc)
                text = text.encode("utf-8")
                with open(filepath, "wb") as f:
                    f.write(text)
                    f.close()
                    return 1
            else:
                return 0

    def isReplaceWord(self, filepath, bad, good):
        with open (filepath, 'r', encoding="utf-8") as f:
            old_data = f.read()
            f.close()

        if old_data.count(bad) > 0:
            self.MSG.append("        '" +bad+ "' >>> '" +good+"'")
            new_data = old_data.replace(bad, good)

            with open (filepath, 'w', encoding="utf-8") as f:
                f.write(new_data)
                f.close()
                return 1
        else:
            return 0

    def openExternalFile(self, filepath):
        fixed = self.fixfile(filepath)
        if fixed >0:
            self.MSG.insert(0, self.ui.config.get("LANGUAGE",'file')+filepath)
            self.MSG.append(self.ui.config.get("LANGUAGE",'done'))
            self.ui.addTextToWindow(self.MSG)
        self.MSG.clear()

    def openExternalFolder(self, folderpath):
        self.copyThread.addFolder(folderpath)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = myIntarface()  # Создаём объект класса ExampleApp
    #window.show()  # Показываем окно
    sys.exit(app.exec_())  # и запускаем приложение
    #time.sleep(5)

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
