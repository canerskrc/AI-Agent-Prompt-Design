# Temel Örnekler

Her örnek üç bölümden oluşuyor:
1. **Kötü versiyon** — çoğu insanın yazdığı
2. **İyi versiyon** — 5 katman uygulanmış
3. **Neden fark yarattı** — teknik açıklama

---

## Örnek 01 — Yönetici Özeti

### ❌ Kötü Versiyon
```
Şu raporu özetle: [rapor metni]
```

**Tipik çıktı sorunu:** Model raporun her bölümünü eşit ağırlıkla özetliyor. 
Yöneticinin görmek istediği şeylere odaklanmıyor.

---

### ✅ İyi Versiyon
```
Rol: Deneyimli bir iş danışmanısın. Yöneticilere raporları 
     nasıl sunacaklarını öğretiyorsun.

Bağlam: Aşağıdaki Q3 operasyonel raporu, CFO'ya sunulmak üzere 
        özetlenecek. CFO zamanı kıt, rakamları ve riskleri önemsiyor, 
        süreci değil.

Görev: Bu raporu CFO için özetle.

Kısıt:
- 200 kelimeyi geçme
- Süreç detaylarına girme
- Her bulguya finansal etki rakamı ekle (varsa)
- Belirsiz bulguları "doğrulanmamış" olarak işaretle

Format:
- 3 cümle genel durum
- Madde madde: 3 kritik bulgu (rakamlarla)
- 1 cümle önerilen aksiyon

[Rapor metni buraya]
```

**Neden fark yarattı:**
- Rol: Model hangi bakış açısından bakacağını biliyor (iş danışmanı)
- Bağlam: Okuyucunun profili verilmiş (CFO, zaman kıtlığı, ilgi alanları)
- Kısıt: Finansal etki zorunluluğu + belirsiz bilgi işaretleme
- Format: Yapı önceden tanımlı

---

## Örnek 02 — E-posta Taslağı

### ❌ Kötü Versiyon
```
Toplantı davet e-postası yaz.
```

**Tipik çıktı sorunu:** Jenerik, resmi olmayan, bağlam yok.

---

### ✅ İyi Versiyon
```
Rol: Kurumsal iletişim konusunda deneyimli bir yazarsın.

Bağlam:
- Gönderen: Orta düzey proje yöneticisi (Ahmet Bey)
- Alıcılar: 3 bölüm müdürü + IT direktörü
- Amaç: ERP geçişi kick-off toplantısı
- Şirket kültürü: Yarı resmi, "bey/hanım" kullanılıyor
- Konu hassasiyeti: Bazı yöneticiler projeye şüpheyle bakıyor

Görev: Toplantı davet e-postası yaz. 
       Şüpheci katılımcıları projenin neden önemli olduğuna ikna etmeli,
       ama baskıcı hissettirmemeli.

Kısıt:
- 150 kelimeyi geçme
- Teknik detaylara girme
- Katılımı zorunluluk olarak değil, önem olarak çerçevele

Format:
- Konu satırı (merak uyandıran, clickbait değil)
- Selamlama
- Neden önemli (2 cümle)
- Toplantı bilgileri
- Kapanış
```

**Neden fark yarattı:**
- "Şüpheci katılımcılar" bağlamı modele stratejik bir görev veriyor
- "İkna et ama baskı yapma" çelişkisini model artık yönetecek
- Şirket kültürü (yarı resmi, hitap şekli) ton kalibrasyon sağlıyor

---

## Örnek 03 — Veri Analizi

### ❌ Kötü Versiyon
```
Bu veriyi analiz et: [CSV data]
```

**Tipik çıktı sorunu:** Model hangi soruyu cevaplamak istediğinizi bilmiyor. 
Genel gözlemler yapıyor, içgörü üretmiyor.

---

### ✅ İyi Versiyon
```
Rol: Deneyimli bir veri analisti olarak davran.

Bağlam: Bu, bir e-ticaret şirketinin Kasım 2024 satış verisi.
        Geçen yılın aynı dönemine kıyasla gelir düşmüş, 
        ancak sipariş sayısı artmış. Yönetim nedenini anlamak istiyor.

Görev: Aşağıdaki veriyi analiz et ve şu soruyu yanıtla:
       "Sipariş sayısı artmasına rağmen gelir neden düştü?"

Cevabında şunları bul:
1. Ortalama sepet değeri değişimi
2. Kategori bazında gelir kaymasını
3. İndirim kullanım oranı değişimini
4. Eğer veri yeterliyse: müşteri segmenti katkısını

Kısıt:
- Veriyi yorum yapmadan listeleme, içgörü üret
- Veriyle desteklenemeyen hipotezleri "hipotez" olarak etiketle
- Eksik veriyi belirt

Format:
- Tek cümle: Ana neden (en yüksek güven düzeyiyle)
- Madde madde: Destekleyici bulgular (rakamlarla)
- Tablo: Kategori bazında yıllık karşılaştırma
- Öneri: 2-3 aksiyon (öncelikli)

[CSV data]
```

