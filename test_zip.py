import os
import shutil
import csv

from zipfile import ZipFile
from pypdf import PdfReader
from openpyxl import load_workbook


files_to_zip = [
    'tmp/example.pdf',
    'tmp/import_empl_xlsx.xlsx',
    'tmp/import_ou_csv.csv'
]

def test_create_archive():
    with ZipFile("archive.zip", "w") as myzip:
        for file in files_to_zip:
            myzip.write(file)

def test_add_archive_to_resources():
    zip_path = os.path.abspath("archive.zip")
    resources_directory = os.path.abspath('C:/Users/masha/QAGuru/hw_7/resources')

    if not os.path.exists(resources_directory):
        os.makedirs(resources_directory)

    shutil.copy(zip_path, resources_directory)

    os.remove(zip_path)

def test_check_archive():
    zip_path = os.path.abspath("resources/archive.zip")
    with ZipFile(zip_path, 'r') as zipf:
        file_list = zipf.namelist()
        for file in file_list:
            format = file.split('.')[-1]
            print(f"\nФайл: {file}, Формат: {format}")
            test_check_file(file,format)

def test_check_file(file,format):
    if format == 'pdf':
        reader = PdfReader(file)
        page = reader.pages[0]  # Первая страница
        text = page.extract_text()  # Текст из первой страницы
        print(f"Текст с первой страницы: {text}")
        assert text == "Тестовый PDF файл"
    elif format == 'xlsx':
        workbook = load_workbook(file)
        sheet = workbook.active
        first_cell_value = sheet.cell(row=1, column=1).value  # Значение первой ячейки (A1)
        print(f"Значение ячейки А1: {first_cell_value}")
        assert first_cell_value == 'Внешний идентификатор для импорта'
    elif format == 'csv':
        with open(file, mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            first_row = next(csv_reader)
            first_row_as_string = ','.join(first_row)  # Получение первой строки
            print(f"Значение первой строки: {first_row_as_string}")
            assert first_row_as_string == 'Index,Customer Id,First Name,Last Name,Company,City,Country,Phone 1,Phone 2,Email,Subscription Date,Website'