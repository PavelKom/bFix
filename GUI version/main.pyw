import sys
import os
import time
import datetime
import glob
import chardet
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from shutil import move
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import PatternMatchingEventHandler

import design

defaultConfig = """language=en
logging=True
silentmode=True
showsettings=True
workfolder=C:/WNC/user/iso
"""


defaultLanguage = """alias=en
name=English
head=Program launch
emptywordfile=The dictionary of broken words is empty !!!
trackedfolder=Tracked Folder:
hookedfile=Hooked file: 
menu=Menu
openfilebutton=Open file
openfiledescription=Fix file
openfolderbutton=Open folder
openfolderdescription=Fix files in folder
clearbutton=Clear window
cleardescription=Clear text window
exitbutton=Exit
exitdescription=Exit the program
file=File: 
time=Time:
decode=Change encoding: 
corruptedword1=Corrupted word: 
corruptedword2=Fixed on: 
corruptedword3=Number of fixes: 
folder=Folder: 
founded=Files found: 
fixed=Fixed files:
logbutton=Logging
silent=Silent mode
done=Done
yes=Yes
no=No
exitmsg=Are you sure you want to quit?
"""

defaultCFG = dict()
defaultLNG = dict()

languageNameList = dict() #key: alias
languageConnectList = list()

class myIntarface(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.textBrowser.clear()
        self.progressBar.hide()
        self.CFG = dict()
        self.LNG = dict()
        self.WORD = dict()
        self.initConfig()
        self.changeLanguage(self.CFG['language'], True)
        self.postUI()
        self.initConnect()
        self.initWordReplacer()
        
        self.observer = Observer()
        self.myobserver = myObserver(self)
        self.observer.schedule(self.myobserver, path=self.CFG['workfolder'], recursive=True)
        self.observer.start()

    #Initialize programm

    def initConfig(self):
        configs = defaultConfig.split('\n')
        for line in configs:
            key, *value = line.split('=')
            defaultCFG[key] = str(value).replace("'",'').replace('[','').replace(']','')
            self.CFG[key] = str(value).replace("'",'').replace('[','').replace(']','')
            
        if not os.path.exists('config.cfg'):
            with open('config.cfg', 'w+', encoding="utf-8") as defaultCfg:
                defaultCfg.write(defaultConfig)
                defaultCfg.close()
        else:
            with open('config.cfg', 'a+', encoding="utf-8") as readCfg:
                tempCfg = dict()
                readCfg.seek(0)
                readCfgList = readCfg.read().split('\n')
                for line in readCfgList:
                    key, *value = line.split('=')
                    tempCfg[key] = str(value).replace("'",'').replace('[','').replace(']','')
                for key in defaultCFG.keys():
                    if tempCfg.get(key) == None:
                        readCfg.write(key+'='+ defaultCFG[key]+'\n')
                    else:
                        self.CFG[key] = tempCfg[key]
                del tempCfg
                readCfg.close()

    def initLanguage(self):
        words = defaultLanguage.split('\n')
        for line in words:
            key, *value = line.split('=')
            defaultLNG[key] = str(value).replace("'",'').replace('[','').replace(']','')
            self.LNG[key] = str(value).replace("'",'').replace('[','').replace(']','')

        if not os.path.exists('lang'): os.makedirs('lang')
        if not os.path.exists('lang/en.lang'):
            with open('lang/en.lang', 'w+', encoding="utf-8") as defaultLng:
                defaultLng.write(defaultLanguage)
                defaultLng.close()
        else:
            with open('lang/en.lang', 'a+', encoding="utf-8") as readDefLng:
                tempLng = dict()
                readDefLng.seek(0)
                readLngList = readDefLng.read().split('\n')
                for line in readLngList:
                    key, *value = line.split('=')
                    tempLng[key] = str(value).replace("'",'').replace('[','').replace(']','')
                for key in defaultLNG.keys():
                    if tempLng.get(key) == None:
                        readDefLng.write(key+'='+ defaultLNG[key]+'\n')
                    else:
                        self.LNG[key] = tempLng[key]
                del tempLng
                readDefLng.close()

    def initWordReplacer(self):
        if not os.path.exists('word.list'):
            with open('word.list', 'w+', encoding="utf-8") as defaultWord:
                defaultWord.close()
                self.textBrowser.append(self.LNG['emptywordfile'])
        else:
            with open('word.list', 'r', encoding="utf-8") as readWord:
                for line in readWord:
                    line = line.replace("\n",'')
                    key, *value = line.split('=')
                    self.WORD[key] = str(value).replace("'",'').replace('[','').replace(']','')
                    self.textBrowser.append(key+'    '+self.WORD[key])
                readWord.close()
            if not bool(self.WORD):
                self.textBrowser.append(self.LNG['emptywordfile'])
        

    #GUI stuff

    def changeLanguage(self, lang, init = False):
        self.initLanguage()

        if not os.path.exists('lang/'+lang+'.lang'):
            self.changeLanguage('en')

        with open('lang/'+lang+'.lang', 'r', encoding="utf-8") as readLng:
            for line in readLng:
                line = line.replace('\n','')
                key, *value = line.split('=')
                self.LNG[key] = str(value).replace("'",'').replace('[','').replace(']','')

        self.menuFile.setTitle(self.LNG['menu'])
        self.actionOpenFile.setText(self.LNG['openfilebutton'])
        #self.actionOpenFile.setToolTip(self.LNG['openfiledescription'])
        self.actionOpenFolder.setText(self.LNG['openfolderbutton'])
        #self.actionOpenFolder.setToolTip(self.LNG['openfolderdescription'])
        self.actionClearWindow.setText(self.LNG['clearbutton'])
        #self.actionClearWindow.setToolTip(self.LNG['cleardescription'])
        self.actionExit.setText(self.LNG['exitbutton'])
        #self.actionExit.setToolTip(str(self.LNG['exitdescription'])
        self.boxLogging.setText(self.LNG['logbutton'])
        self.boxSilentMode.setText(self.LNG['silent'])

        if init:
            self.textBrowser.append(self.LNG['head']+'\n'+
                                     self.LNG['trackedfolder']+
                                     self.CFG['workfolder']+'\n')
            self.logging(self.LNG['head'])
            self.logging(self.LNG['trackedfolder']+self.CFG['workfolder'])

    def postUI(self):
        if self.CFG['showsettings'] == 'False' or self.CFG['showsettings'] == 'no':
            self.boxLogging.hide()
            self.boxSilentMode.hide()
            self.boxLanguage.hide()

    def initConnect(self):
        self.boxLogging.toggle()
        if self.CFG['logging'] == 'True':
            self.boxLogging.setCheckState(Qt.Checked)
        self.boxLogging.stateChanged.connect(self.updateLogButton)
        
        self.boxSilentMode.toggle()
        if self.CFG['silentmode'] == 'True':
            self.boxSilentMode.setCheckState(Qt.Checked)
        self.boxSilentMode.stateChanged.connect(self.updateSilentButton)

        self.boxLanguage.activated['int'].connect(self.changeLanguageButton)
        self.updateLangList()
        self.boxLanguage.setCurrentText(languageNameList[self.CFG['language']])

        self.actionOpenFile.triggered.connect(self.openFile)
        self.actionOpenFolder.triggered.connect(self.openFolder)
        self.actionExit.triggered.connect(QtWidgets.qApp.quit)

        
    def changeLanguageButton(self, num):
        text = languageConnectList[num]
        self.changeLanguage(text)
        self.updateLangList()

        with open ('config.cfg', 'r') as f:
                old_data = f.read()
                new_data = old_data.replace('language='+self.CFG['language'], 'language='+text)
                with open ('config.cfg', 'w') as f:
                    f.write(new_data)

    def updateLangList(self):
        #self.boxLanguage.clear()
        #languageConnectList.clear()
        langList = glob.glob('lang/*.lang')
        for line in langList:
            locale = line.replace('lang\\','').replace('.lang','')
            if not bool(languageNameList):
                self.addLanguageInMenu(locale)
            else:
                try:
                    num = self.boxLanguage.findText(languageNameList[locale])
                except KeyError:
                    self.addLanguageInMenu(locale)
                    
    def addLanguageInMenu(self, lang):
        with open('lang/'+lang+'.lang', 'r', encoding="utf-8") as defaultCfg:
            tmpAlias = str()
            tmpName = str()
            for tmpline in defaultCfg:
                tmpline = tmpline.replace('\n','')
                key, *value = tmpline.split('=')
                if key == 'alias':
                    tmpAlias = str(value).replace("'",'').replace('[','').replace(']','')
                if key == 'name':
                    tmpName = str(value).replace("'",'').replace('[','').replace(']','')
            if tmpAlias != '' and tmpName != '':
                languageNameList[tmpAlias] = tmpName
                self.boxLanguage.addItem(tmpName)
                languageConnectList.append(tmpAlias)
            else:
                #self.errorLog('[Language] Broken locale file: '+line)
                pass
            defaultCfg.close()
            
    def updateLogButton(self, state):
        if state == Qt.Checked:
            self.CFG['logging'] = 'True'
            with open ('config.cfg', 'r') as f:
                old_data = f.read()
                new_data = old_data.replace('logging=False', 'logging=True')
                with open ('config.cfg', 'w') as f:
                    f.write(new_data)
                    f.close()
        else:
            self.CFG['logging'] = 'False'
            with open ('config.cfg', 'r') as f:
                old_data = f.read()
                new_data = old_data.replace('logging=True', 'logging=False')
                with open ('config.cfg', 'w') as f:
                    f.write(new_data)
                    f.close()

    def updateSilentButton(self, state):
        if state == Qt.Checked:
            self.CFG['silentmode'] = 'True'
            with open ('config.cfg', 'r') as f:
                old_data = f.read()
                new_data = old_data.replace('silentmode=False', 'silentmode=True')
                with open ('config.cfg', 'w') as f:
                    f.write(new_data)
                    f.close()
        else:
            self.CFG['silentmode'] = 'False'
            with open ('config.cfg', 'r') as f:
                old_data = f.read()
                new_data = old_data.replace('silentmode=True', 'silentmode=False')
                with open ('config.cfg', 'w') as f:
                    f.write(new_data)
                    f.close()

    def openFile(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, '', '', 'CNI (*.cni)')[0]
        if len(fname) > 0:
            self.myobserver.openExternalFile(fname)

    def openFolder(self):
        filename = QtWidgets.QFileDialog.getExistingDirectory(self, '')
        if len(filename) > 0:
            self.myobserver.openExternalFolder(filename)

    def logging(self, msg):
        if self.CFG['logging'] == 'False' or self.CFG['logging'] == 'no': return

        if not os.path.exists('program.log'):
            with open('program.log', 'w+', encoding="utf-8") as newLog: newLog.close()

        with open('program.log', 'a+', encoding="utf-8") as log:
            log.write(str(datetime.datetime.now())+' '+msg+'\n')
            log.close()

    def addTextToWindow(self, lst):
        for line in lst:
            self.textBrowser.append(str(line))

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

class myObserver(PatternMatchingEventHandler):
    patterns = ["*.cni", "*.CNI"]
    def __init__(self, interface):
        super().__init__()
        self.ui = interface
        self.MSG = list()
        self.TmpTime = datetime.datetime.now()
        self.TmpTimeOld = self.TmpTime
        self.TmpName = str()
        self.TmpNameOld = str()

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
            self.MSG.insert(0, self.ui.LNG['hookedfile']+event.src_path)
            self.ui.addTextToWindow(self.MSG)
        self.MSG.clear()
        self.TmpTimeOld = self.TmpTime
        self.TmpNameOld = self.TmpName

    def fixfile(self, filepath):
        filepath = filepath.replace('\u005C','/')
        fixed = 0
        fixed += self.isDecode(filepath)
        if len(self.ui.WORD) > 0:
            for key in self.ui.WORD.keys():
                fixed += self.isReplaceWord(filepath, key, self.ui.WORD.get(key))
        return fixed
    
    def isDecode(self, filepath):
        with open(filepath, "rb") as F:
            text = F.read()
            enc = chardet.detect(text).get("encoding")
            if enc and enc.lower() != "utf-8":
                self.MSG.append('        ' +enc+ ' --> UTF-8')
                text = text.decode(enc)
                text = text.encode("utf-8")
                with open(filepath, "wb") as f:
                    f.write(text)
                    return 1
            else:
                return 0

    def isReplaceWord(self, filepath, bad, good):
        with open (filepath, 'r', encoding="utf-8") as f:
            old_data = f.read()

        if old_data.count(bad) > 0:
            self.MSG.append("        '" +bad+ "' >>> '" +good+"'")
            new_data = old_data.replace(bad, good)

            with open (filepath, 'w', encoding="utf-8") as f:
                f.write(new_data)
                return 1
        else:
            return 0

    def openExternalFile(self, filepath):
        fixed = self.fixfile(filepath)
        if fixed >0:
            self.MSG.insert(0, self.ui.LNG['file'].replace('\u005C','/')+filepath)
            self.MSG.append(self.ui.LNG['done'])
            self.ui.addTextToWindow(self.MSG)
        self.MSG.clear()

    def openExternalFolder(self, folderpath):
        fileList = glob.glob(folderpath+'/*.cni')
        fileCount = len(fileList)
        self.ui.activateBar(fileCount)
        counter = 0
        fixedCounter = 0
        self.MSG.append(self.ui.LNG['folder']+folderpath)
        self.MSG.append(self.ui.LNG['founded']+str(fileCount))
        self.MSG.append('\n')
        self.ui.addTextToWindow(self.MSG)
        self.MSG.clear()
        for line in fileList:
            if self.fixfile(line)>0:
                fixedCounter += 1 
                counter += 1
                time.sleep(0.01)
            self.ui.updateBar(counter)
            if self.ui.CFG['silentmode'] == 'False' or self.ui.CFG['silentmode'] == 'off':
                self.MSG.insert(0,self.ui.LNG['file'].replace('\u005C','/')+line)
                self.MSG.append('\n')
                self.ui.addTextToWindow(self.MSG)
            self.MSG.clear()
        self.ui.deactivateBar()
        self.MSG.append(self.ui.LNG['fixed']+str(fixedCounter))
        self.MSG.append(self.ui.LNG['done'])
        self.ui.addTextToWindow(self.MSG)
        self.MSG.clear()
    
        
def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = myIntarface()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    sys.exit(app.exec_())  # и запускаем приложение
    time.sleep(5)

    

    

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
