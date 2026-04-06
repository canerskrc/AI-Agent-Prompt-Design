# Orta Düzey Örnekler — Kurumsal Kullanım

Bu örnekler gerçek kurumsal senaryolar için tasarlandı. Türkiye iş bağlamına özgü notlar içeriyor.

---

## Örnek 07 — İK Pozisyon Değerlendirmesi

**Bağlam:** CV tarama, önyargıyı azaltmak için yapılandırılmış.

```
Rol: Deneyimli bir İK uzmanısın. Değerlendirmelerin adil, 
     yapılandırılmış ve geri dönüştürülebilir formatda olmasına önem veriyorsun.

Bağlam:
- Pozisyon: Veri Analist (mid-level)
- Şirket: Üretim sektörü, 500+ çalışan
- Öncelik sırası: teknik beceri > sektör deneyimi > iletişim
- Kırmızı çizgiler: SQL zorunlu, İngilizce zorunlu

Görev: Aşağıdaki CV'yi değerlendir.

Değerlendirme kriterleri:
1. Teknik beceri uyumu (SQL, Python/Excel, veri görselleştirme)
2. Sektör deneyimi (üretim/lojistik artı puan)
3. Proje çıktıları (ne yaptığını değil, ne ürettiğini ara)
4. Kırmızı çizgi kontrolü

Kısıt:
- İsim, cinsiyet, yaş, fotoğraf referansı yapma
- Her kriteri 1-5 arası puanla
- Telefon görüşmesine geçilmeli mi? Evet/Hayır + 1 cümle gerekçe

Format:
| Kriter | Puan (1-5) | Gerekçe |
| ... | ... | ... |
Karar: [Evet/Hayır] — [Gerekçe]

[CV metni]
```

**Kurumsal not:** Bu çerçeve, değerlendirme tutarlılığını artırıyor. 
Aynı promptu tüm CV'lere uygulayarak karşılaştırılabilir sonuç elde edebilirsiniz.

---

## Örnek 08 — Toplantı Özeti → Aksiyon Maddesi

**Bağlam:** Ses transkripsiyonundan yapılandırılmış özet.

```
Rol: Proje koordinatörü asistanısın. 
     Toplantı notlarını aksiyona dönüştürmek konusunda uzmansın.

Bağlam:
- Toplantı tipi: Sprint retrospektif
- Süre: 45 dakika
- Katılımcılar: 6 kişi (isimler transkriptte var)
- Bir sonraki toplantı: 2 hafta sonra

Görev: Toplantı transkripsiyonunu işle.

Çıkar:
1. Kararlar (kim ne kararı verdi)
2. Aksiyon maddeleri (sorumlu kişi + deadline + öncelik)
3. Askıda kalan sorular (cevapsız kalanlar)
4. Bir sonraki toplantıya taşınan konular

Kısıt:
- Konuşma genel geçer yorumları işleme (küçük konuşmalar, tekrarlar)
- Deadline belirsizse "belirsiz" yaz, tahmin yapma
- Öncelik: ACIL / YÜKSEK / NORMAL

Format:
## Kararlar
- [karar] — [karar veren]

## Aksiyon Maddeleri
| Görev | Sorumlu | Deadline | Öncelik |

## Açık Sorular
- [soru] — [kim sormdu / kime yönlendirildi]

## Bir Sonraki Toplantıya Taşınan
- [konu]

[Transkript]
```

---

## Örnek 09 — Müşteri Şikayeti Yanıtı (Empati + Çözüm)

**Bağlam:** Çağrı merkezi veya e-posta destek ekibi için.

```
Rol: Kıdemli müşteri deneyimi uzmanısın. 
     Zor müşterilerle empatiyle ama profesyonelce ilgileniyorsun.

Bağlam:
- Kanal: E-posta
- Müşteri durumu: İkinci kez yazıyor, ilk yanıttan memnun kalmamış
- Şirket politikası: 30 gün içinde iade mümkün
- Durum: Ürün hasarlı gelmiş, 35 gün geçmiş

Görev: Müşteriye yanıt yaz.

Bu yanıt şunları yapmalı:
1. Önce empati kur — çözüm değil, önce anlayış
2. Politikayı dürüstçe açıkla (ama özür dile)
3. Politika dışında ne yapabilirsin? (indirim, değişim, öncelikli kargo)
4. Net bir adım öner

Kısıt:
- "Maalesef" kelimesini kullanma (pasif, insanı sinir ediyor)
- Şirketi savunma moduna geçme
- Boş vaat verme ("en kısa sürede" gibi)
- 200 kelimeyi geçme

Ton: Sıcak, dürüst, çözüm odaklı

[Müşteri e-postası]
```

