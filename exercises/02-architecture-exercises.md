# Egzersizler — Modül 2: Prompt Mimarisi

---

## Egzersiz 2.1 — Peer Review Atölyesi

**Süre:** 20 dakika (10 yazma + 10 değerlendirme)  
**Gruplar:** İkili çalışma önerilir (tercihen biri teknik, biri değil)

**Adım 1:** Her kişi kendi işinden bir görev seçsin ve prompt yazar. (10 dk)

**Adım 2:** Partner'ın promptunu aşağıdaki şablonla değerlendirin:

```
İncelenen prompt: ___________________________

Katman kontrolü:
[ ] Rol var mı?         → Varsa: _____________ / Yoksa ekle: _____________
[ ] Bağlam var mı?      → Varsa: _____________ / Yoksa ekle: _____________  
[ ] Görev net mi?       → Varsa: _____________ / Belirsizse düzelt: _______
[ ] Kısıt var mı?       → Varsa: _____________ / Önerim: ________________
[ ] Format var mı?      → Varsa: _____________ / Önerim: ________________

En güçlü yön: _______________________
En önemli eksik: ____________________
Düzeltilmiş versiyon (birlikte yazın): 

[Promptun yeni versiyonu]
```

---

## Egzersiz 2.2 — Teknik Seçim Senaryosu

Aşağıdaki senaryolarda hangi tekniği kullanırdınız? Neden?

**Teknikler:** Chain-of-Thought / Few-Shot / Self-Consistency / Hepsi / Hiçbiri

---

**Senaryo A:** E-ticaret sitesi için 200 ürün açıklaması yazılacak. Her açıklama aynı formatta ve tonda olmalı.

```
Teknik: ____________
Neden: _____________________________________________
```

---

**Senaryo B:** Şirketin yeni pazara girip girmemesi kararı için AI'dan analiz isteniyor.

```
Teknik: ____________
Neden: _____________________________________________
```

---

**Senaryo C:** Bir matematiksel finans modeli doğrulanacak.

```
Teknik: ____________
Neden: _____________________________________________
```

---

**Senaryo D:** Müşteri yorumlarından marka algısı çıkarılacak (1000 yorum).

```
Teknik: ____________
Neden: _____________________________________________
```

---

**Cevap anahtarı:**
- A: Few-shot (format tutarlılığı kritik)
- B: Self-consistency + CoT (yüksek riskli, akıl yürütme gerekli)
- C: CoT (adım adım doğrulama + self-consistency)
- D: Few-shot (sınıflandırma tutarlılığı) + Self-consistency (şüpheli vakalar için)

---

## Egzersiz 2.3 — "Daha İyi" Yarışması

**Süre:** 15 dakika  
**Amaç:** Aynı sonucu iki farklı yoldan almak, hangisinin daha iyi çalıştığını ölçmek.

İki kişi aynı görevi farklı promptlarla çalıştırır.

**Görev:** "Şirketimizde home office politikasını değerlendiren bir not hazırla."

**Kişi A:** 5 katmanı kullanarak mümkün olan en iyi promptu yazar.  
**Kişi B:** Spontane, doğal bir şekilde promptu yazar (nasıl aklına geliyorsa).

İki çıktıyı şu kriterlere göre karşılaştırın (1-5):

| Kriter | A | B |
|--------|---|---|
| İstenen tona uygunluk | | |
| Yapısallık | | |
| Kullanıma hazır olma | | |
| Düzenleme gerektiriyor mu? | | |

---

# Egzersizler — Modül 3: Agent Düşüncesi

---

## Egzersiz 3.1 — "Agent mı, Değil mi?" Analizi

Aşağıdaki görevler için: Bu görev için agent gerekli mi, zincir mi, yoksa tek prompt yeter mi?

| Görev | Kararınız | Gerekçe |
|-------|-----------|---------|
| Haftalık satış raporunu özetle | | |
| Rakipleri izle, önemli haberlerde uyarı ver | | |
| Müşteri e-postasına yanıt taslağı oluştur | | |
| LinkedIn'den potansiyel adayları bul, profillerini karşılaştır | | |
| PDF sözleşmeden maddeleri çıkar | | |
| Kodun hatalarını bul ve düzelt, test et, raporla | | |

