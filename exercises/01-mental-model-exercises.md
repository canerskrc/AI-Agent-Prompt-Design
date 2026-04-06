# Egzersizler — Modül 1: Zihinsel Model

Eğitimde yaptığımız aktivitelerin yazılı versiyonu. Kendi başınıza ya da ekibinizle yapabilirsiniz.

---

## Egzersiz 1.1 — Prompt Otopsisi

**Süre:** 15 dakika  
**Amaç:** Bir "kötü prompt"un neden kötü çalıştığını analiz etmek.

**Adımlar:**

1. Geçen 2 haftada bir AI'dan hayal kırıklığı yaratan çıktıyı düşünün.
   - Yoksa şunu kullanın: `"Şirketimiz için dijital dönüşüm planı yaz."`

2. O sırada yazdığınız promptu (ya da örnek promptu) yazın:

```
Promptum: ___________________________________
```

3. Şu soruları cevaplayın:

| Soru | Cevabınız |
|------|-----------|
| Model kim olduğunu biliyor muydu? | Evet / Hayır |
| Bağlamı (durum, hedef, kitle) anlattınız mı? | Evet / Kısmen / Hayır |
| Görev tek bir şeye odaklanıyor muydu? | Evet / Hayır |
| Kısıtlar vardı mı? | Evet / Hayır |
| Format belirli miydi? | Evet / Hayır |

4. Eksik olan her katman için model ne varsaydı? Yazın.

5. Promptu 5 katmanla yeniden yazın. Çalıştırın. Fark var mı?

---

## Egzersiz 1.2 — İnsan mı AI mı?

**Süre:** 10 dakika  
**Amaç:** Ton ve üslubun prompt kaynaklı olduğunu görmek.

Aşağıdaki iki metinden hangisinin hangi prompttan geldiğini tahmin edin:

**Metin 1:**
> Yapay zeka, modern organizasyonların verimliliğini ve rekabet gücünü artırmada kritik bir katalizör işlevi görmektedir. Süreç otomasyonu, karar destek sistemleri ve müşteri deneyimi optimizasyonu gibi alanlarda somut değer üretme kapasitesi, kurumsal AI benimsemesini stratejik bir zorunluluk haline getirmektedir.

**Metin 2:**
> Yapay zeka iş hayatını değiştiriyor. Ancak hangi uygulamaların gerçekten işe yaradığını ayrıştırmak kolay değil. İyi haber: Erken benimseyenlerin deneyimlerinden öğrenebiliriz.

---

**Promptlar:**

A) `"Yapay zekanın kurumsal değeri hakkında akademik bir analiz yaz."`  
B) `"Yapay zekanın iş hayatındaki etkisi hakkında bülten yazısı yaz. Okuyucu meşgul, pratik odaklı bir yönetici."`

---

Cevap: Metin 1 → Prompt A, Metin 2 → Prompt B.

**Çıkarım:** Aynı konu, farklı bağlam → tamamen farklı çıktı. Modelin "kişiliği" yok. Verdiğiniz sinyallere göre şekilleniyor.

---

## Egzersiz 1.3 — Bağlam Deneyi

**Süre:** 20 dakika  
**Amaç:** Bağlamın çıktıya etkisini ölçmek.

**Deney:**

Aynı görevi, giderek zenginleşen bağlamla 4 kez çalıştırın.

Görev: `"Bu ürünün avantajlarını anlat."` (bir ürün seçin)

**Versiyon 1 — Sıfır bağlam:**
```
Bu ürünün avantajlarını anlat: [ürün adı]
```

**Versiyon 2 — Hedef kitle bağlamı:**
```
Bu ürünün avantajlarını anlat: [ürün adı]
Hedef kitle: 50+ yaş, teknolojiye uzak, fiyat duyarlı müşteriler.
```

**Versiyon 3 — Kanal bağlamı:**
```
Bu ürünün avantajlarını anlat: [ürün adı]
Hedef kitle: 50+ yaş, teknolojiye uzak, fiyat duyarlı müşteriler.
Kanal: WhatsApp mesajı (kısa, sıcak, teknik jargon yok)
```

**Versiyon 4 — Tam bağlam:**
```
Bu ürünün avantajlarını anlat: [ürün adı]
Hedef kitle: 50+ yaş, teknolojiye uzak, fiyat duyarlı müşteriler.
Kanal: WhatsApp mesajı (kısa, sıcak, teknik jargon yok)
Müşteri objeksiyonu: "Bu kadar paraya değmez."
Amaç: Müşterinin objeksiyonunu ele al ve bir sonraki adımı (mağazayı ziyaret) öner.
```

**Notlarınız:**

| Versiyon | Çıktı kalitesi (1-5) | En büyük fark ne? |
|---------|---------------------|-------------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |

---

**Sonraki egzersiz:** [Egzersiz 2 — Prompt Mimarisi](02-architecture-exercises.md)
