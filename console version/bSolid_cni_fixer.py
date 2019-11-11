"""
Name:                   bSolid_cni_fixer.py
Author:                 PavelKom
Version:                1.0
Description:            EN: A script to fix the encoding of cni files created through bSolid. Also corrects words written in Cyrillic
                        RU: Скрипт для исправления кодировки cni-файлов, созданных через bSolid. Так-же исправляет слова, написанные кириллицей

Installation:           EN: Install python-3 from the official site:        https://www.python.org
                            Installation tips:                              https://python-scripts.com/install-python-windows
                            Install chardet and watchdog (through wincmd):
                                                                            pip install chardet
                                                                            pip install watchdog
                                                                            
                        RU: Установить python-3 с официального сайта:       https://www.python.org
                            Советы по установке:                            https://python-scripts.com/install-python-windows
                            Установить chardet and watchdog (через wincmd):
                                                                            pip install chardet
                                                                            pip install watchdog
                                                                    
What the script does:   EN: The script monitors the CNI files in the folder that bSolid compiles when it is sent to the machine.
                            When they are created/renamed/modified, a check for file encoding and search for broken words is launched.
                            The required files are being corrected.
                            Note: The INTERMAC VERTMAX version 12.0 working program reads the Cyrillic alphabet only in UTF-8 encoding,
                                  while bSolid compiles cni files now in MacCyrillic, then in Windows-1251

                        RU: Скрипт следит за файлами CNI в папке, которые bSolid компилирует при отправке на станок.
                            При их создании/переименовывании/изменении запускается проверка на кодировку файлов и поиск сломанных слов.
                            Производится исправление искомых файлов.
                            Примечание: Рабочая программа INTERMAC VERTMAX версии 12.0 читает кириллицу только в UTF-8 кодировке,
                                        при этом bSolid компилирует cni-файлы то в MacCyrillic, то в Windows-1251

"""
import chardet
import glob
import os
import time
import sys

from tempfile import mkstemp
from shutil import move
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import PatternMatchingEventHandler

#Function for adding a script to autostart Windows
#Функция для добавления скрипта в автозапус Windows
import getpass
USER_NAME = getpass.getuser()
def add_to_startup(file_path=""):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + "bSolid_cni_fixer.bat", "w+") as bat_file:
        bat_file.write(r'start "" %s' % sys.argv[0])

os.system("title "+os.path.basename(sys.argv[0]))

#File tracking folder
#Папка для отслеживания файлов
mainPath = 'C:/WNC/user/iso'
outMSG = list()

#Class for observer work (filter by file type is immediately ready)
#Класс для работы наблюдателя (сразу готов фильтр по типу файлов)
class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.cni", "*.CNI"]

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        FixThis(event.src_path)

    def on_modified(self, event):
        self.process(event)

    def on_moved(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


#File Transcoding Function in UTF-8
#Функция перекодирования файла в UTF-8
def IsDecode(file_path):
    with open(file_path, "rb") as F:
        text = F.read()
        enc = chardet.detect(text).get("encoding")
        if enc and enc.lower() != "utf-8":
            text = text.decode(enc)
            text = text.encode("utf-8")
            with open(file_path, "wb") as f:
                f.write(text)
                #print("\tIs non-UTF-8 file\tDecodong...")
                return False
        else:
            #print("File already is UTF-8")
            return True

#The function of replacing broken words in a file
#Функция замены сломанных слов в файле
def IsReplace(file_path, pattern, subst):
    with open (file_path, 'r', encoding="utf-8") as f:
        old_data = f.read()

    if old_data.count(pattern) > 0:
        outMSG.append('\t' +pattern+ ' >>> ' +subst)
        new_data = old_data.replace(pattern, subst)

        with open (file_path, 'w', encoding="utf-8") as f:
            f.write(new_data)

#File Encoding Check Function
#Функция проверки кодировки файла
def CheckCode(file_path):
    detector = chardet.UniversalDetector()
    with open(file_path, 'rb') as fh:
        for line in fh:
            detector.feed(line)
            if detector.done:
                break
    detector.close()
    output = detector.result.get('encoding')
    return output

#File conversion function with checking the current encoding
#Функция перекодировки файла с проверкой текущей кодировки
def DecodeWithTest(file_path):
    while True:
        if CheckCode(file_path) == 'utf-8':
            break
        outMSG.append('\t' +CheckCode(file_path)+ ' --> UTF-8')
        IsDecode(file_path)

#Dictionary for replacing broken words
#Словарь для замены сломанных слов
replaceList = dict()
#Ключ|Key (ANSI или UTF-8)      Значение|Value (UTF-8)
replaceList['СњР±РіРѕРЅРєР°']   = 'Обгонка'
replaceList['ќбгонка']          = 'Обгонка'

#Main program
#Основная программа
def FixThis(file_path):
    file_path = file_path.replace('\u005C','/')
    outMSG.append(file_path.replace(mainPath+'/',''))
    DecodeWithTest(file_path)
    for key in replaceList.keys():
        IsReplace(file_path, key, replaceList.get(key))
    DecodeWithTest(file_path)
    if len(outMSG) > 1:
        for line in outMSG:
            print(line)
        print('\n')
    outMSG.clear()
    #print('DONE')

#Create a checked folder if it does not exist
#Создание проверяемой папки если её нет
if not os.path.exists(mainPath): os.makedirs(mainPath)

#Launch observer
#Запуск наблюдателя
observer = Observer()
observer.schedule(MyHandler(), path=mainPath, recursive=True)
observer.start()

#Welcome message
#Приветственное сообщение
#RU
print(os.path.basename(sys.argv[0])+'  Запущен')
print('Отслеживаемая папка: '+ mainPath+'\n\n')
#EN
#print(os.path.basename(sys.argv[0])+'  Launched')
#print('Tracked folder: '+ mainPath+'\n\n')

#Adding to Windows startup          |   Comment out the next line if you do not want to add the script to autostart !!!
#Добавление в автозапуск Windows    |   Закомментируйте следующую строку, если не хотите добавлять скрипт в автозапуск!!!
add_to_startup()

#Starting an infinite loop so that the script does not close
#Запуск бесконечного цикла для того, чтобы скрипт не закрывался
while True:
    time.sleep(5)

