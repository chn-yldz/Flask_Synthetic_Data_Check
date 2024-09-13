from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.linear_model import LogisticRegression
from typing import List, Dict
import random

class DataAnalyzer:
    def __init__(self):
        self.model = LogisticRegression()

    def train_model_with_data(self, data: List[List[str]]) -> None:
        """Modeli kullanıcının yüklediği verilerle eğit"""
        X = []
        y = []  # 0 -> Gerçek veri, 1 -> Sentetik veri

        # Gerçek verileri ekleyelim
        for row in data:
            first_name_length = len(row[0])  # İsim uzunluğu
            last_name_length = len(row[1])  # Soyisim uzunluğu
            email_length = len(row[2])  # Email uzunluğu
            date_length = len(row[3])  # Tarih uzunluğu (örn: 'YYYY-MM-DD' -> 10 karakter)
            X.append([first_name_length, last_name_length, email_length, date_length])
            y.append(0)  # Gerçek veriyi temsil ediyor (burada 0)

        # Sentetik veriler oluşturma
        for _ in range(50):  # 50 adet sentetik veri oluştur
            first_name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(5, 10)))
            last_name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(5, 10)))
            email = ''.join(
                random.choices('abcdefghijklmnopqrstuvwxyz1234567890', k=random.randint(10, 20))) + "@random.com"
            date = f"{random.choice([2020, 2021, 2022, 2023])}-{str(random.choice(range(1, 13))).zfill(2)}-{str(random.choice(range(1, 29))).zfill(2)}"

            first_name_length = len(first_name)
            last_name_length = len(last_name)
            email_length = len(email)
            date_length = len(date)

            X.append([first_name_length, last_name_length, email_length, date_length])
            y.append(1)  # Sentetik veriyi temsil ediyor (burada 1)

        # Verileri numpy array'e dönüştür
        X = np.array(X)
        y = np.array(y)

        # Modeli eğit
        self.model.fit(X, y)

    def predict(self, data: List[List[str]]) -> List[int]:
        """Yeni veriler üzerinde tahmin yap"""
        X_new = []
        for row in data:
            first_name_length = len(row[0])  # İsim uzunluğu
            last_name_length = len(row[1])  # Soyisim uzunluğu
            email_length = len(row[2])  # Email uzunluğu
            date_length = len(row[3])  # Tarih uzunluğu
            X_new.append([first_name_length, last_name_length, email_length, date_length])

        X_new = np.array(X_new)
        predictions = self.model.predict(X_new)
        return predictions.tolist()

    def analyze_data(self, predictions: List[int]) -> Dict[str, float]:
        """Sentetik ve sentetik olmayan verileri analiz et"""
        total = len(predictions)
        synthetic_count = sum(predictions)
        non_synthetic_count = total - synthetic_count
        synthetic_percentage = (synthetic_count / total) * 100 if total > 0 else 0

        return {
            "total_data": total,
            "synthetic_data": synthetic_count,
            "non_synthetic_data": non_synthetic_count,
            "synthetic_percentage": synthetic_percentage
        }
