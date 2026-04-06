# Prompt Tasarım Pattern Kataloğu

> Pattern: Tekrar eden bir probleme tekrar eden bir çözüm.  
> Anti-pattern: Tekrar eden bir probleme tekrar eden ama yanlış çözüm.

Bu katalog her ikisini de belgeliyor. Çünkü anti-pattern'ları tanımak, pattern'ları uygulamak kadar değerli.

---

## Bölüm 1 — Temel Yapısal Pattern'lar

---

### Pattern 1: Persona Lock

**Problem:** Model varsayılan "genel asistan" modunda cevap veriyor. Çıktı jenerik.

**Çözüm:** Modeli spesifik bir uzmanlık ve bakış açısıyla kilitle. Sadece "sen bir X'sin" değil — X'in hangi türü, hangi tecrübesi, hangi bakış açısı.

```
# Zayıf persona
"Sen bir pazarlama uzmanısın."

# Güçlü persona
"Sen B2B SaaS şirketlerinde 12 yıl çalışmış, 
özellikle enterprise satış döngüleri ve 
müşteri başarısı konusunda uzmanlaşmış bir 
pazarlama direktörüsün. 
Verilerle konuşursun, sezgiyle değil."
```

**Ne zaman kullanılır:** Tutarlı ton ve uzmanlık perspektifi gerektiğinde. Özellikle toplu içerik üretiminde.

**Dikkat:** Persona ne kadar spesifik olursa, modelin "persona dışı" sorularda cevap vermesi o kadar zorlaşır. Gerektiğinde persona'yı genişletin.

---

### Pattern 2: Perspective Rotation

**Problem:** Model tek bir bakış açısından cevap veriyor. Analiz yüzeysel.

**Çözüm:** Aynı soruyu birden fazla perspektiften cevaplamasını isteyin — aynı promptta.

```
Şu kararı üç farklı perspektiften değerlendir:

Karar: [karar metni]

1. Kısa vadeli finansal perspektif (CFO gözüyle)
2. Uzun vadeli stratejik perspektif (CEO gözüyle)  
3. Operasyonel uygulama perspektifi (COO gözüyle)

Her perspektif için: Ana argüman + En büyük risk

Son bölüm: Üç perspektif arasındaki en kritik gerilim nerede?
```

**Ne zaman kullanılır:** Karar analizi, strateji değerlendirme, tartışmalı konular.

**Varyant:** "Savunucu ve Eleştirmen" — model önce en güçlü argümanı, sonra en güçlü karşı argümanı üretir.

---

### Pattern 3: Constraint Inversion

**Problem:** "Şunu yap" söylüyorsunuz ama model istediğiniz şeyi üretmiyor. Kısıtları pozitif olarak ifade ediyorsunuz ama işe yaramıyor.

**Çözüm:** Ne istediğinizi değil, ne istemediğinizi ve neden istemediğinizi açıklayın. Sonra istediğinizi söyleyin.

```
# Pozitif kısıt (zayıf)
"Özlü ve net yaz."

# İnversiyon pattern (güçlü)
"Kaçın:
- Madde madde liste (bu okuyucu için akışı kesiyor)
- Pasif cümle yapısı ('yapılmaktadır', 'görülmektedir')
- Jargon (okuyucu teknik değil)
- 300 kelimeyi geçmek

Bunların yerine: Aktif fiil, kısa cümle, somut örnek.
[görev]"
```

**Ne zaman kullanılır:** Modelin varsayılan eğilimi istediğinizin tam tersi olduğunda.

---

### Pattern 4: Scaffold and Fill

**Problem:** Uzun, karmaşık bir çıktı istiyorsunuz. Model ya çok kısa ya da yapısız üretiyor.

**Çözüm:** İskeleti siz çizin, modeli doldurmak için yönlendirin.

```
Aşağıdaki yapıyı doldur. [köşeli parantez] içindeki her bölümü yaz.
Yapıyı değiştirme.

---
# [Başlık: Ürünün adı + hedef kitle + ana fayda]

## Problem
[2-3 cümle: Müşterinin yaşadığı acı noktası. Somut, ölçülebilir.]

## Çözümümüz
[3-4 cümle: Ürünün ne yaptığı. Teknik değil, fayda dili.]

## Neden biz?
[Madde madde, 3 madde: Her madde rakipten fark yaratan bir şey.]

## Sosyal Kanıt
[1 müşteri alıntısı: Gerçekmiş gibi hissettiren, spesifik sonuç içeren]

## CTA
[1 cümle eylem çağrısı + 1 aciliyet unsuru]
---

Bağlam: [ürün bilgisi]
```