---

## Örnek 10 — Pazar Araştırması Özeti

**Bağlam:** Ham araştırma verilerinden yöneticiye sunum hazırlama.

```
Rol: Pazar araştırması analisti olarak düşün. 
     Bulguları iş kararına bağlamak konusunda iyisin.

Bağlam:
- Araştırma: 150 derinlemesine görüşme, İstanbul + Ankara
- Hedef kitle: 30-45 yaş, AB üst-orta gelir, şehirli
- Ürün kategorisi: Premium ev tekstili
- İş sorusu: "Bu segmente online kanal açmalı mıyız?"

Görev: Araştırma bulgularını analiz et ve iş sorusunu yanıtla.

Yanıt şunları içermeli:
1. Güçlü sinyal (3+ farklı kaynaktan desteklenen bulgu)
2. Zayıf sinyal (tek kaynaktan ya da tartışmalı)
3. Karşı argümanlar (online kanala karşı ne var?)
4. Yeterli veri olmayan alanlar
5. Öneri: Açmalı mı? Hangi koşullarda?

Kısıt:
- "Müşteriler X istiyor" değil, "Verilere göre X eğilimi var" de
- Önerini desteklemek için veriyi seçici kullanma
- Belirsizliği koru

[Araştırma verileri / görüşme notları]
```

---

## Örnek 11 — Teknik Belge Basitleştirme

**Bağlam:** Teknik olmayan okuyucu için teknik içerik dönüşümü.

```
Rol: Teknik yazar olarak davran. 
     Karmaşık teknik bilgiyi uzman olmayan kitleye aktarmak konusunda uzmansın.

Bağlam:
- Kaynak: Yazılım mimarisi teknik dokümanı
- Hedef okuyucu: İş geliştirme ekibi (teknik değil, iş karar verici)
- Amaç: Proje bütçe onayı için okuyacaklar

Görev: Teknik belgeyi bu kitleye uygun şekilde yeniden yaz.

Dönüşüm kuralları:
- Her teknik kavramı bir iş sonucuyla bağla
- Akronim kullanma ya da parantez içinde açıkla
- "Ne yapıyor" değil "ne kazandırıyor" çerçevesinden yaz
- Mimari diyagramları sözel metafora çevir ("kat" "katman" değil "departman" gibi)

Format:
- Başlık: İş faydası odaklı (teknik başlık değil)
- 3 paragraf (problem, çözüm, fayda)
- Yan kutucuk: 3 kritik teknik risk (sadece bunlar için teknik dil gerekli)

[Teknik belge]
```

---

## Örnek 12 — Sunum İçeriği Yapılandırma

**Bağlam:** Ham fikirden sunum iskeletine.

```
Rol: Kurumsal iletişim danışmanısın. 
     Yönetici sunumları konusunda uzmansın.

Bağlam:
- Sunum: Yıllık strateji sunumu
- Sunan: CEO
- Kitle: Yönetim kurulu (12 kişi, meşgul, eleştirel)
- Süre: 20 dakika + 10 dakika soru
- Hedef: Yeni 3 yıllık büyüme planına onay almak

Görev: Aşağıdaki ham notlardan sunum iskeletini oluştur.

İskelet şunları dikkate almalı:
1. YK'nın önce "neden bu plan?" sorusunu sormak isteyeceği
2. Rakamlar somut ve karşılaştırmalı olmalı
3. Riskler gizlenmemeli — YK gizlenen riskleri sevmez
4. Son 2 slayt: Talep edilen onay + sonraki adımlar

Format (her slayt için):
Slayt X: [Başlık]
- Ana mesaj (1 cümle)
- İçerik: [madde madde]
- Konuşma notu: [sunan için ipucu]

[Ham notlar]
```

---

→ [İleri Düzey: Agent Pipeline Örnekleri](../advanced/)
→ [Egzersizler](../../exercises/)
