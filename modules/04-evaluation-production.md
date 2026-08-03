# Modül 4: Değerlendirme ve Production

> Bir prompt'un çalışması yeterli değildir. Sorulması gereken soru şudur: bu sistem, siz bakmadığınızda da doğru çalışıyor mu?

---

## 4.1 Demo ile Production Arasındaki Fark

Bir demo, kontrollü koşullarda çalışır. Siz girdiyi seçersiniz, sonucu siz okursunuz, hata olursa siz fark edersiniz.

Production bunun tam tersidir. Girdiyi siz seçmezsiniz, kullanıcı seçer. Sonucu siz okumazsınız, çoğu zaman kimse okumaz. Hata olduğunda fark eden ilk kişi genelde müşteridir, sizin log dosyanız değil.

Silikon Vadisi'ndeki olgun ekipler bu farkı bir cümleyle özetler: demo bir fikri kanıtlar, production bir sistemi taşır. İkisi farklı disiplinler ister.

Üç soru bu geçişi test eder:

1. Bu prompt, hiç görmediğiniz bir girdiyle karşılaştığında ne yapar.
2. Bu prompt bin kez çalıştığında, kaç tanesi kabul edilebilir kalitede.
3. Bu prompt bozulduğunda, bunu kaç saat sonra fark edersiniz.

Üçüncü sorunun cevabı "bilmiyorum" ise, henüz production'da değilsiniz. Sadece production'a benzeyen bir demo işletiyorsunuz.

---

## 4.2 Ölçüm Olmadan İterasyon Yoktur

Prompt geliştirmek deneme yanılma sürecidir. Deneme yanılma, sonucu ölçemediğiniz anda tesadüfe döner.

Üç senaryoyu ayırt edin:

**Tek seferlik görev.** Ölçüm gerekmez. Çıktı işinizi görüyorsa iş bitmiştir.

**Tekrarlayan görev.** Basit bir ölçüm şarttır. Aynı kaliteyi her seferinde istiyorsunuz, bu yüzden kaliteyi tanımlamanız gerekir.

**Sistem veya pipeline.** Sistematik ölçüm zorunludur. Çıktı kalitesi artık bir iş sürecini, bir müşteri deneyimini veya bir gelir kalemini etkiliyor.

Çoğu ekibin hatası, üçüncü kategoride çalışırken birinci kategorinin disipliniyle ilerlemesidir. "Bence iyi görünüyor" bir ölçüm değildir, bir izlenimdir.

Bu repodaki [evaluation-guide.md](../../docs/evaluation-guide.md) beş düzeyli somut bir çerçeve sunar: bireysel skor kartından production monitoring'e kadar. Bu modül o çerçevenin arkasındaki karar mantığını anlatır.

---

## 4.3 Hangi Düzeyde Durmalısınız

Değerlendirme yatırımı, kullanım hacmiyle orantılı olmalıdır. Aşırı yatırım kadar yetersiz yatırım da hatadır.

```
Kaç kez kullanılacak?

haftalık 10'dan az kullanım
    Skor kartı yeterli. Beş dakikanızı alır.

günlük 10 ile 100 arası kullanım
    A/B test ve temel loglama gerekir.
    Birden fazla kişi kullanıyorsa ekip standardı da gerekir.

günlük 100'den fazla kullanım veya bir pipeline'ın parçası
    LLM'i hakem olarak kullanan otomatik değerlendirme gerekir.
    Production monitoring zorunludur, opsiyonel değildir.
```

Bir ekip bu ölçeği yanlış okuduğunda iki yöne düşer. Ya günlük on kullanımlık bir prompt için haftalarca otomatik test altyapısı kurar, ya da günde on bin çağrı yapan bir sistemi hiç izlemeden çalıştırır. İkincisi çok daha yaygın ve çok daha pahalıdır.

---

## 4.4 Production'da Neyi İzlersiniz

İzlemenin amacı sistemin çalıştığını görmek değildir. İzlemenin amacı sistemin ne zaman ve neden bozulduğunu, siz sormadan önce bilmektir.

Minimum izleme seti üç kategoriye ayrılır.

