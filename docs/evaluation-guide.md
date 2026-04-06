# Prompt Kalitesi Nasıl Ölçülür?

> "Çalışıyor" bir ölçüt değil. "Ne kadar iyi çalışıyor?" sorusu ölçüt.

Bu rehber bireysel değerlendirmeden ekip standardına, oradan otomatik testlere kadar bir hiyerarşi sunuyor.

---

## Neden Ölçüm Önemli?

Prompt geliştirmek iteratif bir süreç. İterasyon olmadan gelişim olmaz. Gelişim ölçülmezse başarı ya da başarısızlık rastgele.

Üç senaryo:

1. **Tek seferlik görev:** Ölçüm gerekmez. Çıktı işinize yararsa tamam.
2. **Tekrarlayan görev:** Basit ölçüm şart. Her seferinde aynı kaliteyi istiyorsunuz.
3. **Sistem/pipeline:** Sistematik ölçüm zorunlu. Çıktı kalitesi iş sürecinizi etkiliyor.

---

## Düzey 1 — Bireysel Değerlendirme (5 Dakika)

Hızlı kalibrasyon için. Ekip gerektirmiyor.

### Skor Kartı

```
Prompt değerlendirme — Skor kartı

Görev: _______________________________
Tarih: _______________________________

[ ] Doğruluk         — Çıktıdaki iddialar doğru mu?           /5
[ ] Tamlık           — İstenen her şey var mı?                  /5
[ ] Ton uyumu        — Beklenen tona uyuyor mu?                 /5
[ ] Format uyumu     — İstenen formatta mı?                     /5
[ ] Kullanıma hazır  — Düzenleme olmadan kullanılabilir mi?     /5

Toplam: /25

Eşik:
22-25 → Production'a hazır
16-21 → Küçük düzeltme gerek
10-15 → Prompt yeniden yazılmalı
<10   → Yaklaşım değişmeli
```

### Kullanışlı Heuristikler

**"5 dakika testi":** Çıktıyı aldıktan 5 dakika sonra ne kadar düzelttiniz? Hiç düzeltme → çok iyi. 5+ değişiklik → prompt zayıf.

**"Teslim testi":** Bu çıktıyı hiç okumadan müşteriye ya da yöneticinize gönderilebilir mi? Evet → production kalitesi. Hayır → neden değil?

**"Tekrar testi":** Aynı promptu 3 kez çalıştırın. Her seferinde kullanılabilir çıktı geldi mi? 3/3 → güvenilir. 1/3 → sorunlu.

---

## Düzey 2 — Karşılaştırmalı Değerlendirme (A/B)

İki prompt versiyonu arasında karar vermek için.

### A/B Test Protokolü

```
Test edilen değişken: _________________
(sadece bir şeyi değiştirin — format, ton, kısıt vs.)

Prompt A: [orijinal]
Prompt B: [değiştirilen]

Test seti: Minimum 5 farklı girdi
Her girdide her iki promptu çalıştır

Değerlendirme kriteri (bu test için en önemli 1-2 şey):
Kriter 1: _____________ (ağırlık: ___)
Kriter 2: _____________ (ağırlık: ___)
```

### Sonuç Tablosu

```
| Girdi | A Skoru | B Skoru | Kazanan |
|-------|---------|---------|---------|
| 1     |         |         |         |
| 2     |         |         |         |
| 3     |         |         |         |
| 4     |         |         |         |
| 5     |         |         |         |
| ORTALAMA |      |         |         |
```

**Karar kuralı:** Fark ≥1.0 puan ise kazanan açık. Daha küçük fark → tesadüf olabilir, 10 girdi ile tekrarlayın.

---

## Düzey 3 — Ekip Standardı

Birden fazla kişi aynı promptu kullanıyorsa tutarlılık kritik.

### Referans Seti Oluşturma

```
Adım 1: "Altın standart" 5-10 örnek seç
(Hepinizin "bu mükemmel" dediği çıktılar)

Adım 2: Her örnek için şunu belgele:
- Girdi: Ne soruldu?
- Beklenen çıktı: Nasıl görünmeli?
- Kabul kriterleri: Ne olursa "geçti"?
- Red kriterleri: Ne olursa "reddedildi"?

Adım 3: Yeni prompt → bu örneklere karşı test et
Adım 4: Eşik belirle (örn: 8/10 örnekte geçmeli)
```

### Sürüm Kontrolü

```
# prompts/email-outreach/v1.md
Versiyon: 1.0
Tarih: Mart 2025
Ortalama skor: 18/25
Bilinen sınırlar: Teknik okuyucularda ton çok kasıtlı

# prompts/email-outreach/v2.md
Versiyon: 2.0
Tarih: Nisan 2025
Değişiklik: Ton kısıtı güncellendi
Ortalama skor: 22/25
```

---

## Düzey 4 — Otomatik Değerlendirme (LLM-as-Judge)

Büyük hacimde prompt testi için. Model, modeli değerlendiriyor.

### Evaluator Prompt

