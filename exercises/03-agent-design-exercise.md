# Egzersiz 3 — Agent Tasarım Atölyesi

Bu egzersiz kağıt-kalem ile yapılır. Kodlama yok.  
Süre: 15 dakika bireysel + 10 dakika paylaşım.

---

## Bölüm A — Uygun Görev Seçimi (5 dakika)

Kendi işinizden bir görev seçin. Aşağıdaki kriterlere uyan bir görev olmalı:

**İyi aday kriterleri:**
- Haftada en az 1 kez yapılıyor
- Adımlar önceden tahmin edilebilir
- Başarı/başarısızlık ölçülebilir
- Sonuç doğrulanabilir (insan kontrol edebilir)

**Zayıf aday kriterleri:**
- "Her seferinde farklı" 
- Tamamen subjektif yargı gerektiriyor
- Çok nadir yapılıyor
- Hata toleransı sıfır (finansal işlem, tıbbi karar)

**Seçtiğim görev:**
```
_____________________________________________
```

**Kriterlere uyuyor mu?** (işaretleyin)
- [ ] Düzenli tekrarlıyor
- [ ] Adımlar tahmin edilebilir
- [ ] Başarı ölçülebilir
- [ ] Sonuç doğrulanabilir

---

## Bölüm B — Agent Taslak Kartı (8 dakika)

```
════════════════════════════════════════════
          AGENT TASLAK KARTI
════════════════════════════════════════════

GÖREV ADI: _________________________________

────────────────────────────────────────────
TETİKLEYİCİ
Ne olunca çalışır?

 [ ] Belirli saatte (cron)    → ne zaman: _______
 [ ] Bir olay gerçekleşince   → hangi olay: ______
 [ ] Kullanıcı istediğinde    → nasıl isteyecek: __
 [ ] Başka sistem tetikler    → hangi sistem: _____

────────────────────────────────────────────
HEDEF
Başarılı bir çıktı nasıl görünür?
(Ölçülebilir olmalı)

→ _________________________________________

────────────────────────────────────────────
VERİ KAYNAKLARI (ne okuyacak?)

 [ ] Web / internet
 [ ] Dahili veritabanı: ____________________
 [ ] E-posta / takvim
 [ ] Dosya sistemi: ________________________
 [ ] Harici API: ___________________________
 [ ] Diğer: ________________________________

────────────────────────────────────────────
YAZMA İZİNLERİ (nereye yazacak?)

 [ ] Sadece okur, hiçbir yere yazmaz
 [ ] Rapor / özet dosyası oluşturur
 [ ] E-posta gönderir           → kime: _______
 [ ] Veritabanına yazar         → hangi tablo: _
 [ ] Form doldurur              → hangi form: __
 [ ] Başka sistemi tetikler     → hangisi: _____

────────────────────────────────────────────
OTONOM SINIR
Kaç adım sonra insan onayı gerekli?

 [ ] Her adımda insan onayı
 [ ] ___ adım sonra onay
 [ ] Sadece şu koşullarda: _________________
 [ ] Tam otonom (insan onayı yok)

────────────────────────────────────────────
İNSAN ONAYI ZORUNLU NOKTALAR

1. ________________________________________
2. ________________________________________
3. (varsa) ________________________________

────────────────────────────────────────────
BAŞARISIZLIK SENARYOSU
Bir araç başarısız olursa ne yapacak?

 [ ] Hata logla, sonraki adıma geç
 [ ] Dur ve kullanıcıya bildir
 [ ] Alternatif araçla dene
 [ ] Görevin o bölümünü atla

Kritik başarısızlık (görev durmalı):
→ _________________________________________

────────────────────────────────────────────
FAYDA TAHMİNİ

Şu an bu iş kaç saat/hafta alıyor?
→ ___ saat / hafta

Yanlış giderse etkisi ne?
→ [ ] Minör   [ ] Orta   [ ] Büyük   [ ] Kritik

════════════════════════════════════════════
```

---

## Bölüm C — Kritik Değerlendirme (2 dakika)

Tasarladığınız agent'a şu soruları sorun:

**1. Bu gerçekten agent mı gerekiyor?**
- Aynı iş tek bir iyi prompt ile yapılır mı? → _______
- Sabit adımlarla bir zincir yeter mi? → _______
- Agent gerçekten değer katıyor mu? → _______

**2. Nerede kırılır?**
- En olası başarısızlık noktası: _________________
- Bunu nasıl test edersiniz? ____________________

**3. Pilot nasıl olur?**
- Hangi küçük versiyonu önce denersiniz? _________

---

## Paylaşım

Gönüllü olarak paylaşıyorsanız, şu üçünü anlatın:
1. Görev neydi?
2. En kritik "insan onayı" noktası neresi?
3. Nerede başarısız olabileceğini düşünüyorsunuz?

---

*→ [Modül 3'e dön](../modules/03-agent-thinking/)*
