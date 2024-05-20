import zipfile
import os
import shutil
import pytest

CURRENT_FILE = os.path.abspath(__file__)
CURRENT_DIRECTORY = os.path.dirname(CURRENT_FILE)
TMP_DIR = os.path.join(CURRENT_DIRECTORY, "tmp")


@pytest.fixture(scope="module", autouse=True)
def create_archive():
    if not os.path.exists("resources"):
        os.mkdir("resources")

    RESOURCES_DIR = os.path.join(CURRENT_DIRECTORY, "resources")

    with zipfile.ZipFile(os.path.join(RESOURCES_DIR, "files.zip"), "w") as zf:
        for file in ["test.pdf", "test.xlsx", "test.csv"]:
            add_file = os.path.join(TMP_DIR, file)
            zf.write(add_file, os.path.basename(add_file))

    yield
    # zf.close()
    # os.remove(os.path.join(RESOURCES_DIR, "files.zip"))
    shutil.rmtree(RESOURCES_DIR)