---

**Kılavuz:**
- **Tek prompt:** Sabit giriş, sabit çıkış, araç gerekmez
- **Zincir:** Çok adım ama adımlar önceden bilinir
- **Agent:** Adımlar veriye bağlı, araç gerekli, dinamik karar var

---

## Egzersiz 3.2 — Agent Taslak Tasarımı

**Süre:** 10 dakika  
**Kağıt kalemle yapın. Kodlamaya gerek yok.**

Kendi işinizden tekrar eden, kurallarla tanımlanabilir bir görev seçin.

```
AGENT TASLAK KARTI

Görev adı: _______________________________

Tetikleyici: Ne olunca çalışır?
→ ___________________________________________

Hedef: Başarı nasıl görünür?
→ ___________________________________________

Veri kaynakları: Nereden okur?
→ [ ] Web  [ ] İç sistem  [ ] E-posta  [ ] Dosya  [ ] Diğer: ___

Yazma izinleri: Nereye yazar?
→ [ ] Rapor  [ ] E-posta  [ ] Veritabanı  [ ] Hiçbiri

Maksimum otonom adım: Kaç adım sonra insan onayı gerekli?
→ ___ adım

İnsan onayı zorunlu noktalar:
1. _____________________________________________
2. _____________________________________________

Başarısızlık senaryosu: Bir araç başarısız olursa ne olur?
→ ___________________________________________

Fayda tahmini: Şu an kaç saat/haftada bu iş yapılıyor?
→ ___ saat/hafta
```

---

## Egzersiz 3.3 — ReAct Trace Okuma

Bir agent'ın "düşünce akışı" (trace) aşağıda. Her adımı analiz edin.

```
Hedef: "Bu aydaki müşteri şikayetlerinin ana kategorilerini bul"

Düşünce: Müşteri şikayetleri veritabanında olmalı. 
         Önce hangi tabloların olduğunu bakayım.
Hareket: db_query("SHOW TABLES")
Gözlem: complaints, users, products, orders

Düşünce: complaints tablosunda bu ay ne var?
Hareket: db_query("SELECT category, COUNT(*) FROM complaints 
                   WHERE MONTH(created_at) = MONTH(CURDATE()) 
                   GROUP BY category ORDER BY COUNT(*) DESC")
Gözlem: Error: Column 'category' doesn't exist

Düşünce: Kategori sütunu yok. Tablo yapısına bakmalıyım.
Hareket: db_query("DESCRIBE complaints")
Gözlem: id, user_id, text, status, created_at, resolved_at

Düşünce: Hazır kategori yok. Şikayet metinlerini okuyup 
         kategorize etmem gerekecek. Ama kaç şikayet var?
Hareket: db_query("SELECT COUNT(*) FROM complaints 
                   WHERE MONTH(created_at) = MONTH(CURDATE())")
Gözlem: 847

Düşünce: 847 metin — hepsini okuyamam (token limiti). 
         Örnekleme yapmalıyım. 50 rastgele örnek al, 
         kategorileri tespit et, sonra hepsini o kategorilerle etiketle.
Hareket: db_query("SELECT text FROM complaints 
                   WHERE MONTH(created_at) = MONTH(CURDATE()) 
                   ORDER BY RAND() LIMIT 50")
```

**Sorular:**

1. Agent hangi adımda beklenmeden "akıllı" davrandı?
   → ___________________________________________

2. "Column doesn't exist" hatasıyla nasıl başa çıktı?
   → ___________________________________________

3. 847 şikayet problemini nasıl çözdü? Bu iyi bir çözüm mü?
   → ___________________________________________

4. Bu agent'ta görmek istediğiniz ama olmayan bir şey var mı?
   → ___________________________________________

---

**Sonraki adım:** [İleri Düzey Örnekler](../examples/advanced/)
