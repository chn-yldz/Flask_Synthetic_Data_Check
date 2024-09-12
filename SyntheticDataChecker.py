from DataAnalyzer import DataAnalyzer  # DataAnalyzer sınıfını içe aktarıyoruz
from typing import List

class SyntheticDataChecker:
    def __init__(self, analyzer: DataAnalyzer):
        self.analyzer = analyzer

    def check_synthetic_data(self, data: List[List[str]]) -> float:
        """Verilerin sentetik olup olmadığını analiz eder ve yüzdesini döndürür"""
        predictions = self.analyzer.predict(data)
        analysis_result = self.analyzer.analyze_data(predictions)
        return analysis_result['synthetic_percentage']
