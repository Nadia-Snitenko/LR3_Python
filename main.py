import argparse  # модуль для обработки аргументов командной строки
import json  # встроенный модуль json для кодирования и декодирования данных JSON
import re  # модуль для регулярных выражений
from tqdm import tqdm  # tqdm- способ создания индикаторов прогресса в python
from Pack.validator import file_validate
from Pack.bucket_sort import *
import os


parser = argparse.ArgumentParser("Использование парсера для получения аргументов командной строки")
# argparse.ArgumentParser()- конструктор класса
parser.add_argument("-input", type=str, default="data.txt", help="Путь к файлу данных", dest="file_input")
# Метод add_argument() объекта ArgumentParser определяет, как следует анализировать один аргумент командной строки.
parser.add_argument("-output", type=str, default="result.txt", help="Результат валидации данных", dest="file_output")
parser.add_argument("-sorted", type=str, default="sorted.txt", help="Результат сортировки данных", dest="file_sorted")
parser.add_argument('-s', '--sort', help="Производит сортировку данных", dest="sort")
parser.add_argument('-v', '--valid', help="Производит валидацию файла", dest="valid")
parser.add_argument('-o', '--option', type=str, default='weight', help="Выбор параметра для сортировки", dest="option")

args = parser.parse_args()
input_path = os.path.realpath(args.file_input)
output_path = os.path.realpath(args.file_output)
sorted_path = os.path.realpath(args.file_sorted)
option = args.option
if args.valid is not None:
    file_validate(input_path, output_path)
elif args.sort is not None:
    data = read_file(output_path)
    data = bucket_sort(data, option)
    save_file(sorted_path, data)