```python
EVALUATOR_PROMPT = """
Sen titiz bir içerik kalite değerlendiricisisin.
Aşağıdaki çıktıyı verilen kriterlere göre değerlendir.

Değerlendirme kriterleri:
{criteria}

Değerlendirilen çıktı:
{output}

Orijinal görev:
{task}

Her kriter için 1-5 puan ver ve kısa gerekçe yaz.
Sonunda: genel skor (ağırlıklı ortalama) ve tek cümle özet.

Format (JSON):
{{
  "scores": {{
    "kriter_1": {{"puan": X, "gerekce": "..."}},
    "kriter_2": {{"puan": X, "gerekce": "..."}}
  }},
  "genel_skor": X.X,
  "ozet": "..."
}}
"""

def evaluate_output(task: str, output: str, criteria: dict) -> dict:
    """
    LLM'i hakem olarak kullanarak çıktıyı değerlendir.
    
    criteria örneği:
    {
        "dogruluk": {"agirlik": 0.4, "aciklama": "İddialar doğru mu?"},
        "ton": {"agirlik": 0.3, "aciklama": "Beklenen tona uyuyor mu?"},
        "format": {"agirlik": 0.3, "aciklama": "Doğru formatta mı?"}
    }
    """
    from langchain_openai import ChatOpenAI
    import json
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    criteria_text = "\n".join([
        f"- {k} (ağırlık: {v['agirlik']}): {v['aciklama']}"
        for k, v in criteria.items()
    ])
    
    prompt = EVALUATOR_PROMPT.format(
        criteria=criteria_text,
        output=output,
        task=task
    )
    
    response = llm.invoke(prompt)
    
    # JSON parse
    try:
        result = json.loads(response.content)
    except json.JSONDecodeError:
        # Model bazen markdown backtick ekliyor
        clean = response.content.strip("```json\n```").strip()
        result = json.loads(clean)
    
    return result


# Örnek kullanım:
task = "Müşteriye gecikme bildirimi e-postası yaz"
output = """Sayın Müşterimiz,

Siparişinizde yaşanan gecikme için özür dileriz. 
Kargonuz 3 iş günü içinde elinize ulaşacaktır.

Saygılarımızla"""

criteria = {
    "empati": {"agirlik": 0.3, "aciklama": "Müşterinin hayal kırıklığını kabul ediyor mu?"},
    "net_bilgi": {"agirlik": 0.4, "aciklama": "Gecikme süresi ve sonraki adım net mi?"},
    "ton": {"agirlik": 0.3, "aciklama": "Şirket imajına uygun mu?"}
}

result = evaluate_output(task, output, criteria)
print(f"Genel skor: {result['genel_skor']}/5")
print(f"Özet: {result['ozet']}")
```

### LLM-as-Judge Uyarıları

**Tutarsızlık riski:** Aynı çıktıyı iki kez değerlendirirseniz farklı puan alabilirsiniz. Evaluator için `temperature=0` kullanın.

**Halo etkisi:** Uzun, iyi görünen çıktılar gerçekte kötü olsa bile yüksek puan alabilir. Criteria'yı somut tutun.

**Kendi kendini övme:** Evaluator olarak aynı modeli kullanıyorsanız (hem üretici hem hakem GPT-4o), model kendi çıktısını favore edebilir. Farklı model kullanın ya da insan değerlendirmeyle kalibre edin.

---

## Düzey 5 — Production Monitoring

Sistem canlıya geçtikten sonra kaliteyi izlemek için.

### İzlenecek Metrikler

```python
# Her API çağrısında loglanacak minimum set
{
    "timestamp": "2025-04-06T10:23:11",
    "prompt_version": "email-outreach-v2.1",
    "input_tokens": 523,
    "output_tokens": 187,
    "latency_ms": 1240,
    "model": "gpt-4o",
    "cost_usd": 0.0042,
    
    # Kalite sinyalleri (iş verisiyle bağlantılı)
    "user_edited": true,           # Kullanıcı çıktıyı düzeltti mi?
    "user_rejected": false,        # Tamamen reddedildi mi?
    "downstream_success": null     # E-posta açıldı mı? (sonraki aşamada)
}
```

### Alarm Eşikleri

```
Uyarı:   user_rejected_rate > %15 (son 100 çağrı)
Kritik:  user_rejected_rate > %30
Uyarı:   ortalama_latency > 3000ms
Kritik:  hata_oranı > %5
```

**Drift tespiti:** Aynı prompt zamanla farklı sonuç verebilir (model güncellemeleri, bağlam değişimi). Haftalık otomatik test setini çalıştırın.

---

## Çerçeve Seçim Kılavuzu

```
Kaç kez kullanılacak?
│
├─ 1 kez → Değerlendirme gerekmez
│
├─ haftalık < 10 kullanım
│   └─ Düzey 1: Skor kartı yeterli
│
├─ günlük 10-100 kullanım  
│   ├─ Düzey 2: A/B test + temel log
│   └─ Düzey 3: Ekip standardı (birden fazla kullanıcıysa)
│
└─ günlük 100+ kullanım / pipeline
    ├─ Düzey 4: LLM-as-judge (spot check)
    └─ Düzey 5: Production monitoring
```

---

*→ [Prompt Pattern Kataloğu](prompt-patterns.md)*  
*→ [İleri Düzey Örnekler](../examples/advanced/)*
