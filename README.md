# Birliktelik Analizi ile Hizmet Önerisi

Bu proje, müşterilerin aldıkları hizmetlerden ve bu hizmetlerin kategorilerinden oluşan bir veri seti üzerinde birliktelik analizi gerçekleştirerek hizmet önerisi yapmayı amaçlamaktadır.

# Veri Seti
Proje, müşterilerin hizmetleri ve bu hizmetlerin tarih/saat bilgilerini içeren bir veri setini kullanmaktadır.

# Analiz Adımları
# Veriyi Hazırlama:

Veri seti okunur ve gerekli değişiklikler yapılır.
ServiceID ve CategoryID birleştirilerek hizmetleri temsil eden yeni bir değişken oluşturulur.
Sepet tanımı için müşteri ID'si ve yıl/ay bilgisi kullanılarak bir ID oluşturulur.
Birliktelik Kuralları Üretme:

Sepet hizmet pivot tablosu oluşturulur.
NaN değerleri 0 ile doldurulur ve sepet hizmet matrisi oluşturulur.
Apriori algoritması kullanılarak sık görünen öğeler ve kurallar üretilir.
Üretilen kurallar sıralanarak incelenir.

# Hizmet Önerisi:

Kullanıcının en son aldığı hizmet belirlenir.
Üretilen kurallardan kullanıcının son aldığı hizmete dayanarak öneri yapılır.

# Sonuçlar

Bu projede birliktelik analizi kullanılarak müşterilere hizmet önerileri yapılması amaçlanmıştır. Kullanıcıların geçmiş alımlarına dayanarak sıkça bir arada görünen hizmetler ve bunların kuralları tespit edilerek, hizmet önerileri sağlanmıştır.

Bu projenin detaylı açıklamaları ve kodun tamamı "ARMUT_ARL_PROJE.py" dosyasında bulunmaktadır. Detaylı bilgi için kodu incelemek önemlidir.
