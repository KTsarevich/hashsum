import csv
import hashlib
import os
from tkinter import filedialog
from tkinter import *
#Функция расчета хеша файла
def file_hash_hex(file_path, hash_func):
    with open(file_path, 'rb') as f:
        return hash_func(f.read(4096)).hexdigest()
#Функция рекурсевного обхода файлов
def recursive_file_listing(base_dir):
    for directory, subdirs, files in os.walk(base_dir):
        for filename in files:
            yield directory, filename, os.path.join(directory, filename)
#Основная вункция
def main():
    menu = input(str("1. Выбор файла \n2. Выход \n->"))
    while (menu != "2"):
        if (menu == "1"):
            # Открываем проводник
            root = Tk()
            root.withdraw()
            path = filedialog.askopenfilename()
            f = open(path)
            #Выбираем файл и считаем хеш
            ff = file_hash_hex(path, hashlib.sha256)
            print('Контрольная сумма выбранного файла: ', ff)
            search = input(str("Начать поиск? (да/нет):"))
            if (search == "да" or search == "1"):
                #Открываем проводник
                root = Tk()
                root.withdraw()
                src_dir = filedialog.askdirectory()
                # Записываем хеши всех файлов в отдльный файл
                with open('checksums_archive.tsv', 'w', encoding="utf-8") as f:
                    writer = csv.writer(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    for directory, filename, path in recursive_file_listing(src_dir):
                        writer.writerow((directory, filename, file_hash_hex(path, hashlib.sha256)))
                        #print(filename, file_hash_hex(path, hashlib.sha256))
                        #Сравниваем хеш файла и сканированные хеши
                        check = (file_hash_hex(path, hashlib.sha256) == ff)
                        if check:
                            print("Путь: ",directory, "Название файла: ",filename)
                    # if check == False:
                    #     print("Файлов не найдено")
            elif (search == "нет" or search == "2"):
                return main()
        elif (menu != 1):
            print("Введено неверное значение!!!")
        return main()

main()