# Modül 2 — Prompt Mimarisi

> İyi bir prompt, iyi bir brief gibi yazılır. Reklam ajansına verilen bir brief. İyi ajanslar kötü brief'le çalışmaz. LLM çalışır — ama sonuç kötü olur.

---

## 2.1 — 5 Katmanlı Yapı

Her güçlü prompt şu beş katmanı içerir. Hepsini her zaman yazmanız gerekmiyor. Ama her birinin ne işe yaradığını bilmeniz gerekiyor — çünkü eksik bıraktığınız her katman modelin doldurmasına izin veriyorsunuz. Model doldurur — ama sizin istediğiniz gibi değil.

---

### Katman 1: Rol

**Ne yapar:** Modele kim olduğunu söyler. Perspektif ve uzmanlık düzeyini ayarlar.

**Neden önemli:** Model büyük miktarda metinle eğitildi — tıp metinleri, hukuk metinleri, teknik belgeler, roman, gazete, kod. "Rol" komutu bu eğitim verisi içinde hangi bölümden ağırlıklı örnekleme yapacağını yönlendiriyor.

```
# Zayıf
"Bana hukuki bir metin yaz."

# Güçlü
"Sen deneyimli bir iş hukuku avukatısın. 
Müvekkillere hizmet sözleşmesi risklerini açıklıyorsun."
```

**Uyarı:** Rol ne kadar spesifik, çıktı o kadar tutarlı — ama aşırı spesifik roller bazen modeli kısıtlar. "Kıdemli veri bilimcisi" çoğu zaman "2019-2023 yılları arasında öneri sistemleri üzerine çalışmış, Python ve Spark konusunda uzman bir veri bilimcisi"nden daha iyi çalışır. Test edin.

---

### Katman 2: Bağlam

**Ne yapar:** Modele durumu anlatır. Ne bilmesi gerektiğini belirler.

**Neden önemli:** Model bağlam olmadan "ortalama durum"u varsayar. Ortalama durum nadiren sizin durumunuzdur.

```
# Bağlamsız
"Bu e-postayı düzelt."

# Bağlamlı
"Bu e-postayı düzelt. Bağlam: 
- Gönderen: Orta düzey yönetici
- Alıcı: C-suite
- Amaç: Bütçe artışı talebi
- Ton: Şirkette resmi yazışma kültürü hâkim
- Durum: İlk istek reddedildi, bu ikinci deneme"
```

**Pratik öneri:** Bağlamı "durum, hedef, kısıt" üçlüsüyle düşünün. Durum: şu an ne var. Hedef: ne olmasını istiyorsunuz. Kısıt: ne olmamalı ya da nelere dikkat edilmeli.

---

### Katman 3: Görev

**Ne yapar:** Ne yapılmasını istediğinizi net olarak tanımlar.

**Neden önemli:** "Yaz", "analiz et", "öneride bulun" gibi fiiller çok geniş. Model en olası yorumu seçer. Sizin istediğiniz yorum olmayabilir.

```
# Belirsiz görev
"Bu raporu analiz et."

# Net görev
"Bu rapordaki verileri incele ve şunları yap:
1. Beklenmedik örüntüleri tespit et (varsa)
2. Her bulgu için olası bir neden öner
3. Emin olmadığın yerleri açıkça belirt"
```

**Kural:** Görev cümlesinde eylem fiilleri kullanın. "Analiz et" değil "karşılaştır, sırala, tespit et, öner." Ne kadar spesifik, o kadar iyi.

---

### Katman 4: Kısıt

**Ne yapar:** Sınırları, yasakları ve öncelikleri belirler.

**Neden önemli:** Model varsayılan olarak "yardımcı olmak" ister. Bu bazen gereksiz bilgi eklemek, konu dışına çıkmak ya da çok uzun yazmak anlamına gelir.

```
# Kısıtsız
"Proje planı yaz."

# Kısıtlı
"Proje planı yaz.
- Sadece MVP kapsamını dahil et, sonraki aşamaları değil
- Kaynak tahmini yapma, sadece zaman çizelgesi
- Teknik detaylara girme, bu belge yönetim için
- 500 kelimeyi geçme"
```

**İki tür kısıt:**
- **Ne yapma:** Konu dışı şeyler, belirli bir ton, belirli bilgiler
- **Nasıl yap:** Uzunluk, format, dil seviyesi, referans stili

---

### Katman 5: Format

**Ne yapar:** Çıktının nasıl görüneceğini belirler.

**Neden önemli:** Aynı içerik farklı formatlarda çok farklı kullanışlıdır. Bir toplantı için madde madde liste, bir rapor için paragraf, bir sistem için JSON, bir sunum için başlıklar gerekir.

```
# Formatsız
"Rekabetçi analiz yaz."

# Formatlı
"Rekabetçi analiz yaz. Format:
- Her rakip için ayrı bölüm
- Her bölümde: güçlü yönler, zayıf yönler, tehdit oluşturduğu alanlar
- Son bölüm: karşılaştırmalı tablo (Markdown)
- Başlıklar H2, alt başlıklar H3"
```

---

## 2.2 — Üç Temel Teknik

Bu teknikler araç değil, strateji. Ne zaman hangisini kullanacağınızı bilmek kullanmak kadar önemli.

---

### Chain-of-Thought (Adım Adım Düşünme)

**Ne işe yarar:** Modelin "iç monologunu" dışa vurmasını sağlar. Özellikle çok adımlı akıl yürütme gerektiren görevlerde doğruluğu artırır.

**Ne zaman kullanılır:**
- Matematik/mantık soruları
- Karmaşık karar analizleri
- Bir argümanın zayıf noktalarını bulmak
- Hata ayıklama

**Nasıl eklenir:**

