import os
from zipfile import ZipFile
from pypdf import PdfReader
from openpyxl import load_workbook, Workbook
import csv
from io import TextIOWrapper

CURRENT_FILE = os.path.abspath(__file__)
CURRENT_DIRECTORY = os.path.dirname(CURRENT_FILE)
TMP_DIR = os.path.join(CURRENT_DIRECTORY, "tmp")
PDF_DIR = os.path.join(TMP_DIR, "test.pdf")
XLSX_DIR = os.path.join(TMP_DIR, "test.xlsx")
CSV_DIR = os.path.join(TMP_DIR, "test.csv")

if not os.path.exists("resources"):
    os.mkdir("resources")

RESOURCES_DIR = os.path.join(CURRENT_DIRECTORY, "resources")


def test_archive():
    with ZipFile(os.path.join(RESOURCES_DIR, "files.zip"), "w") as zf:
        zf.write(PDF_DIR, os.path.basename(PDF_DIR))
        zf.write(XLSX_DIR, os.path.basename(XLSX_DIR))
        zf.write(CSV_DIR, os.path.basename(CSV_DIR))


def test_archive_pdf():
    with ZipFile(os.path.join(RESOURCES_DIR, "files.zip"), "r") as zip_file:
        # print(zip_file.namelist())
        reader = PdfReader(zip_file.open("test.pdf"))
        text = reader.pages[1].extract_text()
        assert "Работа подготовлена на кафедре прикладной математики" in text


def test_archive_xlsx():
    with ZipFile(os.path.join(RESOURCES_DIR, "files.zip"), "r") as zip_file:
        workbook = load_workbook(zip_file.open("test.xlsx"))
        sheet = workbook.active
        text = sheet.cell(row=15, column=3).value
        assert "Значения искомых перемен." in text


def test_archive_csv():
    with ZipFile(os.path.join(RESOURCES_DIR, "files.zip"), "r") as zip_file:
        with zip_file.open("test.csv") as csv_file:
            csvreader = list(csv.reader(TextIOWrapper(csv_file, "Windows-1251")))
            # print(list(csvreader))
            second_row = csvreader[1]
            # print(second_row)

            assert "Произв. оборуд. в нормочасах" in second_row[0]
            # assert second_row[3] == "1"
