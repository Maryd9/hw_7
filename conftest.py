import os
import shutil
import pytest

from pathlib import Path
from zipfile import ZipFile

files_to_zip = [
    'tmp/example.pdf',
    'tmp/import_empl_xlsx.xlsx',
    'tmp/import_ou_csv.csv'
]


@pytest.fixture
def test_create_archive():
    # Запись файлов в архив
    with ZipFile("archive.zip", "w") as myzip:
        for file in files_to_zip:
            myzip.write(file)

    folder_path = Path('hw_7/resources')
    # Перемещение архива в ресурсы
    if not folder_path.exists():
        # Если не существует папки, создаем её
        os.makedirs('resources', exist_ok=True)
    shutil.move('archive.zip', 'resources')
    yield
    shutil.rmtree('resources')
