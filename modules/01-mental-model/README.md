# Modül 1 — Zihinsel Model

> Prompt yazmayı öğrenmeden önce ne yazdığınızı anlamanız gerekiyor.

---

## Bu Modülün Tek Hedefi

Sizi şu cümleden şu cümleye taşımak:

❌ *"AI'ya komut veriyorum."*  
✅ *"AI'yla bir şeyi birlikte inşa ediyorum — ve o inşanın kalitesi büyük ölçüde benden geliyor."*

Bu fark küçük görünüyor. Pratikte her şeyi değiştiriyor.

---

## 1.1 — LLM Ne Yapıyor, Gerçekten?

Teknik cevap karmaşık. Sezgisel cevap basit:

**Bir LLM, bir sonraki kelimeyi tahmin etmek için önceki her kelimeye bakıyor.**

Bu kadar. Gerisi bu temel mekanizmanın üstüne inşa edilmiş mühendislik.

Ama bu "basit" mekanizmadan şu üç kritik sonuç çıkıyor:

### Bağlam Penceresi

Modelin "kısa süreli belleği" var. Konuşmanın başına yazdığınız şey, sonundaki cevabı etkiliyor. Ama bu pencere sonsuz değil. Çok uzun konuşmalarda model erken bağlamı "unutuyor" — teknik olarak attığı için değil, dikkat dağıldığı için.

**Pratik çıkarım:** Önemli bağlamı her zaman yakın tut. Uzun konuşmada kritik bir kısıtı en başta söylediyseniz, ara ara tekrarlayın.

### Dikkat Mekanizması

Model her kelimeye eşit bakmıyor. Bazı kelimeler (özellikle nadir, spesifik, ya da konuyla çok alakalı olanlar) daha fazla "dikkat çekiyor." Bu yüzden:

- Genel kelimeler zayıf sinyal verir: *"iyi bir yazı yaz"*
- Spesifik kelimeler güçlü sinyal verir: *"ikna edici, veri destekli, C-suite okuyucuya yönelik bir yönetici özeti yaz"*

### Olasılık Dağılımı

Model tek bir cevap üretmiyor. Her adımda bir olasılık dağılımı hesaplıyor ve oradan örnekliyor. Bu yüzden aynı promptu iki kez çalıştırdığınızda farklı çıktılar alıyorsunuz — bu bir hata değil, tasarım gereği.

**Pratik çıkarım:** Kritik kararlarda tek çıktıya güvenmeyin. Aynı promptu 3 kez çalıştırın, en tutarlı cevabı seçin (bu "self-consistency" tekniğinin temelidir — Modül 2'de detaylandırıyoruz).

---

## 1.2 — "Komut" Yanılgısı

Yazılımcılar için özel not: LLM bir API değil. Deterministik değil, stokastik. Aynı input her zaman aynı output'u üretmez.

Yazılımcı olmayanlar için özel not: LLM bir sihir değil. İçinde "anlayan" bir şey yok. Olağanüstü istatistik yapıyor.

Her iki grup için ortak gerçek: **LLM, verdiğiniz bağlamla orantılı çalışıyor.** Zayıf bağlam → zayıf çıktı. Her seferinde.

---

## 1.3 — Prompt = Niyet Tercümesi

Şu soruyu sorun kendinize: *"Bunu bir insan asistana nasıl açıklardım?"*

Çoğu zaman o açıklama — rol, bağlam, hedef kitle, kısıtlar dahil — zaten iyi bir promptun taslağıdır.

### Kötü Prompt Anatomisi

Eğitimde gördüğümüz gerçek örnekler (anonim):

```
"Bana rapor yaz."
```

Model için belirsiz olan şeyler:
- Ne hakkında rapor?
- Kim için?
- Ne kadar uzun?
- Hangi ton?
- Hangi bilgilere erişimim var?

Model cevap verir — ama siz beğenmezsiniz. Bu modelin başarısızlığı değil, bağlam eksikliğidir.

### Aynı Niyetin İyi Versiyonu

```
Bir lojistik şirketinin operasyon müdürüsün. 
2024 Q3 teslimat gecikme verilerini analiz eden 
bir yönetici özeti hazırla.

Okuyucu: CEO ve CFO.
Ton: Doğrudan, sonuç odaklı.
Format: 3 bölüm — özet (3 cümle), temel bulgular (madde madde), öneriler (öncelikli sırayla).
Uzunluk: 400 kelimeyi geçmesin.
```

Fark: Bağlam, hedef kitle, ton, format, kısıt — hepsi var.

---

## 1.4 — Turing Testi Deneyi (Eğitim Aktivitesi)

Eğitimde şu deneyi yaptık. Burada da deneyebilirsiniz.

Aşağıdaki iki metinden hangisi bir insandan, hangisi AI'dan geliyor?

**Metin A:**
> "Dijital dönüşüm sadece teknoloji değil, kültür meselesidir. Pek çok şirket araçlara yatırım yaparken insan faktörünü göz ardı eder. Oysa değişim yönetimi, yazılım yönetiminden çok daha zordur."

**Metin B:**
> "Dijital dönüşüm sürecinde karşılaşılan en önemli engellerden biri, teknolojik altyapı eksikliklerinden ziyade kurumsal kültür ve değişime direnç olarak öne çıkmaktadır. Literatür, başarılı dijital dönüşümlerin teknik unsurlardan önce insan merkezli yaklaşımları önceliklendirdiğini göstermektedir."

---

Cevap: İkisi de AI. Metin A, "doğal konuşma tarzı" promptuyla; Metin B, "akademik ton" promptuyla üretildi.

**Çıkarım:** Modelin tonu, üslubu, hatta "insan gibi görünmesi" büyük ölçüde prompttaki ton sinyallerinden geliyor.

---

## Modül Özeti

| Kavram | Özü |
|--------|-----|
| Bağlam penceresi | Model önceki her şeye bakıyor, ama dikkat azalıyor |
| Dikkat mekanizması | Spesifik kelimeler > genel kelimeler |
| Olasılık dağılımı | Aynı prompt ≠ aynı çıktı |
| Prompt = niyet tercümesi | İyi prompt, iyi bir açıklama gibi yazılır |

---

## Devam

→ [Modül 2: Prompt Mimarisi](../02-prompt-architecture/)  
→ [Egzersiz 1](../../exercises/01-mental-model-exercises.md)  
→ [Derinlemesine: LLM Mimarisi Makalesi](../../docs/how-llms-work.md)