**Ne zaman kullanılır:** Pazarlama metni, teknik belgeler, standart rapor formatları. Çıktının formatı sabitse bu pattern süre kazandırır.

---

### Pattern 5: Progressive Disclosure

**Problem:** Tek seferde çok fazla şey istiyorsunuz. Çıktı ya sığ ya da dağınık.

**Çözüm:** Görevi adımlara bölün. Her adımın çıktısını bir sonraki adıma girdi olarak verin.

```
Adım 1: [Analiz et] → çıktıyı al
Adım 2: [Adım 1 çıktısını kullanarak önceliklendir] → çıktıyı al  
Adım 3: [Adım 2 çıktısını kullanarak uygulama planı yaz] → final
```

**Pratik uygulama:** "Önce sadece şunu yap" diyerek başlayın. Çıktıyı alın. Devam edin.

**Ne zaman kullanılır:** Karmaşık analiz, çok adımlı içerik üretimi, bağımlı kararlar.

---

## Bölüm 2 — İleri Düzey Pattern'lar

---

### Pattern 6: Calibrated Uncertainty

**Problem:** Model her zaman güvenli konuşuyor. Belirsizliği ifade etmiyor. Siz de çıktıya hak ettiğinden fazla güveniyorsunuz.

**Çözüm:** Modeli belirsizliğini açıkça işaretlemeye zorlayın.

```
Her iddia için güven seviyeni işaretle:

[YÜKSEK] → Birden fazla güvenilir kaynakla destekleniyor
[ORTA]   → Makul ama doğrulama önerilir  
[DÜŞÜK]  → Tahmin ya da tek kaynaktan

Emin olmadığın şeyleri söyleme. İşaretle.
```

**Örnek çıktı:**
```
[YÜKSEK] Türkiye'nin 2023 e-ticaret hacmi yaklaşık 1.2 trilyon TL'dir.
[ORTA]   Bu büyüme oranı 2024'te yavaşlayabilir.
[DÜŞÜK]  Sektörün 2025 lider oyuncusu muhtemelen X olacak.
```

**Ne zaman kullanılır:** Araştırma, analiz, karar desteği — kritik bilginin doğruluğunun önemli olduğu her yerde.

---

### Pattern 7: Adversarial Prompt

**Problem:** Kendi kararınızı, planınızı veya argümanınızı test etmek istiyorsunuz ama kör noktalarınız var.

**Çözüm:** Modeli karşı taraf olarak konumlandırın.

```
Aşağıdaki iş planının en zayıf noktalarını bul.
Planı benimsemeye çalışma. En güçlü karşı argümanları üret.

Özellikle şunları sorgula:
- Temel varsayımlardan hangisi yanlışsa ne olur?
- En kötü pazar senaryosu nedir?
- Hangi operasyonel risk göz ardı edilmiş?

Sonra: Bu eleştiriler göz önüne alındığında planı nasıl güçlendirilir?

[Plan metni]
```

**Ne zaman kullanılır:** Strateji belgeleri, yatırım kararları, ürün spesifikasyonları. Pre-mortem analizi.

---

### Pattern 8: Audience Calibration

**Problem:** İçeriği doğru kitleye yazmak zor. Çok teknik veya çok basit oluyor.

**Çözüm:** Kitleyi demografik değil, davranışsal olarak tanımlayın.

```
Hedef kitle:
- Okuduklarına şüpheyle yaklaşır, kanıt ister
- Zamanı kıt, her cümle iş yapmalı
- Teknik terimleri bilir ama jargon sevmez
- "Neden önemli?" sorusunu her paragrafta sorar

Bu kitleye yaz: [içerik]
```

**Davranışsal tanım > Demografik tanım:**
- ❌ "35-45 yaş, erkek, yönetici"  
- ✅ "Karar vermeden önce üç referans sorar, satış dilinden hızla sıkılır, rakamlarla ikna olur"

---

### Pattern 9: Format Mirroring

**Problem:** Model çıktısını doğrudan bir sisteme ya da şablona entegre etmeniz gerekiyor. Format uyumsuzluğu el işi gerektiriyor.

