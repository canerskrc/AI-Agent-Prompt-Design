# LLM'ler Gerçekte Ne Yapıyor?

*Bu makale teknik bir referans değil. "Sezgisel doğruluk" hedefleniyor: Mekanizmaları matematiksel olarak doğru değil, işlevsel olarak doğru anlatmak.*

---

## Problem: Neden Bu Önemli?

Bir araç kullanıyorsanız nasıl çalıştığını tam bilmeniz gerekmez. Araba kullanmak için motor termodinamiğini bilmek zorunda değilsiniz.

Ama LLM'lerle çalışırken bu analoji biraz yanıltıcı. Çünkü LLM'in nasıl "düşündüğünü" anlamadan neden iyi çalıştığını veya neden başarısız olduğunu tahmin edemezsiniz.

Bu makale şu üç soruyu yanıtlıyor:
1. LLM token'ları nasıl işliyor?
2. "Dikkat" gerçekte ne anlama geliyor?
3. Bu mekanik prompt tasarımını nasıl etkiliyor?

---

## 1 — Token: Modelin Alfabe Birimi

LLM kelimelerle değil, token'larla çalışıyor. Token'lar yaklaşık olarak kelime parçaları.

```
"Yapay zeka çok ilginç" →

["Yap", "ay", " zeka", " çok", " ilginç"]
```

Türkçe için bu özellikle önemli: Türkçe eklemeli bir dil. "Çalışabilirsiniz" gibi bir kelime birçok token'a bölünebilir. Bu yüzden aynı içerik için İngilizce genellikle daha az token harcar — dolayısıyla İngilizce prompt'lar bazen daha verimli.

**Pratik sonuç:** Token sayısı maliyet demek. Uzun prompt = yüksek maliyet. Uzun konuşma = yüksek maliyet. Bağlam penceresinin dolması = sonraki token'lar eskilerini "iter."

---

## 2 — Dikkat Mekanizması: Her Şeyin Merkezi

Transformatör mimarisinin kalbi "attention" (dikkat) mekanizması. Matematiksel formülasyonu karmaşık ama sezgisi basit:

**Her token, diğer tüm token'lara bakıyor ve "bu benim için ne kadar önemli?" diye soruyor.**

Bir örnekle:

```
"Banka nehrin kenarındaydı ve sular yükselmişti."
```

"Banka" token'ı bu cümlede ne anlama geliyor? Finansal kurum mu, nehir kıyısı mı?

Dikkat mekanizması "nehir", "sular", "kenar" token'larına yüksek ağırlık verir. Sonuç: Model "banka"yı nehir kıyısı olarak yorumlar.

Aynı metin farklı bağlamda:

```
"Banka hesabım bloke oldu ve paramı çekemiyorum."
```

Şimdi "hesap", "para", "çekemiyorum" yüksek ağırlık alır. Aynı kelime, farklı anlam.

**Prompt tasarımına etkisi:** Spesifik, anlamlı kelimeler güçlü sinyal verir. Genel kelimeler zayıf sinyal. "İyi bir yazı yaz" → "iyi" ve "yazı" kelimelerine model hangi ağırlığı verecek? Bilinmez. "Yönetici için özlü, veri destekli bir not yaz" → her kelime güçlü ve yönlendirici sinyal.

---

## 3 — Bağlam Penceresi: Kısa Süreli Bellek

LLM'in bir "belleği" var ama bu bellek çok sınırlı ve geçici:

```
┌─────────────────────────────────────────────────────────┐
│                     Bağlam Penceresi                    │
│                                                         │
│  [Sistem promptu] [Konuşma geçmişi] [Şu anki mesaj]    │
│                                                         │
│  ←──────────────── N token ────────────────────────────→│
│  (GPT-4: ~128K, Claude: ~200K, Gemini: ~1M+)           │
└─────────────────────────────────────────────────────────┘
```

Bu pencere dolduğunda ne olur? Model eski token'ları "unutur" — daha doğrusu onlara artık dikkat etmez. Uzun bir konuşmada başa söylediğiniz kritik bir kısıt, sonunda modelin radarından çıkabilir.

**Pratik sonuç:** 
- Kritik bilgiyi hem başa hem de yakın bağlama koyun
- Çok uzun konuşmalarda (özellikle agent kullanımında) kritik kısıtları ara ara tekrarlayın
- Uzun dokümanlarla çalışırken chunking (parçalama) stratejisi şart

---

## 4 — Sıcaklık: Determinizm vs Yaratıcılık

Model her token üretiminde bir olasılık dağılımı hesaplıyor. "Sıcaklık" (temperature) bu dağılımı etkiliyor:

