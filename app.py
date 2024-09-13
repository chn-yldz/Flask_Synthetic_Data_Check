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


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or not file.filename.endswith('.csv'):
            flash('Geçerli bir CSV dosyası seçmelisiniz!')
            return redirect(request.url)

        # Eski dosyaları sil
        csv_handler.delete_old_files()

        # Dosyayı kaydet ve verileri işleyelim
        file_path = csv_handler.save_csv(file)
        data = csv_handler.parse_csv(file_path)

        if len(data) < 10:  # Veri seti minimum satır kontrolü
            flash('Modelin eğitilebilmesi için en az 10 satır veri gerekli.')
            return redirect(request.url)

        # Veritabanına kaydet
        save_to_db(data)

        # Modeli yeni verilerle eğit
        analyzer.train_model_with_data(data)

        # Verileri tahmin et
        predictions = analyzer.predict(data)
        analysis_result = analyzer.analyze_data(predictions)

        # Analiz sonuçlarını göster
        return redirect(url_for('show_data',
                                total_data=analysis_result['total_data'],
                                synthetic_data=analysis_result['synthetic_data'],
                                non_synthetic_data=analysis_result['non_synthetic_data'],
                                synthetic_percentage=analysis_result['synthetic_percentage']))

    return render_template('index.html')


@app.route('/data')
def show_data():
    all_data = UploadedData.query.all()

    # Analiz için sadece ilk 3 satırı maskele
    masked_data = mask_data(all_data[:3])  # Sadece analiz için maskeleme yapılacak

    # GET parametrelerinden verileri al
    total_data = request.args.get('total_data', 0, type=int)
    synthetic_data = request.args.get('synthetic_data', 0, type=int)
    non_synthetic_data = request.args.get('non_synthetic_data', 0, type=int)
    synthetic_percentage = request.args.get('synthetic_percentage', 0, type=float)

    return render_template('data.html', data=all_data, masked_data=masked_data,
                           total_data=total_data,
                           synthetic_data=synthetic_data,
                           non_synthetic_data=non_synthetic_data,
                           synthetic_percentage=synthetic_percentage)


def save_to_db(data):
    """Verileri veritabanına kaydet"""
    db.session.query(UploadedData).delete()  # Eski verileri sil
    for row in data:
        new_data = UploadedData(
            first_name=row[0],
            last_name=row[1],
            email=row[2],
            date=row[3],
            guid=str(uuid.uuid4())
        )
        db.session.add(new_data)
    db.session.commit()


def mask_data(data):
    """Sadece analiz kısmı için verileri maskele"""
    masked_data = []
    for row in data:
        masked_row = {
            "first_name": row.first_name[0] + "*" * (len(row.first_name) - 1),  # İsim maskeleme
            "last_name": row.last_name[0] + "*" * (len(row.last_name) - 1),     # Soyisim maskeleme
            "email": mask_email(row.email),                                    # Email maskeleme
            "date": row.date                                                   # Tarih aynı kalır
        }
        masked_data.append(masked_row)
    return masked_data


def mask_email(email):
    """Email adresini maskele, @ işaretinden sonrasını koru"""
    local_part, domain = email.split('@')
    return local_part[0] + "*" * (len(local_part) - 1) + "@" + domain


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