**Çözüm:** Tam olarak ne istediğinizi bir örnek çıktıyla gösterin.

```
Aşağıdaki formatta çıktı ver. Formatı değiştirme.
Her alan için köşeli parantez içindeki talimatı uygula.

```json
{
  "title": "[15 kelimeden kısa, eylem fiiliyle başlayan başlık]",
  "summary": "[2 cümle, problem + çözüm]",
  "tags": ["[kategori1]", "[kategori2]", "[kategori3]"],
  "priority": "[HIGH|MEDIUM|LOW]",
  "estimated_impact": "[sayısal etki tahmini, varsa]"
}
```

Girdi: [içerik]
```

**Ne zaman kullanılır:** API entegrasyonu, veritabanı doldurma, pipeline girişleri, Notion/Airtable otomasyonu.

---

### Pattern 10: Socratic Prompting

**Problem:** Modelden doğrudan cevap değil, sizi doğru cevaba götürecek sorular istiyorsunuz.

**Çözüm:** Modeli öğretmen konumuna koyun.

```
Aşağıdaki problemi bana çözmek yerine, 
beni çözüme götürecek 5 soru sor.

Sorular şu kriterleri karşılamalı:
- Cevabı bilgi değil, düşünme gerektiriyor
- Birbirini hiyerarşik olarak besliyor
- Son soruyu yanıtlayan kişi çözüme ulaşmış olacak

Problem: [problem]
```

**Ne zaman kullanılır:** Öğrenme, coaching, karar çerçeveleme, karmaşık problem çözme.

---

## Bölüm 3 — Anti-Pattern'lar

Bunları tanıyın. Kendinizde görürseniz duraksayın.

---

### Anti-Pattern 1: The Vague Imperative

```
# Bunlar anti-pattern
"İyi bir yazı yaz."
"Kapsamlı bir analiz yap."
"Detaylı bir plan hazırla."
```

**Problem:** "İyi", "kapsamlı", "detaylı" — model için anlamsız. Kendi standardını kullanır.

**Düzeltme:** Ne istediğinizi ölçülebilir ya da örneklenebilir olarak tanımlayın.

```
"Yönetici için yazı: 200 kelime, 3 paragraf, 
her paragraf bir bulguyla başlıyor."
```

---

### Anti-Pattern 2: The Loaded Question

```
# Anti-pattern
"Bu stratejinin neden harika olduğunu açıkla."
"Bu ürünün üstünlüklerini listele."
```

**Problem:** Modele sonucu önceden söylüyorsunuz. Model o yönde argüman üretiyor — zayıf yönleri görmüyor.

**Düzeltme:** Tarafsız çerçeveleme.

```
"Bu stratejiyi değerlendir: Güçlü yönler, zayıf yönler, 
varsayımlar, riskler."
```

---

### Anti-Pattern 3: The Infinite Canvas

```
# Anti-pattern
"Her şeyi anlat."
"Tüm seçenekleri listele."
"Kapsamlı bir rehber yaz."
```

**Problem:** Sınırsız görev → model ne kadar yazacağını bilmiyor. Ya çok kısa ya da anlamsız uzun çıktı.

**Düzeltme:** Kapsam sınırlayın.

```
"En kritik 3 seçeneği listele. Her biri için: 
ne, neden, ne zaman. Listeden öte gitme."
```

---

### Anti-Pattern 4: The Phantom Constraint

```
# Anti-pattern
"Bana bir e-posta yaz. Kısa olsun."
```

**Problem:** "Kısa" belirsiz. Model için 5 cümle de kısa, 15 cümle de.

**Düzeltme:** Sayısal ya da yapısal kısıt.

```
"3 paragraf, toplam 120 kelime, tek CTA."
```

---

### Anti-Pattern 5: The Assumed Expert

```
# Anti-pattern (hedef kitle belirtilmemiş)
"Yapay zeka etik meselesini açıkla."
```

**Problem:** Model "ortalama okuyucu" varsayıyor. Bu okuyucu siz değilsiniz.

**Düzeltme:** Kitleyi her zaman belirtin.

```
"Yapay zeka etik meselesini açıkla.
Okuyucu: Teknik altyapısı olmayan, 
etik tartışmalarla yeni tanışan 
bir şirket yöneticisi."
```

---