```
Düşük sıcaklık (0.0-0.3):
Olasılık: [token_A: 0.85, token_B: 0.10, token_C: 0.05]
Model neredeyse her zaman token_A'yı seçer.
Sonuç: Tahmin edilebilir, tutarlı ama tekrarcı.

Yüksek sıcaklık (0.7-1.0):
Olasılık: [token_A: 0.45, token_B: 0.35, token_C: 0.20]
Model token_A, B veya C'yi seçebilir.
Sonuç: Yaratıcı, çeşitli ama bazen tutarsız.
```

**Ne zaman hangi sıcaklık?**

| Görev | Önerilen Sıcaklık |
|-------|-------------------|
| Kod yazma | 0.0 - 0.2 |
| Veri analizi | 0.0 - 0.3 |
| Özet ve çeviri | 0.2 - 0.4 |
| E-posta, rapor | 0.3 - 0.6 |
| Yaratıcı yazı | 0.6 - 0.9 |
| Beyin fırtınası | 0.7 - 1.0 |

---

## 5 — Neden Bazen "Halüsine" Ediyor?

"Halüsinasyon" (model gerçek olmayan şeyler üretiyor) bu mekanizmadan anlaşılıyor:

Model bir sonraki token'ı tahmin ediyor. Bu tahmin bağlam + eğitim verisine dayanıyor. Eğitim verisinde olmayan bir şey sorduğunuzda ne yapıyor? En olası token'ı üretiyor — ama bu token gerçeği yansıtmayabilir.

Model "bilmiyorum" demeyi öğrenmemiş mi? Belirli ölçüde öğrenmiş, ama her zaman başarılı değil. "Bilmiyorum" da bir token dizisi — ve bazı bağlamlarda model bu diziyi üretmek yerine daha "yardımsever görünen" bir yanıt üretiyor.

**Pratik sonuç:** 
- Spesifik, doğrulanabilir bilgi için model çıktısını doğrulayın
- "Emin değilsen belirt" kısıtı gerçekten işe yarıyor
- Retrieval Augmented Generation (RAG) — modele kendi verinizi bağlam olarak vermek — halüsinasyonu önemli ölçüde azaltıyor

---

## 6 — RLHF: Modelin "Karakterini" Kim Şekillendirdi?

Temel dil modeli (base model) inanılmaz derecede yetenekli ama sizi yanıltabilir, zararlı içerik üretebilir, faydasız cevaplar verebilir.

ChatGPT, Claude, Gemini gibi asistan modeller şu ek eğitim aşamasından geçiyor:

**RLHF — Reinforcement Learning from Human Feedback:**

1. Model binlerce yanıt üretiyor
2. İnsan değerlendiriciler hangi yanıtların daha iyi olduğunu işaretliyor
3. Model bu geri bildirimden öğreniyor
4. Tekrar et → "yararlı, zararsız, dürüst" davranış ortaya çıkıyor

**Bu ne anlama geliyor?** Modelin "karakteri" insan tercihleriyle şekillendirildi. Bu yüzden "yardımcı olma" eğilimi var. Bu yüzden "özür dilemek" biliyor. Bu yüzden bazı konularda temkinli davranıyor.

Ve bu yüzden prompt'larınızla modelin bu eğilimlerini hem kullanabilir hem yönetebilirsiniz.

---

## Özet: Beş Temel İçgörü

1. **Token = harf değil, anlam parçası.** Türkçe için bu özellikle maliyet etkisi yaratıyor.

2. **Dikkat = bağlamsal anlam.** Model aynı kelimeyi farklı bağlamlarda farklı anlar. Spesifik kelimeler güçlü sinyal.

3. **Bağlam penceresi = kısa süreli bellek.** Kritik bilgiyi yakın tutun. Uzun konuşmalarda tekrarlayın.

4. **Sıcaklık = yaratıcılık/tutarlılık dengesi.** Göreve göre ayarlayın. API kullanıyorsanız bu parametreyi kontrol edin.

5. **Halüsinasyon = olasılık mekanizmasının yan etkisi.** Doğrulanabilir bilgi için RAG veya kaynak verme.

---

## Daha Fazlası İçin

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — Orijinal transformatör makalesi (teknik)
- [Chain-of-Thought Prompting Elicits Reasoning in LLMs](https://arxiv.org/abs/2201.11903) — CoT'un akademik temeli
- [Constitutional AI](https://arxiv.org/abs/2212.08073) — Claude'un güvenlik yaklaşımı

---

*→ [Modül 1'e dön](../modules/01-mental-model/)*
