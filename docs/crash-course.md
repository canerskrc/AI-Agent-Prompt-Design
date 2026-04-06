# Hızlı Başlangıç Rehberi

*3 saatlik eğitime katılamadıysanız ya da tazeleme istiyorsanız buradan başlayın.*  
*Okuma süresi: ~25 dakika. Pratik dahil: ~1 saat.*

---

## Neden Buradan Başlıyorsunuz?

Muhtemelen şunlardan birini yaşıyorsunuz:

- AI kullanıyorsunuz ama sonuçlar tutarsız
- "Prompt mühendisliği" duyuyorsunuz ama ne olduğunu bilmiyorsunuz
- Ekibinizde AI kullanımını standardize etmek istiyorsunuz
- Ya da sadece meraklısınız

Bu rehber 3 şeyi yapacak: Çerçeve verecek, somut teknikler verecek, nereye gideceğinizi gösterecek.

---

## Çerçeve: Tek Cümle

> **İyi prompt = modele ne istediğinizi değil, neden istediğinizi, kime istediğinizi ve nasıl istediğinizi anlatmak.**

---

## 5 Dakikada 5 Katman

Her etkili prompt şu beş katmanı içeriyor. Eksik katman = modelin doldurduğu boşluk.

```
┌─────────────────────────────────────────────────┐
│  ROL         Sen bir ... sın                    │
│  BAĞLAM      Durum şu, okuyucu şu               │
│  GÖREV       Şunu yap (spesifik eylem fiiliyle)  │
│  KISIT       Yapma / sadece / en fazla           │
│  FORMAT      Tablo / madde / paragraf / JSON     │
└─────────────────────────────────────────────────┘
```

**Test:** Bir prompt yazdığınızda bu beş kategoriden hangisi eksik? Eksik olan = model tahmin ediyor.

---

## 10 Dakikada Hızlı Pratik

Şu promptu çalıştırın (herhangi bir AI aracında):

**Versiyon 1:**
```
Bana liderlik hakkında bir şeyler yaz.
```

**Versiyon 2 (5 katman):**
```
Rol: Deneyimli bir yönetim danışmanısın.
Bağlam: Okuyucu, ilk yöneticilik pozisyonuna yeni geçmiş, 
         30 yaşında bir mühendis.
Görev: İlk 90 günde kaçınılması gereken en yaygın 3 hatayı anlat.
Kısıt: Klişe tavsiyelerden kaçın ("iletişim önemli" gibi). 
       Somut, yaşanmış gibi hissettiren örnekler kullan.
Format: Her hata için: hata adı + nasıl oluyor + önleme yolu
```

Farkı görün. Sonra kendi işinizden bir prompt yazın ve aynı çerçeveyi uygulayın.

---

## Agent Nedir? (5 Dakika)

Prompt yazdığınızda bir soruya cevap alıyorsunuz.

Agent kurduğunuzda bir sistemin çalışmasını izliyorsunuz.

```
Prompt: "X'i araştır" → cevap
Agent:  "X'i araştır" → 
        [web'e bak] → 
        [ilgili kaynakları oku] → 
        [notlar al] → 
        [çelişkileri tespit et] → 
        [rapor yaz]
```

Agent'ın farkı: Araçlara erişimi var ve kendi kendine karar veriyor.

**Bugün agent'a ihtiyacınız var mı?** Muhtemelen hayır. Çoğu kurumsal kullanım için iyi promptlar ve prompt zincirleri yeterli. Agent ancak dinamik karar verme gerçekten gerektiğinde değer katıyor.

---

## Öğrenme Yolu

Nereden başlayacaksınız?

**Sıfırdan başlıyorsanız:**
1. [Modül 1: Zihinsel Model](modules/01-mental-model/) → okuyun
2. [Egzersiz 1.3: Bağlam Deneyi](exercises/01-mental-model-exercises.md) → yapın
3. [Temel Örnekler 01-03](examples/basic/) → kendi işinize uyarlayın

**Temel prompt yazıyorsanız:**
1. [Modül 2: Prompt Mimarisi](modules/02-prompt-architecture/) → okuyun
2. [Egzersiz 2.1: Peer Review](exercises/02-architecture-exercises.md) → bir meslektaşınızla yapın
3. [Orta Düzey Örnekler](examples/intermediate/) → sektörünüze yakın olanları alın

**Otomasyon düşünüyorsanız:**
1. [Modül 3: Agent Düşüncesi](modules/03-agent-thinking/) → okuyun
2. [Egzersiz 3.2: Agent Taslak Tasarımı](exercises/02-architecture-exercises.md) → kağıtta çizin
3. [İleri Düzey Örnekler](examples/advanced/) → kod varsa çalıştırın

---

## Sık Sorulan Sorular

**"Hangi AI aracını kullanmalıyım?"**  
Herhangi biri ile başlayın. Prensipler araç bağımsız. Fark göze çarpmaya başladığında karşılaştırma yapın.

**"Prompt mühendisliği öğrenmek ne kadar sürüyor?"**  
Temel çerçeve: 1-2 gün pratikle. İyi olmak: birkaç hafta aktif kullanım. Ustalaşmak: süregelen pratik.

**"Kodlama bilmem gerekiyor mu?"**  
Agent geliştirme için evet, büyük ölçüde. Prompt tasarımı için hayır.

**"AI işimi elimden alacak mı?"**  
Dürüst cevap: Bazı işler değişecek. Hangileri? Tekrarlayan, kurallara dayalı, bilgi işleme görevleri. Değişmeyenler? Yargı, ilişki, bağlamsal karar verme gerektiren işler. En iyi konum: Her ikisini de yapabilmek.

---

*Soru veya geri bildirim: GitHub Issues açabilirsiniz.*
