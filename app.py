from flask import Flask, render_template, request, redirect, url_for, flash
import os
from models import db, UploadedData
from CSVHandler import CSVHandler
from DataAnalyzer import DataAnalyzer
from SyntheticDataChecker import SyntheticDataChecker
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'

db.init_app(app)

# CSV ve analiz modülleri
csv_handler = CSVHandler(app.config['UPLOAD_FOLDER'])
analyzer = DataAnalyzer()
checker = SyntheticDataChecker(analyzer)

# Modeli eğitmek
analyzer.train_model()

def save_to_db(data):
    """Veriyi veritabanına kaydet"""
    db.session.query(UploadedData).delete()  # Eski verileri sil
    for row in data:
        new_data = UploadedData(
            first_name=row[0],  # İlk sütun: İsim
            last_name=row[1],   # İkinci sütun: Soyisim
            email=row[2],
            date=row[3],
            guid=str(uuid.uuid4())
        )
        db.session.add(new_data)
    db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Dosya bulunamadı!', 'error')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('Lütfen bir dosya seçin!', 'error')
            return redirect(request.url)

        if file and file.filename.endswith('.csv'):
            # Eski dosyaları sil
            csv_handler.delete_old_files()

            # Yeni dosyayı kaydet
            file_path = csv_handler.save_csv(file)

            # CSV dosyasını işle
            data = csv_handler.parse_csv(file_path)

            # Verileri veritabanına kaydet
            save_to_db(data)

            # Sentetik verileri analiz et
            predictions = analyzer.predict(data)
            analysis_result = analyzer.analyze_data(predictions)

            # GET parametreleri ile yönlendirme
            return redirect(url_for('show_data',
                                    total_data=analysis_result['total_data'],
                                    synthetic_data=analysis_result['synthetic_data'],
                                    non_synthetic_data=analysis_result['non_synthetic_data'],
                                    synthetic_percentage=analysis_result['synthetic_percentage']))

    return render_template('index.html')

@app.route('/data')
def show_data():
    all_data = UploadedData.query.all()

    # GET parametrelerinden verileri al
    total_data = request.args.get('total_data', 0, type=int)
    synthetic_data = request.args.get('synthetic_data', 0, type=int)
    non_synthetic_data = request.args.get('non_synthetic_data', 0, type=int)
    synthetic_percentage = request.args.get('synthetic_percentage', 0, type=float)

    return render_template('data.html', data=all_data,
                           total_data=total_data,
                           synthetic_data=synthetic_data,
                           non_synthetic_data=non_synthetic_data,
                           synthetic_percentage=synthetic_percentage)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tabloları oluştur
    app.run(debug=True)
