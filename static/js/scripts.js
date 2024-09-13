document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.querySelector('input[type="file"]');
    const form = document.querySelector('form');

    // Dosya yükleme kontrolü
    form.addEventListener('submit', function(event) {
        const file = fileInput.files[0];

        if (!file) {
            alert('Lütfen bir dosya seçin!');
            event.preventDefault(); // Yüklemeyi durdur
        } else if (!file.name.endsWith('.csv')) {
            alert('Sadece CSV dosyası yükleyebilirsiniz!');
            event.preventDefault(); // Yüklemeyi durdur
        } else if (file.size > 2 * 1024 * 1024) { // 2MB sınırı
            alert('Dosya boyutu 2MB\'dan büyük olamaz!');
            event.preventDefault(); // Yüklemeyi durdur
        } else {
            // CSV dosyasının satır sayısını kontrol edelim
            const reader = new FileReader();
            reader.onload = function(e) {
                const text = e.target.result;
                const rows = text.split('\n');
                if (rows.length < 10) {
                    alert('Modelin eğitilebilmesi için en az 10 satır veri gerekli.');
                    event.preventDefault(); // Yüklemeyi durdur
                } else {
                    alert('Dosya yükleniyor ve analiz ediliyor...');
                }
            };
            reader.readAsText(file);
        }
    });
});
