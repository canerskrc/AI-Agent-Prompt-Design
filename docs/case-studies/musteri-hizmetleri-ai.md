# Vaka Çalışması: Kurumsal Şikayet Yönetiminde AI

> **Not:** Bu vaka gerçek uygulamalardan anonimleştirilerek derlenmiştir. Şirket adları ve rakamlar değiştirilmiştir.

---

## Özet

**Şirket:** Türkiye'de faaliyet gösteren orta ölçekli e-ticaret şirketi, ~800 çalışan  
**Dönem:** 2024 Q1-Q3  
**Uygulama:** Müşteri şikayet yönetiminde AI destekli sınıflandırma ve yanıt taslağı  
**Sonuç:** Yanıt süresi %62 azaldı, müşteri memnuniyeti skoru 3.4'ten 4.1'e çıktı

---

## Başlangıç Durumu

### Problem

Müşteri hizmetleri ekibi her gün ~300 şikayet e-postası alıyordu. Süreç:

1. Destek temsilcisi e-postayı okur (ort. 3 dakika)
2. Kategori belirler (ort. 2 dakika)  
3. Uygun departmana iletir (ort. 1 dakika)
4. Yanıt taslağı yazar (ort. 8 dakika)
5. Onaya gönderir, revize eder, gönderir (ort. 5 dakika)

**Toplam:** Şikayet başına ortalama 19 dakika  
**İlk yanıt süresi:** Ortalama 4.2 saat (mesai dışı: 18+ saat)

### Ek Sorunlar

- Tutarsız sınıflandırma: Aynı şikayet farklı temsilcilere farklı kategoriye gidiyordu
- Ton tutarsızlığı: Her temsilcinin yazı stili farklı
- Kayıp şikayetler: Kategorisi belirsiz e-postalar bazen gözden kaçıyordu

---

## Çözüm Tasarımı

### Faz 1 — Sınıflandırma Otomasyonu (3 hafta)

**Yaklaşım:** Her gelen e-posta otomatik sınıflandırılıyor.

```
Kategoriler:
- ÜRÜN (hasar, kalite, beklentiden farklı)
- TESLİMAT (gecikme, kayıp, yanlış adres)
- FATURA (hatalı ücret, iade talebi)
- İADE/DEĞİŞİM
- TEKNİK (uygulama, web sitesi)
- DİĞER
```

**Kullanılan prompt (basitleştirilmiş):**

```
Rol: Müşteri hizmetleri sınıflandırma uzmanısın.

Görev: E-postayı analiz et ve JSON formatında çıktı ver.

Kısıt:
- Sadece verilen kategorileri kullan
- Birden fazla kategori varsa hepsini listele
- Güven skoru ver (0-1)
- 0.6 altı güven → "MANUEL_İNCELEME" bayrağı koy

Format:
{
  "kategoriler": ["..."],
  "aciliyet": "ACIL|NORMAL|DÜŞÜK",
  "duygu": "ÇOK_NEGATİF|NEGATİF|NÖTR",
  "güven_skoru": 0.85,
  "manuel_inceleme": false,
  "özet": "1 cümle"
}

E-posta: {email_content}
```

**Sonuç:** %91 doğruluk (insan değerlendirmesi ile karşılaştırıldığında). Güven skoru 0.6 altındaki %12 vaka manuel incelemeye gönderiliyor.

---

### Faz 2 — Yanıt Taslağı Üretimi (4 hafta)

**Yaklaşım:** Sınıflandırmadan sonra kategori + şirket politikasına göre taslak üretiliyor.

**Kritik tasarım kararı:** AI taslak üretiyor, insan onaylıyor. Tam otomasyon yok.

**Yanıt üretim promptu:**

```
Rol: Kıdemli müşteri deneyimi uzmanısın. 
     Şirketi temsil ediyorsun ama müşteri yanında duruyorsun.

Bağlam:
- Şirket: [şirket adı] e-ticaret platformu
- Durum: {durum_özeti}
- Şikayet kategorisi: {kategori}
- Müşteri değeri: {vip_statüs}
- Politika: {ilgili_politika}

Görev: Yanıt e-postası taslağı yaz.

Yapı:
1. İsmiyle hitap et
2. Deneyimi kabul et (empati, 1-2 cümle)
3. Durumu açıkla (varsa — suçlama değil, bilgi)
4. Çözümü bildir (spesifik, tarihli)
5. Kapan (tek cümle, sıcak)

Kısıt:
- "Maalesef" kelimesi YASAK
- "En kısa sürede" YASAK — tarih ver
- "Anlayışınız için teşekkür ederiz" YASAK
- VIP müşteri için ekstra bir jest öner (uygulama ekibi onaylayacak)
- 150 kelimeyi geçme

Çıktı:
- Konu satırı
- E-posta gövdesi
- [Temsilciye not]: Bu yanıtı göndermeden önce kontrol edin: [özel dikkat noktaları]
```

