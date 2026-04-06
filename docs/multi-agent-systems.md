# Multi-Agent Sistemler: Ne Zaman Neden?

*Bu makale teorik değil. "Ne zaman inşa etmeli, ne zaman kaçınmalı" sorusuna odaklanıyor.*

---

## Neden Birden Fazla Agent?

Tek agent yaklaşımının üç temel sınırı var:

**1. Bağlam penceresi dolumu**  
Büyük görevlerde tek agent bağlam penceresini dolduruyor. Bir agent 50 sayfayı okuyup analiz edip rapor yazarsa — ya analiz sığmaz, ya rapor sığmaz.

**2. Perspektif tekliği**  
Tek bir modelin "güvenlik uzmanı" ve "performans uzmanı" gibi davranmasını isteyebilirsiniz. Mümkün — ama aynı anda ikisi olmak çelişkili.

**3. Paralel çalışma imkansızlığı**  
Sıralı çalışma. Üç analiz yapmak istiyorsanız üçünü sırayla yapıyor. Paralel değil.

Multi-agent bu üç sorunu çözüyor — ama karmaşıklık ekliyor.

---

## Temel Desenler

### 1 — Supervisor + Worker

```
                    ┌──────────────┐
                    │  Supervisor  │
                    │   Agent      │
                    └──────┬───────┘
              ┌────────────┼────────────┐
              ↓            ↓            ↓
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ Worker 1 │ │ Worker 2 │ │ Worker 3 │
        │ (Araştır)│ │ (Yaz)    │ │ (Doğrula)│
        └──────────┘ └──────────┘ └──────────┘
```

**Ne zaman kullanılır:** Büyük bir görevi alt görevlere bölmek gerektiğinde. Supervisor planlar, worker'lar uygular.

**Örnek:** Pazar araştırması raporu. Supervisor: "Önce rakipleri araştır, sonra pazar verilerini topla, sonra rapor yaz." Her iş farklı worker'a gidiyor.

**Risk:** Supervisor'ın planı yanlışsa her şey yanlış gidiyor. Supervisor'ı test edin.

---

### 2 — Paralel Uzmanlar + Sentez

```
┌──────────────────────────────────────────────────┐
│                   Orkestratör                    │
└──────┬──────────────────────────────┬────────────┘
       ↓                              ↓            
┌──────────────┐              ┌──────────────┐    
│  Güvenlik    │              │  Performans  │    
│  Uzmanı      │              │  Uzmanı      │    
└──────┬───────┘              └──────┬───────┘    
       └──────────────┬──────────────┘            
                      ↓                            
               ┌──────────────┐                   
               │  Sentezleyici│                   
               └──────────────┘                   
```

**Ne zaman kullanılır:** Aynı problemi birden fazla perspektiften değerlendirmek gerektiğinde.

**Örnek:** Örnek 15'teki kod review sistemi. Her agent farklı boyuta odaklanıyor, sentez agent'ı birleştiriyor.

**Risk:** Uzmanlar çelişkili öneriler verebilir. Sentezleyici bunu nasıl yönetiyor?

---

### 3 — Boru Hattı (Pipeline)

```
Girdi → [Agent 1] → [Agent 2] → [Agent 3] → Çıktı
```

**Ne zaman kullanılır:** Her adımın çıktısı bir sonrakinin girdisi olduğunda. Sıralı, öngörülebilir akış.

**Örnek:** Örnek 13'teki belge analiz pipeline'ı.

**Risk:** Bir adımdaki hata sonraki tüm adımlara yayılıyor. Adım çıktılarını kontrol edin.

---

### 4 — Uzman Panel (Debate)

```
         Soru
           ↓
    ┌──────┴──────┐
    ↓             ↓
[Savunucu]   [Eleştirmen]
    ↓             ↓
    └──────┬──────┘
           ↓
       [Hakem]
           ↓
         Karar
```

**Ne zaman kullanılır:** Kritik kararlar için. Bir agent karar üretiyor, diğeri eleştiriyor, hakem sentezliyor.

**Örnek:** Yatırım kararı analizi. Boğa case'i vs. ayı case'i vs. gerçekçi değerlendirme.

