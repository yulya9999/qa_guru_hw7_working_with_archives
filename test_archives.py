import os
import zipfile
from zipfile import ZipFile
from pypdf import PdfReader
from openpyxl import load_workbook
import csv
from io import TextIOWrapper
from conftest import RESOURCES_DIR


def test_read_file_pdf():
    with (zipfile.ZipFile(os.path.join(RESOURCES_DIR, 'files.zip')) as zip_file):
        with zip_file.open('test.pdf') as pdf_file:
            reader = PdfReader(pdf_file)
            text = reader.pages[1].extract_text()
            assert "Работа подготовлена на кафедре прикладной математики" in text


def test_archive_xlsx():
    with ZipFile(os.path.join(RESOURCES_DIR, "files.zip"), "r") as zip_file:
        with zip_file.open("test.xlsx") as xlsx_file:
            workbook = load_workbook(xlsx_file)
            sheet = workbook.active
            text = sheet.cell(row=15, column=3).value
            assert "Значения искомых перемен." in text


def test_archive_csv():
    with ZipFile(os.path.join(RESOURCES_DIR, "files.zip"), "r") as zip_file:
        with zip_file.open("test.csv") as csv_file:
            csvreader = list(csv.reader(TextIOWrapper(csv_file, "Windows-1251"), delimiter=';'))
            second_row = csvreader[1]

            assert "Произв. оборуд. в нормочасах" in second_row[0]
            assert second_row[3] == "1"
