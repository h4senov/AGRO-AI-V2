AgroVision: The Beginning (Early Prototype)
-----------------------------------------------------------
Bu repozitariya AgroVision layihəsinin ən ilkin, təməl versiyasıdır. Burada kənd təsərrüfatı sahələrinin idarə olunması üçün Flask və Django ilə aparılan ilk struktur sınaqları və "back-to-basics" yanaşmaları yer alır.

⚠️ Qeyd: Bu layihə hal-hazırda aktiv inkişafda olan əsas layihə deyil, mənim proqramlaşdırma və aqrar texnologiyalar sahəsindəki ilk təcrübələrimi əks etdirən bir "learning archive"-dir.

🛠 Nələr sınaqdan keçirilib?
Flask Routing: Sahələrin (Area) siyahılanması və detallarına baxış üçün sadə marşrutlar.

SQLAlchemy & Django ORM: Verilənlər bazası ilə işləməyin fərqli yolları (SQLite üzərində).

Manual Data Handling: POST müraciətləri ilə məlumatların qəbulu və bazaya işlənməsi.

Localization (i18n): İlk çoxdilli interfeys cəhdləri.

📂 Struktur (Sadələşdirilmiş)
app.py: Flask ilə yazılmış ilkin marşrutlar (Areas, Soils).

smart_farm/: Django strukturuna keçid cəhdi.

templates/: HTML-in backend ilə ilk inteqrasiyası.

🚀 Məqsəd
Bu layihənin əsas məqsədi mürəkkəb sistemlərə keçməzdən əvvəl:

Verilənlər bazası münasibətlərini (Area <-> Soil) anlamaq.

CRUD (Create, Read, Update, Delete) funksiyalarını sıfırdan qurmaq.

Backend məntiqini brauzer interfeysi ilə əlaqələndirmək idi.
