# Türkiye Kurumsal AI Bağlamı

> Bu belge Türkiye'deki AI benimseme sürecine özgü gözlemler içeriyor.  
> Pek çok kaynakta bulamayacağınız pratik bilgi — sahadan.

---

## Neden Ayrı Bir Bölüm?

Batı merkezli AI eğitimlerinin çoğu Türkiye bağlamını görmezden gelir. Oysa burada çalışmak farklı. Farklı kurumsal kültür, farklı regülasyon ortamı, farklı adaptasyon hızları, farklı dil dinamikleri.

Bu bölüm o farkı adresliyor.

---

## 1 — Dil: Türkçe ile Çalışmak

### Mevcut Durum (2025)

Büyük dil modelleri Türkçede iyi çalışıyor — ama İngilizce kadar değil. Fark neden?

Eğitim verisi dağılımı. İnternetteki İngilizce içerik, Türkçe içeriğin ~50 katı. Model bu oranla eğitildi. Sonuç: Türkçe görevlerde hafif bir performans düşüşü.

**Pratik ölçüm:**

```
Deney: Aynı görevi hem İngilizce hem Türkçe çalıştırın.
Karşılaştırdığınız görevler:
- Karmaşık akıl yürütme (mantık, matematik)
- Nüanslı ton (diplomatik yazı, hassas konu)
- Jargon yoğun içerik (hukuk, tıp, finans)
```

Deneyimlerimizde: Bu kategorilerde İngilizce yaklaşık %10-20 daha tutarlı sonuç veriyor. Basit görevlerde fark önemsiz.

### Strateji: Ne Zaman Hangi Dil?

```
Türkçe prompt → Türkçe çıktı:
✅ Müşteri iletişimi
✅ İç yazışmalar  
✅ Sosyal medya içeriği
✅ Basit analiz

İngilizce prompt → Türkçe çıktı:
✅ Karmaşık akıl yürütme gerektiren analiz
✅ Kod yazma (her zaman İngilizce daha iyi)
✅ Yapısal çıktı (JSON, tablo, şema)
✅ Hassas ton kontrolü gerektiren durum
```

**Template:**
```
[İngilizce sistem prompt + talimatlar]
Please respond in Turkish.
The output must be in natural, professional Turkish.

[Turkish context/content here]
```

### Türkçe'ye Özgü Dikkat Noktaları

**Eklemeli dil sorunu:** Türkçe'nin morfiolojisi modeller için zorlu. "Çalışabilirsiniz" gibi bir kelime birden fazla token. Bu maliyet ve bazen anlam kayması demek.

**Resmiyet seviyeleri:** Türkçe'de "siz/sen" ayrımı önemli. Promptta belirtin:
```
"Resmi 'siz' hitabı kullan." veya
"Samimi 'sen' hitabı kullan."
```

**Argo ve günlük dil:** Modeller genellikle resmi Türkçe üretiyor. Günlük dil için örnekler verin (few-shot).

---

## 2 — Kurumsal Kültür ve AI Benimseme

### Yaygın Direnç Noktaları

**"Bu iş bizi mi işten çıkaracak?"**  
En yaygın endişe. Özellikle veri girişi, raporlama, çeviri yapan rollerde.

Dürüst cevap: Bazı görevler değişecek. Ama bu zaten oluyor — sürekli. Excel de sekreterleri değiştirdi. Photoshop da karanlık odaları. Adaptasyon her zaman mümkün olmuştur.

**"Hata yaparsa kim sorumlu?"**  
Meşru soru. Cevap: İnsan. AI bir araç. Elektrikli testere de kesebilir — sorumluluk kullananın.

**"Verilerimiz nereye gidiyor?"**  
Çok meşru soru, özellikle finans ve sağlık sektöründe. Bkz. aşağıdaki veri güvenliği bölümü.

### Benimseme Hızını Etkileyen Faktörler

```
Hızlı benimseme:
+ Üst yönetim desteği açık
+ Küçük, elle tutulur ilk başarı
+ Teknik şampiyonlar var (her departmanda 1-2 kişi)
+ Eğitim pratik, teorik değil

Yavaş benimseme:
- "Önce IT onaylasın" kültürü
- İlk kötü deneyim (halüsinasyon vb.) yaygınlaştı
- Eğitim olmadan araç verildi
- Başarı metrikleri tanımlanmadı
```

### Türkiye'ye Özgü Fırsatlar

**Muhasebe ve vergi:** Türk vergi mevzuatı karmaşık. AI ile vergi hesaplama değil, mevzuat araştırması ve form doldurma yardımı ciddi zaman kazandırıyor.

**Çok dilli müşteri hizmeti:** Türkiye'de faaliyet gösteren çok uluslu şirketler Türkçe + İngilizce + bazen Arapça destek veriyor. AI bu geçişi kolaylaştırıyor.

**Kamu ihaleleri:** İhale dokümanları uzun ve karmaşık. AI ile anahtar maddeleri çıkarma, benzer ihalelerle karşılaştırma pratik bir kazanım.

**Üretim sektörü:** Türkiye'nin güçlü üretim tabanı + AI: Kalite kontrol, önleyici bakım, tedarik zinciri optimizasyonu henüz erken aşamada ama ivme kazanıyor.

---

