import os
from werkzeug.utils import secure_filename
from typing import List
import csv

class CSVHandler:
    def __init__(self, upload_folder: str):
        self.upload_folder = upload_folder

    def save_csv(self, file) -> str:
        """Yeni dosyayı kaydet ve dosya yolunu döndür"""
        filename = secure_filename(file.filename)
        file_path = os.path.join(self.upload_folder, filename)
        file.save(file_path)
        return file_path

    def delete_old_files(self) -> None:
        """Eski dosyaları sil"""
        for filename in os.listdir(self.upload_folder):
            file_path = os.path.join(self.upload_folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def parse_csv(self, file_path: str) -> List[List[str]]:
        """CSV dosyasını oku ve verileri liste olarak döndür"""
        data = []
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Başlık satırını atla
            for row in csv_reader:
                # İsim ve soyisim ayrımı yapılır
                first_name, last_name = row[0], row[1]  # İlk iki sütun isim ve soyisim
                email = row[2]  # Üçüncü sütun email
                date = row[3]   # Dördüncü sütun tarih
                data.append([first_name, last_name, email, date])
        return data