**Risk:** Yavaş. Her karar için 3 API çağrısı. Sadece gerçekten önemli kararlar için kullanın.

---

## Ne Zaman Multi-Agent'tan Kaçınmalı?

Multi-agent her sorunu çözmüyor. Bazen kötü seçim:

**Senaryo:** "Bir e-postaya yanıt yaz" için 3 agent kurmak.  
**Sorun:** Overcomplicated. Tek iyi prompt yeterli.

**Senaryo:** Her görev için yeni agent kurgusu.  
**Sorun:** Hata yüzey alanı büyüyor. Hata ayıklama çok zor.

**Senaryo:** Agent'ların birbirinin çıktısını doğrulamadan kullanması.  
**Sorun:** Hata birikimi. 5 agent, her %90 doğruluk = %59 sistem doğruluğu.

**Karar ağacı:**

```
Görev tek LLM çağrısıyla çözülür mü?
→ Evet: Tek prompt kullan
→ Hayır ↓

Adımlar önceden belirli ve sabit mi?
→ Evet: Prompt zinciri kur
→ Hayır ↓

Farklı uzmanlıklar gerekiyor mu veya paralel çalışma avantaj sağlıyor mu?
→ Evet: Multi-agent değerlendir
→ Hayır: Tek, iyi tasarlanmış agent yeter
```

---

## Üretim İçin Kritik Kontrol Listesi

Multi-agent sistemi production'a almadan önce:

**Hata yönetimi:**
- [ ] Her agent başarısız olabilir — sistem nasıl davranıyor?
- [ ] Kısmi başarı nasıl ele alınıyor? (3/5 agent başarılı olduysa)
- [ ] Kullanıcıya ne gösteriliyor başarısızlıkta?

**İzleme:**
- [ ] Her agent çağrısı loglanıyor mu?
- [ ] Toplam maliyet izleniyor mu?
- [ ] Hangi adımda ne kadar sürdüğü biliniyor mu?

**Güvenlik:**
- [ ] Agent'lar ne yapabilir, ne yapamaz? (Yetki sınırları)
- [ ] Hassas veriler hangi agent'lara gidiyor?
- [ ] İnsan onayı gerektiren noktalar belirli mi?

**Ölçek:**
- [ ] Eş zamanlı 10 kullanıcı olursa ne olur?
- [ ] API rate limit'leri yönetildi mi?
- [ ] Maliyet tahmini yapıldı mı?

---

## Gerçek Dünya Beklenti Yönetimi

2024-2026 durumu dürüstçe:

**İyi çalışıyor:**
- Belge işleme pipeline'ları (doküman → özet, doküman → veri)
- Kod review otomasyonu (güvenlik, kalite, performans)
- Araştırma asistanı (web araştırma + sentez)
- Müşteri destek sınıflandırma + yönlendirme

**Dikkatli olun:**
- Tamamen otonom, uzun vadeli görevler (hâlâ kırılıyor)
- Kritik finansal ya da hukuki kararların otomasyonu
- "Herhangi bir soruya cevap ver" tipi genel asistanlar

**Henüz gerçekten çalışmıyor:**
- Uzun vadeli öğrenme (her konuşma sıfırdan başlıyor)
- Gerçek anlamda yaratıcı inisyatif ("ne yapmam gerektiğini sen bul")
- İnsan düzeyinde akıl yürütme gerektiren belirsiz problemler

---

## Araç Önerileri (2025 itibarıyla)

| İhtiyaç | Araç | Neden |
|---------|------|-------|
| Basit zincirler | LangChain | Geniş ekosistem, iyi dökümantasyon |
| Karmaşık akışlar | LangGraph | State machine, döngü desteği |
| Production agent'lar | AutoGen (Microsoft) | Multi-agent framework, debug araçları |
| No-code başlangıç | n8n, Make | Kod yazmadan pipeline |
| Enterprise | Vertex AI Agent Builder | GCP entegrasyonu, ölçek |

---

*→ [Modül 3'e dön](../modules/03-agent-thinking/)*  
*→ [İleri Düzey Örnekler](../examples/advanced/)*
