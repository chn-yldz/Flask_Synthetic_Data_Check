from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.linear_model import LogisticRegression
from typing import List, Dict

class DataAnalyzer:
    def __init__(self):
        self.model = LogisticRegression()
        self.name_encoder = LabelEncoder()
        self.email_encoder = LabelEncoder()

    def train_model(self) -> None:
        """Modeli sentetik ve gerçek verilerle 4 özellik kullanarak eğit"""
        real_data = np.random.rand(50, 4)  # Gerçek veriler (4 özellik)
        synthetic_data = np.random.rand(50, 4) + 1  # Sentetik veriler (4 özellik)
        X = np.vstack((real_data, synthetic_data))  # 4 özellikten oluşan veri seti
        y = np.hstack((np.zeros(50), np.ones(50)))  # 0 -> Gerçek, 1 -> Sentetik
        self.model.fit(X, y)

    def predict(self, data: List[List[str]]) -> List[int]:
        """Yeni veriler üzerinde tahmin yap"""
        X_new = []
        for row in data:
            try:
                # İsim ve soyisim uzunluklarını birlikte değerlendirelim
                first_name_length = len(row[0])  # İlk sütun isim
                last_name_length = len(row[1])   # İkinci sütun soyisim
                email_length = len(row[2])       # Üçüncü sütun email
                guid_length = len(row[3])        # Dördüncü sütun tarih ya da GUID olabilir

                # Uzunluk değerlerine göre tahmin yapalım (4 özellik)
                numeric_row = [float(first_name_length), float(last_name_length), float(email_length), float(guid_length)]
                X_new.append(numeric_row)
            except ValueError:
                continue  # Hatalı verileri atla

        if not X_new:
            return []

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