**Neden fark yarattı:**
- Spesifik soru: "Neden düştü?" → model odaklanıyor
- İstenen analizler önceden tanımlanmış → model neye bakacağını biliyor
- "Hipotez" etiketi → model emin olmadığını söyleyebilecek

---

## Örnek 04 — Kod Review

### ❌ Kötü Versiyon
```
Bu kodu gözden geçir: [kod]
```

---

### ✅ İyi Versiyon
```
Rol: Kıdemli Python geliştiricisi, code review konusunda uzmansın.
     Yapıcı ama doğrudan geribildirim veriyorsun.

Bağlam:
- Junior geliştirici tarafından yazılmış
- Production ortamına gidecek
- Servis: Günde ~50k istek alan REST API endpoint'i
- Ekip standardı: PEP8, tip ipuçları zorunlu, docstring tercihli

Görev: Aşağıdaki kodu review et.

Değerlendir:
1. Güvenlik açıkları (varsa — önce bunları)
2. Performans sorunları (bu yük altında)
3. Okunabilirlik ve maintainability
4. Test edilebilirlik
5. Ekip standartlarına uyum

Kısıt:
- Küçük stil sorunlarını listeleme (linter halleder)
- Her eleştiriyle birlikte somut düzeltme öner
- Junior dostu ton: öğretici, aşağılayıcı değil

Format:
- 🔴 Kritik (production'a gitmemeli): ...
- 🟡 Önemli (ilk PR'da çözülmeli): ...
- 🟢 Öneri (yapılırsa iyi olur): ...
- Düzeltilmiş versiyon (kritik sorunlar için)

[Kod buraya]
```

---

## Örnek 05 — Sınıflandırma Görevi (Few-Shot)

Bu örnek few-shot tekniğini gösteriyor. Tek prompt, büyük ölçeklenebilirlik.

```
Müşteri destek ekibindeki şikayetleri kategorilere ayır.

Kategoriler:
- ÜRÜN: Ürün kalitesi, hasar, beklentiden farklı
- TESLİMAT: Gecikme, yanlış adres, kayıp kargo
- FATURA: Hatalı ücret, iade, fatura sorunları
- TEKNİK: Uygulama/web sitesi sorunları
- DİĞER: Yukarıdakilere girmeyen

Örnekler:
Şikayet: "Sipariş ettiğim ürün 10 gün sonra geldi, çoktan lazım oldu"
Kategori: TESLİMAT
Aciliyet: YÜKSEK

Şikayet: "Aldığım kazak yıkandıktan sonra küçüldü"
Kategori: ÜRÜN
Aciliyet: ORTA

Şikayet: "Kartımdan iki kez para çekmiş sistem"
Kategori: FATURA
Aciliyet: KRİTİK

Şimdi şu şikayetleri sınıflandır (aynı format):

1. "Uygulamaya giriş yapamıyorum, şifremi değiştirmeye çalıştım olmadı"
2. "İndirimli fiyattan aldım ama faturada normal fiyat yazıyor"
3. "Ürün güzeldi ama kutu açıkken geldi"
```

**Neden few-shot burada kritik:**
- "Aciliyet" kategorisi hiçbir yerde tanımlanmadı — model örneklerden öğrendi
- Format tutarlılığı sağlandı — sonuç bir pipeline'a beslenebilir
- Sınır durumlar (açık kutu = ürün mü, teslimat mı?) için model örüntüden karar verecek

---

## Örnek 06 — Chain-of-Thought: Yatırım Kararı

```
Rol: Sektör bağımsız bir iş stratejisti olarak düşün.

Görev: Aşağıdaki iki seçenek arasında karar ver. 
       Düşünce sürecini adım adım göster, sonra karar ver.

Seçenek A: Yeni ürün geliştirme — 18 ay, ₺2M yatırım, pazar belirsiz
Seçenek B: Mevcut ürünü Orta Asya'ya taşıma — 8 ay, ₺800K, pazar kısmen biliniyor

Önce şu soruları sırayla yanıtla:
1. Her seçeneğin temel risk faktörleri nedir?
2. Hangi varsayımlar doğru olursa A daha iyi? B daha iyi?
3. Geri dönüşü olmayan kararlar hangilerinde var?
4. 12 ay içinde başarısız olursa ne olur? (her iki senaryo için)

Sonra: Hangi seçenek daha az kötü? Neden?
(Not: "Daha iyi" değil, "daha az kötü" diyorum — belirsizlik yüksek)
```

**Teknik not:** "Daha az kötü" çerçevelemesi model cevabını kalibre ediyor. 
Aşırı güvenli cevaplar yerine belirsizliği koruyan bir analiz alıyorsunuz.

---

→ [Orta Düzey Örnekler](../intermediate/)
→ [İleri Düzey: Agent Örnekleri](../advanced/)