### Anti-Pattern 6: The Hallucination Invitation

```
# Anti-pattern
"2024'teki en başarılı 10 Türk AI startup'ını listele."
"Dr. Ahmet Yılmaz'ın bu konudaki görüşü nedir?"
"X şirketinin son çeyrek geliri ne kadar?"
```

**Problem:** Model bilmediği şeyleri üretiyor. Bu sorular modeli halüsine etmeye davet ediyor.

**Düzeltme A:** Bilgisini sorgulayın.

```
"Bu listeyi oluşturabilir misin? Eğer güncel veriye 
erişimin yoksa veya emin değilsen belirt."
```

**Düzeltme B:** Veriyi siz sağlayın.

```
"Aşağıdaki listeyi analiz et: [liste]"
```

**Düzeltme C:** Web araması olan araç kullanın.

---

### Anti-Pattern 7: The Context Dump

```
# Anti-pattern
[2000 kelime bağlam metni]
...
"Şimdi bana 50 kelimelik bir özet ver."
```

**Problem:** Modelin bağlam penceresinin büyük bölümünü siz doldurdunuz. Model hangi kısmın önemli olduğunu bilmiyor.

**Düzeltme:** Bağlamı hedefe göre filtreleyin. Ya da "Bu bağlamdan sadece X ile ilgili kısmı kullan" deyin.

---

### Anti-Pattern 8: The Recursive Vagueness

```
# Anti-pattern (her katman belirsiz)
"Güzel bir pazarlama metni yaz, 
müşterilerimize hitap etsin, 
ürünümüzü iyi anlatsın."
```

**Problem:** "Güzel", "hitap etsin", "iyi anlatsın" — her kelime belirsiz. Belirsizlik üstüne belirsizlik.

**Düzeltme:** Her belirsiz kelimeyi somutlaştırın.

```
"Güzel" → "Okunduğunda 'bu benim için' hissettiren"
"Hitap etsin" → "30-40 yaş, teknolojiye meraklı, 
                zaman kıtlığı yaşayan anneler için"
"İyi anlatsın" → "Ürünün 3 spesifik faydasını, 
                 rakipten farkını, fiyat gerekçesini"
```

---

## Bölüm 4 — Sektöre Özel Pattern Notları

---

### Finans ve Hukuk

```
Her finansal/hukuki çıktıda şunu ekleyin:
"Bu çıktı bilgi amaçlıdır. 
Profesyonel danışmanlık yerine geçmez. 
Emin olmadığın noktalarda [DOĞRULAMA GEREKİR] işareti koy."
```

Neden: Model hukuki ya da finansal olgularda halüsine edebilir. Bu uyarı hem modeli hem sizi korur.

---

### İnsan Kaynakları

```
CV değerlendirme, performans yorumu, işe alım kararı gibi 
görevlerde şunu ekleyin:
"Bu değerlendirmede isim, cinsiyet, yaş, 
etnik köken referansı yapma. 
Sadece iş performansı ve yetkinlik."
```

Neden: Model eğitim verisindeki önyargıları taşıyabilir. Explicit kısıt bu riski azaltır.

---

### Müşteri İletişimi

```
Müşteriye gidecek her içerikte:
"Bu metin [şirket adı] adına gönderilecek. 
İddia etme: Sadece kanıtlayabildiğimiz şeyleri yaz.
Taahhüt verme: 'Kesinlikle', 'garanti' kelimelerini kullanma.
Hukuki risk içeren ifadelerden kaçın."
```

---

## Hızlı Referans Kartı

| İhtiyaç | Pattern |
|---------|---------|
| Tutarlı ton/uzmanlık | Persona Lock |
| Çok boyutlu analiz | Perspective Rotation |
| Modelin varsayılanını kırmak | Constraint Inversion |
| Uzun yapılandırılmış çıktı | Scaffold and Fill |
| Karmaşık görevi böl | Progressive Disclosure |
| Belirsizliği yönet | Calibrated Uncertainty |
| Kendi planını test et | Adversarial Prompt |
| Doğru kitleye yaz | Audience Calibration |
| Pipeline entegrasyonu | Format Mirroring |
| Öğrenme / coaching | Socratic Prompting |

---

*→ [Modül 2: Prompt Mimarisi](../modules/02-prompt-architecture/)*  
*→ [Örnek Şablonlar](../examples/templates/)*