## 3 — Regülasyon ve Uyumluluk

### KVKK (Kişisel Verilerin Korunması Kanunu)

AI kullanımında KVKK ile ilgili kritik noktalar:

```
Soru: AI'ya kişisel veri gönderebilir miyim?

Cevap:
- Anonimleştirilmiş veri → Evet, genellikle sorun yok
- İsimli müşteri verisi → Veri işleme sözleşmesi gerekebilir
- Hassas kategori (sağlık, dini bilgi) → Özel dikkat şart
- Çocuk verisi → Ek kısıtlamalar

Pratik kural: Müşteri ismi, TC kimlik no, telefon, adres → 
AI'ya göndermeden önce hukuk departmanına danışın.
```

### Sektöre Özel Kısıtlamalar

**Bankacılık (BDDK):** Bankalar AI sistemlerini BDDK'ya bildirmek durumunda. AI çıktısının kararı doğrudan etkilediği durumlar ek denetim gerektiriyor.

**Sağlık (Sağlık Bakanlığı):** Tıbbi karar destek sistemleri onay sürecine tabi. Hasta verisi işleme katı kurallara bağlı.

**Sigortacılık (SEDDK):** Aktüeryal hesaplamalarda AI kullanımı regulatör denetimine giriyor.

**Genel kural:** Sektörünüzün düzenleyici kurumuna "AI destekli sistemler" hakkında sorumadan production'a almayın. Türkiye'de bu süreçler hızla şekilleniyor.

---

## 4 — Pratik Başlangıç Senaryoları

Türk kurumlarında hızla değer yaratan kullanım alanları — eğitimlerimizden derlendi:

### Muhasebe / Finans Departmanı

```
Yüksek değer, düşük risk:
- E-Defter / e-Fatura açıklamaları için metin üretme
- Yönetim kurulu raporları için özet
- Mevzuat değişikliklerini takip ve özetleme

Dikkat gerektiren:
- Kesin hesaplama (AI sonucu kontrol et)
- Vergi optimizasyonu tavsiyesi (meslek mensubu onayı şart)
```

### Hukuk / Sözleşme

```
Yüksek değer, düşük risk:
- Sözleşme madde özeti ve risk işaretleme
- Standart sözleşme taslağı (avukat revizyonuyla)
- İhale şartname analizi

Dikkat gerektiren:
- Final hukuki karar (avukat imzası şart)
- Mahkeme belgeleri (yetkin hukuki destek)
```

### İnsan Kaynakları

```
Yüksek değer, düşük risk:
- İş ilanı yazma
- CV ön değerlendirme (önyargı kısıtlarıyla)
- Onboarding materyali üretme
- Anket/geri bildirim analizi

Dikkat gerektiren:
- İşe alım kararı (insan onayı şart)
- Performans değerlendirme (HR politikasıyla uyumlu)
```

### Pazarlama / Satış

```
Yüksek değer, düşük risk:
- Kampanya metin üretme
- Sosyal medya içeriği
- Müşteri segmentasyon analizi
- Rakip analizi özetleme

Dikkat gerektiren:
- Marka tonu kontrolü (insan onayı)
- Reklamcılık mevzuatı uyumu (RTÜKvs.)
```

---

## 5 — Başarılı Kurumsal AI Geçişi

Türkiye'deki başarılı örneklerde görülen ortak pattern:

### Faz 1: Küçük Başla (1-2 ay)

```
Seç: En az riskli, en çok tekrarlayan 1 görevi
Ekip: 2-5 kişi, gönüllü erken benimseyenler
Araç: 1 araçla başla (fazla seçenek kafa karışıklığı)
Ölçüm: Basit → "bu görev ne kadar süre aldı önce / şimdi"
```

### Faz 2: Öğren ve Belgele (1-2 ay)

```
Ne işe yaradı → Belgele
Ne işe yaramadı → Neden analiz et
Başarı hikayeleri → Paylaş (ekip motivasyonu)
Prompt kütüphanesi → Oluştur (bu repoyu şablona al)
```

### Faz 3: Yay ve Standardize (Devam)

```
Eğitim: Pratik, sektöre özgü, kısa seanslar
Şampiyonlar: Her departmanda 1-2 kişi yetiştir
Politika: Hangi veri AI'ya gidebilir? Yazılı hale getir
Güncelleme: 3 ayda bir araç ve prompt revizyonu
```

---

## 6 — Yaygın Yanılgılar

**"AI her şeyi yapacak"**  
Hayır. AI belirli görevlerde insandan hızlı ve ucuz. Diğerlerinde insan hâlâ gerekli ve daha iyi.

**"Bir kez kurarız, çalışır"**  
Hayır. AI sistemleri bakım ister. Modeller güncellenir, promptlar zamanla kayar, kullanım senaryoları değişir.

**"Herkese aynı eğitimi verelim"**  
Verimsiz. Muhasebecinin AI ihtiyacı, yazılımcınınkinden farklı. Rol bazlı eğitim daha etkili.

**"Önce mükemmel prompt yazalım, sonra kullanalım"**  
Mükemmel prompt yoktur. Kullanın, geri bildirim alın, geliştirin. Iterasyon şart.

---

*→ [Kaynaklar](../resources/)*  
*→ [Örnek Şablonlar](../examples/templates/)*