```
# Basit versiyon
"...Adım adım düşün."

# Daha güçlü versiyon
"...Cevabına ulaşmadan önce şu soruları yanıtla:
1. Bu problemin temel varsayımı ne?
2. Hangi bilgi eksik?
3. Alternatif yorumlar var mı?
Sonra sonucunu ver."
```

**Gerçek test:** Stanford NLP grubu (Wei et al., 2022) CoT'un özellikle 100B+ parametre modellerde dramatik performans artışı sağladığını gösterdi. Küçük modellerde etkisi daha sınırlı.

---

### Few-Shot Prompting (Örnekle Yönlendirme)

**Ne işe yarar:** "Bu formatta istiyorum" demek yerine formatı gösterir. Model örüntüden öğrenir.

**Ne zaman kullanılır:**
- Spesifik bir format ya da ton istediğinizde
- Modelin varsayılan tarzı işinize gelmediğinde
- Tutarlılık kritik olduğunda (toplu işlem gibi)

```
# Few-shot örneği
Aşağıdaki müşteri yorumlarını sınıflandır.

Örnekler:
Yorum: "Teslimat geç geldi ama ürün harikaydı." → Sınıf: Karma (lojistik negatif, ürün pozitif)
Yorum: "Müşteri hizmetleri hiç cevap vermedi." → Sınıf: Negatif (hizmet)
Yorum: "Tam beklediğim gibi, hızlı geldi." → Sınıf: Pozitif

Şimdi sınıflandır:
Yorum: "Ürün güzeldi ama ambalaj hasarlıydı."
```

**Kaç örnek gerekir?** Genellikle 2-5 yeterli. 10'dan fazlası nadiren anlamlı fark yaratır ve token harcatır.

---

### Self-Consistency (Çoğunluk Oylaması)

**Ne işe yarar:** Aynı promptu birden fazla çalıştırıp en tutarlı cevabı seçer. Stokastikliği avantaja çevirir.

**Ne zaman kullanılır:**
- Yüksek riskli kararlar
- Faktüel doğrulama
- Karmaşık analiz

**Nasıl uygulanır:**

```python
# Örnek: 3 paralel sorgu, çoğunluk seçimi
responses = []
for i in range(3):
    response = llm.complete(prompt, temperature=0.7)
    responses.append(response)

# Manuel: En sık görülen sonucu seçin
# Otomatik: Modele üç cevabı ver, "hangisi en tutarlı" diye sor
```

**Uyarı:** Her API çağrısı maliyet. Self-consistency gerçekten önemli kararlar için saklayın.

---

## 2.3 — Canlı Demo: 5 Katman Toggle

Aşağıdaki prompt başlangıç noktası. Her katmanı ekleyerek çıktının nasıl değiştiğini gözlemleyin.

**Sıfır bağlam:**
```
"Yazı yaz."
```

**+ Rol:**
```
"Sen deneyimli bir iş geliştirme uzmanısın. Yazı yaz."
```

**+ Bağlam:**
```
"Sen deneyimli bir iş geliştirme uzmanısın. 
Bağlam: Bir SaaS startup'ı B2B müşterilere yönelik 
soğuk e-posta kampanyası başlatıyor.
Yazı yaz."
```

**+ Görev:**
```
"Sen deneyimli bir iş geliştirme uzmanısın. 
Bağlam: Bir SaaS startup'ı B2B müşterilere yönelik 
soğuk e-posta kampanyası başlatıyor.
Görev: İlk iletişim e-postası yaz. 
Hedef: Demo toplantısı almak."
```

**+ Kısıt:**
```
"...
Kısıtlar:
- 150 kelimeyi geçme
- Ürün özelliğinden bahsetme, problemi konuş
- 'merhaba' ile başlama
- Tek bir CTA"
```

**+ Format:**
```
"...
Format:
- Konu satırı (A/B test için 2 seçenek)
- E-posta gövdesi
- Gönderenden önce neden bu formatı seçtiğini 1 cümleyle açıkla"
```

Her adımda çıktıyı karşılaştırın. Fark görülecek.

---

## 2.4 — Sık Yapılan Hatalar

### Hata 1: Çelişkili Kısıtlar

```
# Çelişkili
"Kısa ve öz yaz. Tüm detayları dahil et. 500 kelime."

# Düzeltilmiş
"500 kelimede tüm kritik detayları kapsayan özlü bir özet yaz."
```

### Hata 2: Format Sonradan Söylemek

Model cevabı oluştururken formatı da belirliyor. Format talebi en sona gelirse model zaten bir yapı kurmuştur. Format her zaman önceden söyleyin.

### Hata 3: Negatif Kısıt Fazlalığı

```
# Sorunlu (çok fazla "yapma")
"Yüzeysel olma. Tekrarlama. Çok uzun yazma. 
Jargon kullanma. Subjektif olma."

# Daha iyi
"Uzman bir okuyucuya yönelik, 300 kelimede, 
kanıta dayalı bir analiz yaz."
```

Modele ne istediğinizi söyleyin, ne istemediğinizi değil — ya da istemediğiniz şeyleri minimize edin.

---

## Modül Özeti

```
Prompt = Rol + Bağlam + Görev + Kısıt + Format
```

Her katmanı ekledikçe model için belirsizlik azalır. Belirsizlik azaldıkça çıktı kalitesi artar.

Teknikler:
- **CoT** → Akıl yürütme gerektiren görevler
- **Few-shot** → Format ve ton tutarlılığı
- **Self-consistency** → Yüksek riskli kararlar

---

## Devam

→ [Modül 3: Agent Düşüncesi](../03-agent-thinking/)  
→ [Egzersiz 2](../../exercises/02-architecture-exercises.md)  
→ [Örnek: Kurumsal Prompt Şablonları](../../examples/intermediate/)