**Performans sinyalleri.** Gecikme süresi, hata oranı, token maliyeti. Bunlar teknik sinyallerdir, kolayca ölçülür, genelde ilk kurulan şeylerdir.

**Kalite sinyalleri.** Kullanıcı çıktıyı düzeltti mi, tamamen reddetti mi, aynı soruyu tekrar sordu mu. Bunlar zor ölçülür çünkü doğrudan bir sayı değildir, ama asıl önemli olan bunlardır.

**İş sinyalleri.** Bu çıktı bir e postaysa açıldı mı, bir öneri ise kabul edildi mi, bir özet ise okuyan kişi ek soru sordu mu. Bu sinyaller prompt kalitesini iş sonucuna bağlar.

Çoğu ekip sadece birinci kategoriyi kurar ve orada durur. Sistem "çalışıyor" görünür çünkü hata vermiyor, gecikme normal, maliyet bütçede. Ama kullanıcı çıktının yarısını her seferinde elle düzeltiyor olabilir. Bu, izlemeden görünmeyen bir başarısızlıktır.

---

## 4.5 Sessiz Bozulma: Drift

Bir prompt bugün mükemmel çalışabilir ve üç ay sonra aynı prompt daha kötü sonuç verebilir. Kod değişmedi, prompt değişmedi. Peki ne değişti.

Üç yaygın sebep vardır.

**Model güncellemesi.** Sağlayıcı arka planda modeli günceller. Sizin promptunuz artık farklı bir modelle konuşuyor, siz bunu fark etmeden.

**Bağlam kayması.** Girdileriniz zamanla değişir. Müşteri sorularının doğası, ürün kataloğunuz, kullanıcı davranışı altı ay önceki test setinizden farklılaşır.

**Ölçek etkisi.** On örnekte mükemmel çalışan bir prompt, on bin farklı örnekte önceden görmediğiniz uç durumlarla karşılaşır.

Drift'e karşı tek savunma düzenli yeniden testtir. Haftalık olarak sabit bir referans test setini çalıştırıp sonuçları önceki haftayla karşılaştırmak, sürprizi büyük ölçüde azaltır.

---

## 4.6 Silikon Vadisi Standardı: Production Öncesi Kontrol Listesi

Bir prompt sistemi gerçek kullanıcıya çıkmadan önce şu sorulara net bir cevabınız olmalı.

```
[ ] En az elli farklı girdiyle test edildi mi, sadece elinizdeki üç örnekle değil
[ ] Başarısızlık durumunda sistem sessizce mi bozuluyor, yoksa fark edilir bir hata mı veriyor
[ ] Maliyet, beklenen hacimde aylık bazda hesaplandı mı
[ ] Kalite düşüşünü fark etmek için bir alarm eşiği tanımlandı mı
[ ] Prompt bir sürüm numarasına sahip mi, değişiklik geçmişi tutuluyor mu
[ ] Kritik bir hata durumunda geri dönüş (rollback) planı var mı
```

Altı maddenin hepsine evet diyemiyorsanız, sistem demodan production'a henüz geçmedi. Bu bir eksiklik değil, bir aşamadır. Her sistem bu aşamadan geçer. Sorun, bu aşamayı atlayıp doğrudan geniş kullanıcı kitlesine çıkmaktır.

---

## Özet

Demo bir fikri kanıtlar. Ölçüm bir sistemi güvenilir kılar. Production bir sistemi, siz bakmasanız da doğru çalışır halde tutar.

Bu üçü ayrı beceridir ve sırayla gelir. Değerlendirme çerçevesini atlayıp doğrudan production'a çıkan ekipler, hatayı kullanıcıdan öğrenir. Silikon Vadisi'nde olgun mühendislik kültürünün ayırt edici özelliği budur: hatayı kullanıcıdan önce kendi ölçümünden öğrenmek.

---

*Sonraki adım: [evaluation-guide.md](../../docs/evaluation-guide.md) ile beş düzeyli çerçevenin prosedürel detaylarına bakın.*
*Uygulamalı örnekler için: [İleri Düzey Örnekler](../../examples/advanced/)*
