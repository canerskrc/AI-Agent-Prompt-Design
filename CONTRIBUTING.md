# Katkı Rehberi

Bu repo açık ve büyümeye devam ediyor. Katkılarınızı bekliyoruz.

---

## Ne Tür Katkılar Bekliyoruz?

### Yüksek öncelikli

- **Yeni gerçek örnekler:** Kendi iş bağlamınızdan anonimleştirilmiş vakalar
- **Prompt şablonları:** Test edilmiş, kullanıma hazır şablonlar
- **Hata düzeltmeleri:** Yanlış bilgi, bozuk kod, kırık link
- **Türkçe dil düzeltmeleri:** Yazım, dilbilgisi, akıcılık

### Orta öncelikli

- **Yeni modül önerileri:** Eksik olduğunu düşündüğünüz konular
- **Egzersiz ekleri:** Mevcut egzersizlere yeni varyantlar
- **Araç güncellemeleri:** Fiyat, özellik veya öneri güncellemeleri

### Kabul etmediğimiz

- Araç tanıtım reklamları (belirli ürünleri ödeme karşılığı önerme)
- Kaynak olmadan iddia edilen "araştırma bulguları"
- Kötü niyetle yazılmış içerik

---

## Nasıl Katkı Yapılır

### Küçük düzeltmeler

GitHub'da doğrudan dosyayı düzenleyin → Pull Request açın.

### Yeni içerik

1. Issue açın: "Şunu eklemek istiyorum: ..."
2. Geri bildirim alın
3. Fork → Branch → Commit → PR

### Prompt şablonu eklemek

`examples/templates/README.md` dosyasına şu formatta ekleyin:

```markdown
### [Şablon Kodu] — [Şablon Adı]

**Kullanım durumu:** [1 cümle]

```
[Şablon metni]
```

**Test edildi:** [Hangi AI aracıyla, kaç kez]
**Uyarılar:** [Varsa dikkat edilecekler]
```

---

## İçerik Standartları

### Doğruluk

- İddialar için kaynak gösterin
- Belirsiz bilgiler için "doğrulanmamış" işareti
- Kendinizi deney yapan biri olarak konumlandırın, otorite değil

### Dil

- Türkçe: Eğitim materyalleri için
- İngilizce: Kod yorumları ve kod için (standart)
- Jargon: Hedef kitleye uygun, ilk kullanımda açıkla

### Kod

- Python 3.10+ uyumlu
- Tip ipuçları (type hints) tercihli
- Her fonksiyon için docstring
- Bağımlılıkları `requirements.txt`'e ekle

---

## Repo Yapısı Hakkında

Yeni dosya eklerken mevcut yapıya uyun:

```
docs/         → Uzun form makaleler (.md)
modules/      → Eğitim modülleri (README.md per module)
examples/     → Kullanıma hazır örnekler
exercises/    → Uygulama aktiviteleri
notebooks/    → Jupyter deneyleri (.ipynb)
resources/    → Araç listeleri, referanslar
```

---

## Lisans

Bu repo [MIT Lisansı](LICENSE) altında yayınlanmaktadır.

Katkıda bulunarak, katkınızın aynı lisans altında yayınlanmasına izin vermiş olursunuz.

---

## Teşekkür

Bu projeye katkıda bulunanlar:
- Eğitim katılımcılarından gelen geri bildirimler
- Sahadan toplanan gerçek kullanım vakaları
- Açık kaynak topluluğu

---

*Sorunuz varsa: GitHub Issues*