---

### Faz 3 — Ölçüm ve Optimizasyon (Devam ediyor)

**İzlenen metrikler:**

```python
# Her yanıt için loglanıyor
{
    "şikayet_id": "...",
    "sınıflandırma_süresi_sn": 4.2,
    "taslak_üretim_süresi_sn": 8.1,
    "temsilci_düzenleme_oranı": 0.23,  # %23 değiştirildi
    "temsilci_red_oranı": 0.04,         # %4 tamamen reddedildi
    "gönderim_süresi_dk": 6.4,
    "müşteri_geri_dönüş": "ÇÖZÜLDÜ|DEVAM|YENİ_ŞİKAYET"
}
```

---

## Sonuçlar

### Nicel

| Metrik | Önce | Sonra | Değişim |
|--------|------|-------|---------|
| Şikayet başına süre | 19 dk | 7.2 dk | -%62 |
| İlk yanıt süresi | 4.2 saat | 1.1 saat | -%74 |
| Sınıflandırma tutarlılığı | %67 | %91 | +%24 |
| Müşteri memnuniyeti (CSAT) | 3.4/5 | 4.1/5 | +%21 |
| Temsilci başına günlük şikayet | 38 | 67 | +%76 |

### Nitel

**Beklenmedik faydalar:**
- Temsilciler taslaktan başlayınca daha fazla kişiselleştirme yapıyorlar (paradoksal)
- Yeni temsilci onboarding süresi 3 haftadan 1 haftaya düştü (taslaklar referans görevi görüyor)
- Şikayet örüntüleri artık veri olarak izlenebilir hale geldi

**Beklenmedik zorluklar:**
- %4 red oranı başlangıçta daha düşük beklendi — inceleme: AI "çok resmi" yanıtlar üretiyor, temsilciler kendi sesini tercih ediyor
- Bazı temsilciler taslağı olduğu gibi gönderiyor (özelleştirme yapmıyor) — bu istenmiyordu

---

## Öğrenilen Dersler

### Teknik

**1. Güven eşiği kritik**  
%100 otomasyon hedeflemek yerine güven eşiği koymak (0.6) hem kaliteyi korudu hem ekibi rahatlattı. "Şüpheli vakalar manuel incelemeye" yaklaşımı direnci azalttı.

**2. Prompt versiyonlamaya yatırım yapın**  
İlk 6 haftada 23 farklı prompt versiyonu denendi. Her versiyon numaralandı, performans takip edildi. En iyi üç versiyonun karışımı production'a alındı.

**3. "Temsilciye not" bölümü oyun değiştirici**  
Yanıt taslağının sonuna "Bunu göndermeden kontrol edin: [özel not]" eklemek temsilcinin kontrolünü artırdı, sahiplenmeyi güçlendirdi.

### Organizasyonel

**1. Şampiyon-önce yaklaşımı**  
Tüm ekibe aynı anda açmak yerine 3 istekli temsilciyle başlandı. Onlar deneyimlerini paylaşınca benimseme hızlandı.

**2. "AI yanıt gönderecek" korkusunu adresin**  
"AI taslak üretiyor, sen gönderin" mesajı net tutuldu. Kontrol temsilcide. Bu kritikti.

**3. Başarısızlık şeffaf paylaşıldı**  
İlk 2 haftada çıkan kötü yanıtlar ekiple paylaşıldı, ne öğrenildiği anlatıldı. Şeffaflık güven yarattı.

---

## Tekrar Edilebilirlik

Bu uygulama başka kurumsal şikayet yönetimi bağlamlarında çalışır — finans, telecom, perakende. Kritik uyarlama noktaları:

1. Kategori listesi sektöre özel
2. Şirket politikası prompt'a eklenmeli
3. Ton ve hitap tarzı şirket kültürüne göre ayarlanmalı
4. Güven eşiği ilk haftalarda test edilmeli

---

*→ [Agent Örnekleri](../../examples/advanced/)*  
*→ [Türkiye Bağlamı](../turkish-context.md)*
