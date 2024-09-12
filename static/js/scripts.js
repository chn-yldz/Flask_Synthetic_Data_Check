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
            // Eğer her şey doğruysa dosya yüklenebilir
            alert('Dosya yükleniyor ve analiz ediliyor...');
        }
    });
});
